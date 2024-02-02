# LFS-Canva-Syllabus (with Python)
This application extracts syllabi from Canvas, downloads them, and adds it to an index.html file

## Prerequisites
1. **Install [Python 3.7 or greater](https://www.python.org/downloads/)**.
2. **Install [Git](https://git-scm.com/downloads)**.

## Installing and Setup
1. First, clone this repo. `git clone https://github.com/UBC-LFS/lfs-canvas-syllabus-python.git`

## Setting up
```
pip install virtualenv
virtualenv venv
```

On Windows
```
venv\Scripts\activate
```

On Linux
```
source venv\bin\activate
```

```
pip install -r requirements.txt
```

Create a `.env` file. 
This is where you'll specify the URL and token as show below. Don't add quotes. You can swap out the domain if you want to run it off production. 

```
CANVAS_API_TOKEN=PLACE YOUR TOKEN HERE
CANVAS_API_DOMAIN=https://ubc.beta.instructure.com
```


## Gathering syllabus
1. Run `getSyllabi.py`: 
```
python getSyllabi.py
```
2. Input the year you are interested in (if you are interested in more than one year, you'll need to run the script more than one time).
3. Select the terms you are interested in. You can select multiple terms by pressing space. If you want to select all the terms, leave the default selection of 'All'.
4. Input the account number of your Faculty. For LFS, it's 15.
5. Wait for the script to gather the syllabuses. Depending on how many terms you select and how many courses there are, this could take some time.
6. The syllabuses are now downloaded in `output/syllabi`, inside folders that indicate what year/term the course was offered.
7. The name of the courses without a syllabus will be added `output/coursesWithNoSyllabus/{session}`
    - Do not worry what `lastUpdatedSessionKey` is. This is just so the script can determine if the file was created in the past, or when it just ran.
8. **Note:** If you encounter "`Error: list index out of range`", it most likely means that the syllabus does not exist on Canva or it's due to some permission errors.
