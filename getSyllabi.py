import os
from dotenv import load_dotenv
from canvasapi import Canvas
import requests
import json
from pathlib import Path
from InquirerPy import prompt
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

load_dotenv()

TOKEN = os.environ.get('CANVAS_API_TOKEN')
BASEURL = os.environ.get('CANVAS_API_DOMAIN')

# Gets the HTML code for the syllabus
def getSyllabusHTML(courseSession, courseCode, courseID):
    # Makes a API call and passes the TOKEN
    response = requests.get(f'https://ubc.beta.instructure.com/api/v1/courses/{courseID}?include[]=syllabus_body', headers={'Authorization': 'Bearer {}'.format(TOKEN)})
    if (json.loads(response.text)["syllabus_body"]):
        # Replaces beta link to prod so we have permission to get syllabus
        syllabusHTML = json.loads(response.text)["syllabus_body"].replace("ubc.beta.instructure.com", "ubc.instructure.com")

        path = Path(f"./output/syllabi/{courseSession}/{courseCode}/")

        # If the course folder does not exist, create it
        if not path.exists():
            os.makedirs(f"./output/syllabi/{courseSession}/{courseCode}/")
        # Creates the HTML file for the syllabus
        makePage = open(f"./output/syllabi/{courseSession}/{courseCode}/index.html", "w", encoding="utf-8")
        makePage.write(syllabusHTML)
        makePage.close()
        # Make source folder (syllabus pdfs will be manually added here)
        os.makedirs(f"./output/syllabi/{courseSession}/{courseCode}/source/")

def getSyllabi():
    year = inquirer.number(message="What year are you interested in?", default=None).execute()
    allTerms = ['S1', 'SA', 'S2', 'S', 'S1-2', 'W1', 'WA', 'W2', 'WC', 'W', 'W1-2']
    term_choices = [
        Separator(),
        Choice("All", name="All", enabled=True),
        Choice("S1", name="S1", enabled=False),
        Choice("SA", name="SA", enabled=False),
        Choice("S2", name="S2", enabled=False),
        Choice("S", name="S", enabled=False),
        Choice("S1-2", name="S1-2", enabled=False),
        Choice("W1", name="W1", enabled=False),
        Choice("WA", name="WA", enabled=False),
        Choice("W2", name="W2", enabled=False),
        Choice("WC", name="WC", enabled=False),
        Choice("W", name="W", enabled=False),
        Choice("W1-2", name="W1-2", enabled=False)
    ]

    print("\nInstructions:\n↑/↓: Change option\n[space]: Toggle selection\n[enter]/[return]: Submit answer\n")
    terms = inquirer.checkbox(
        message="Select the term(s) you are interested in:",
        choices=term_choices,
        cycle=False,
        transformer=lambda result: "%s terms%s selected"
        % (len(result), "s" if len(result) > 1 else ""),
    ).execute()
    
    accountNum = inquirer.number(message="What is your subaccount number? If you don't know, go to https://ubc.beta.instructure.com/accounts/ and click on your Faculty - in the URL, the number will show at the end. LFS is 15. ", default=None).execute()

    if ("All" in terms):
        terms = allTerms

    canvas = Canvas(BASEURL, TOKEN)

    account = canvas.get_account(accountNum)
    courses = account.get_courses()

    selectedSessions = []

    for term in terms:
        selectedSessions.append(str(year) + str(term))

    print("Please wait... Trying to get the information via Canvas API. This might take several minutes.\n\nFeel free to go on a walk or grab some coffee while waiting :)\n\n")
    for course in courses:
        courseSession = course.course_code.split(" ")[-1]
        if (courseSession in selectedSessions):
            path = Path(f"./output/syllabi/{courseSession}/")
            if not path.exists():
                os.makedirs(f"./output/syllabi/{courseSession}/")
            if not ("/" in course.course_code):
                try:
                    getSyllabusHTML(courseSession, course.course_code, course.id)
                except:
                    print("Failed to get syllabus. Course code: " + course.course_code)
    
    print("Done collecting syllabi!")

getSyllabi()
