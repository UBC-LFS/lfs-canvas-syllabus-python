import os
from dotenv import load_dotenv
from canvasapi import Canvas
import requests
import json
from pathlib import Path
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import exrex
import re
import urllib.request

load_dotenv()

TOKEN = os.environ.get('CANVAS_API_TOKEN')
BASEURL = os.environ.get('CANVAS_API_DOMAIN')

# Gets the HTML code for the syllabus
def getSyllabusHTML(courseSession, courseCode, courseID):
    # Makes a API call and passes the TOKEN
    response = requests.get(f'https://ubc.beta.instructure.com/api/v1/courses/{courseID}?include[]=syllabus_body', headers={'Authorization': 'Bearer {}'.format(TOKEN)})
    if (json.loads(response.text)["syllabus_body"]):
        
        path = Path(f"./output/syllabi/{courseSession}/{courseCode}/")
        # If the course folder does not exist, create it
        if not path.exists():
            os.makedirs(f"./output/syllabi/{courseSession}/{courseCode}/")
        # Make source folder if it doesn't exist yet
        sourcePath = f"./output/syllabi/{courseSession}/{courseCode}/source/"
        if not Path(sourcePath).exists():
            os.makedirs(sourcePath)

        # Replaces beta link to prod so we have permission to get syllabus
        syllabusHTML = json.loads(response.text)["syllabus_body"].replace("ubc.beta.instructure.com", "ubc.instructure.com")
        # print("\n"+ syllabusHTML +"\n")
        autoDownloadableFiles = re.findall(r"https://ubc.instructure.com/courses/[\d]+/files/[\d]+/download\W?verifier=[\S]*", syllabusHTML)
        if (autoDownloadableFiles):
            for autoDownloadableFile in autoDownloadableFiles:
                autoDownloadableFile = autoDownloadableFile.replace("\"", "").replace("\'", "")
                file = urllib.request.urlopen(autoDownloadableFile)
                filename = file.headers.get_filename()
                syllabusHTML = syllabusHTML.replace(autoDownloadableFile, f"./source/{filename}")
                open(f"./output/syllabi/{courseSession}/{courseCode}/source/{filename}", 'wb').write(file.read())
        
        redirectedSyllabi = re.findall(r"https://ubc.instructure.com/courses/[\d]+/files/[\d]+\W?verifier=[\S]*", syllabusHTML)
        if (redirectedSyllabi):
            for redirectedSyllabus in redirectedSyllabi:
                canvaPage = requests.get(redirectedSyllabus).text.replace("\"", "").replace("\'", "")
                downloadableSyllabus = re.findall(r"courses/[\d]+/files/[\d]+/download\W?download_frd=1&amp;verifier=[\w]*", canvaPage)
                # Using index 0 because there should only be 1 downloadable syllabus
                downloadURL = "https://ubc.instructure.com/" + downloadableSyllabus[0].replace("\"", "").replace("\'", "")
                file = urllib.request.urlopen(downloadURL)
                filename = file.headers.get_filename()
                try:
                    open(f"./output/syllabi/{courseSession}/{courseCode}/source/{filename}", 'wb').write(file.read())
                # Unsupported file name
                except Exception as e: 
                    filename = filename.replace("?", "-")
                    open(f"./output/syllabi/{courseSession}/{courseCode}/source/{filename}", 'wb').write(file.read())
                syllabusHTML = syllabusHTML.replace(redirectedSyllabus.replace("\"", "").replace("\'", ""), f"./source/{filename}")

        # Creates the HTML file for the syllabus
        makePage = open(f"./output/syllabi/{courseSession}/{courseCode}/index.html", "w", encoding="utf-8")
        makePage.write(syllabusHTML)
        makePage.close()

    else:
        with open(f"./output/coursesWithNoSyllabus/{courseSession}.json", "r") as noSyllabusPathFile:
            noSyllabusDict = json.load(noSyllabusPathFile)
            noSyllabusPathFile.close()

        with open(f"./output/coursesWithNoSyllabus/{courseSession}.json", "w") as noSyllabusPathFile:
            noSyllabusDict[f"{courseSession}"].append(courseCode)
            json.dump(noSyllabusDict, noSyllabusPathFile, indent = 4)
            noSyllabusPathFile.close()
    # print(f"Got {courseCode}")

def getSyllabi():
    # Generate a random session key to keep track of if a file was created during this session or during a previous session
    sessionKey = exrex.getone('(\d){7}([A-Z]|(a-z)){6}([\d]|(A-Z)|(a-z)){7}')

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

    canvas = Canvas(BASEURL, TOKEN)

    account = canvas.get_account(accountNum)
    courses = account.get_courses()

    selectedSessions = []

    if ("All" in terms):
        for term in range(len(allTerms)):
            allTerms[term] = str(year) + str(allTerms[term])
            selectedSessions = allTerms
    else:
        for term in terms:
            selectedSessions.append(str(year) + str(term))
    

    print("Please wait... Trying to get the information via Canvas API. This might take several minutes. Please do not shut off your computer!\n\nFeel free to go on a walk or grab some coffee while waiting :)\n\n")
    for course in courses:
        courseSession = course.course_code.split(" ")[-1]
        if (courseSession in selectedSessions):
            path = Path(f"./output/syllabi/{courseSession}/")
            if not path.exists():
                os.makedirs(f"./output/syllabi/{courseSession}/")

            noSyllabusPath = Path(f"./output/coursesWithNoSyllabus/{courseSession}.json")    
            if not noSyllabusPath.exists():
                with open(f"./output/coursesWithNoSyllabus/{courseSession}.json", "w+") as noSyllabusPathFile:
                    noSyllabusDict = {
                        f"{courseSession}": [],
                        "lastUpdatedSessionKey": sessionKey
                    }
            
                    json.dump(noSyllabusDict, noSyllabusPathFile, indent = 4)
                    noSyllabusPathFile.close()

            # If a file already exist, check if it was generated during this session or in a previous session
            else:
                with open(f"./output/coursesWithNoSyllabus/{courseSession}.json", "r") as noSyllabusPathFile:
                    noSyllabusDict = json.load(noSyllabusPathFile)
                    noSyllabusPathFile.close()

                if (noSyllabusDict["lastUpdatedSessionKey"] != sessionKey):
                    with open(f"./output/coursesWithNoSyllabus/{courseSession}.json", "w") as noSyllabusPathFile:
                        noSyllabusDict = {
                            f"{courseSession}": [],
                            "lastUpdatedSessionKey": sessionKey
                        }
                        json.dump(noSyllabusDict, noSyllabusPathFile, indent = 4)
                        noSyllabusPathFile.close()
            
            if not ("/" in course.course_code):
                try:
                    getSyllabusHTML(courseSession, course.course_code, course.id)
                except Exception as errorMessage:
                    print("Failed to get syllabus. Course code: " + course.course_code)
                    print("Error: " + str(errorMessage) + "\n")
    
    print("Done collecting syllabi!")

if (TOKEN == None or BASEURL == None):
    print("\nError: Missing .env variables!\n")
else:
    getSyllabi()