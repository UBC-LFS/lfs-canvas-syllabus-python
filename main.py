import os
import re
import json
import requests
import inquirer
from urllib import request
from inquirer import errors
from dotenv import load_dotenv

load_dotenv()

CANVAS_PROD_URL = os.environ['CANVAS_PROD_URL']
CANVAS_TEST_URL = os.environ['CANVAS_TEST_URL']
CANVAS_API_TOKEN = os.environ['CANVAS_API_TOKEN']
API_VERSION = os.environ['API_VERSION']

TERMS = ['S_V', 'S1_V', 'S2_V', 'S1-2_V', 'SA_V', 'W_V', 'W1_V', 'W2_V', 'W1-2_V', 'WA_V', 'WC_V']

SYLLABI_FOLDER_PATH = os.path.join(os.getcwd(), 'syllabi')


def question_validation(answers, value):
    if len(value) == 0:
        raise errors.ValidationError('', reason='This field is required.')
    return True


def get_courses(account):
    print('\nPlease wait... Start fetching courses through Canvas API. This might take several minutes.')
    courses = {}
    has_next = True
    url = '{0}/{1}/accounts/{2}/courses?include[]=syllabus_body&include[]=term&per_page=100&page=1'.format(CANVAS_TEST_URL, API_VERSION, account)
    while has_next:
        res = requests.get(url, headers={ 'Authorization': 'Bearer ' + CANVAS_API_TOKEN })
        if res.status_code == 200:
            items = res.json()
            for item in items:
                term = item['term']['name']
                if term not in courses.keys():
                    courses[term] = []
                courses[term].append(item)

            if 'rel="next"' in res.headers['link']:
                links = res.headers['link'].split(',')
                for link in links:
                    if 'rel="next"' in link:
                        link = link.replace('<', '').replace('>', '')
                        url = link.split(';')[0]
            else:
                has_next = False
        else:
            has_next = False
            print('Error! Your GET request does not work at this time. Please try again.')
    
    print('Done! Downloaded Term(s): {0}'.format(courses.keys()))
    return courses


def load_courses():
    courses = []
    with open(os.path.join(os.getcwd(), 'courses.json'), 'r', encoding='utf-8') as f:
        courses = json.loads(f.read())
    return courses


def create_folder(path):
     if not os.path.exists(path):
        os.makedirs(path)

def create_html(course_code, path, syllabus):
    syllabus = delete_data_api_endpoint(syllabus)

    html = '''\
<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{0}</title>
    </head>
    <body>
        {1}
    </body>
</html>
    '''.format(course_code, syllabus)

    with open(os.path.join(path, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)


def delete_data_api_endpoint(syllabus):
    temps = re.findall(r'data-api-endpoint=[\'"]?([^\'" >]+)', syllabus)
    for temp in temps:
        t = 'data-api-endpoint="{0}"'.format(temp)
        syllabus = syllabus.replace(t, '')
    return syllabus


def download_file(course_path, syllabus, links, option):
    for link in links:
        if CANVAS_TEST_URL in link and 'files' in link and 'verifier' in link and 'preview' not in link:
            cid = link.split('/files/')[1].split('?')[0].split('/')[0]

            if cid and len(cid) > 0 and isinstance(int(cid), int):
                new_link = link.replace(CANVAS_TEST_URL, CANVAS_PROD_URL)

                if 'download' not in new_link:
                    new_link = new_link.replace(cid, cid + '/download')

                # Download a file
                f = request.urlopen(new_link)
                filename = f.headers.get_filename()
                if filename:
                    file_path = os.path.join(course_path, 'source')
                    create_folder(file_path)

                    request.urlretrieve(new_link, os.path.join(file_path, filename)) # download
                    syllabus = syllabus.replace('{0}="{1}"'.format(option, link), '{0}="./source/{1}"'.format(option, filename))
                    
    return syllabus


def create_syllabi(year, terms, items):
    print("\nLet's start creating course syllabi.\n")

    valid_terms = [year + t for t in terms]
    if 'All' in terms:
        valid_terms = [year + t for t in TERMS]

    for term in valid_terms:
        if term in items.keys():
            courses = items[term]
            print('Term {0} has {1} courses.'.format(term, len(courses)))

            for course in courses:
                term = course['term']['name']
                course_code = course['course_code']
                syllabus = course['syllabus_body']
                if term in valid_terms and syllabus:
                    term_path = os.path.join(SYLLABI_FOLDER_PATH, term)
                    create_folder(term_path)

                    course_path = os.path.join(term_path, course_code.replace('/', '-'))
                    create_folder(course_path)

                    syllabus = download_file(course_path, syllabus, re.findall(r'href=[\'"]?([^\'" >]+)', syllabus), 'href') # pdf, docx
                    syllabus = download_file(course_path, syllabus, re.findall(r'src=[\'"]?([^\'" >]+)', syllabus), 'src') # jpg, png
                    create_html(course_code, course_path, syllabus)
            
            print('{0} finished! \n'.format(term))
                            

if __name__ == '__main__':
    questions = [
        inquirer.Text('year', message='What year are you interested in?', validate=question_validation),
        inquirer.Checkbox('terms', message='What term(s) are you interested in?', choices=['All'] + TERMS, validate=question_validation),
        inquirer.Text('account', message="What is your Faculty account number? (If you don't know, go to https://ubc.beta.instructure.com/accounts/ and click on your Faculty - in the URL, the number will show at the end. Note that LFS is 1122 (old one: 15).)", validate=question_validation)
    ]
    selections = inquirer.prompt(questions)
    print('Your selections: ', selections)

    courses = get_courses(selections['account'])
    create_syllabi(selections['year'], selections['terms'], courses)

    print("Everything's done!")