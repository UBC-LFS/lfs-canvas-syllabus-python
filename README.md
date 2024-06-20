# LFS-Canva-Syllabus (with Python)
This application extracts syllabi from Canvas, downloads them, and adds it to an index.html file

## Prerequisites
1. **Install [Python 3.7 or greater](https://www.python.org/downloads/)**.
2. **Install [Git](https://git-scm.com/downloads)**.

## Installing and Setup
1. First, clone this repo. `git clone https://github.com/UBC-LFS/lfs-canvas-syllabus-python.git`

## Setting up
```
$ pip install virtualenv
$ python -m venv venv
```

On Windows
```
$ venv\Scripts\activate
```

On Linux
```
$ source venv\bin\activate
```

```
$ pip install -r requirements.txt
```

## Create a `.env` file. 
This is where you'll specify the URL and token as show below. Don't add quotes. You can swap out the domain if you want to run it off production. 

```
CANVAS_PROD_URL='https://[YOUR_URL].instructure.com'
CANVAS_TEST_URL='https://[YOUR_TEST_URL].instructure.com'
CANVAS_API_TOKEN=''
API_VERSION = 'api/v1'
```


## Gathering syllabus
0. Rename **syllabi_example** to **syllabi**
1. Run this application: 

```
python main.py
```

2. Input the year you are interested in (if you are interested in more than one year, you'll need to run the script more than one time).
3. Select the terms you are interested in. You can select multiple terms by pressing space. If you want to select all the terms, leave the default selection of 'All'.
4. Input the account number of your Faculty. For LFS, it's 1122 (old one 15).
5. Wait for the script to gather the syllabuses. Depending on how many terms you select and how many courses there are, this could take some time.
6. The syllabuses are now downloaded in `syllabi`, inside folders that indicate what year/term the course was offered.
7. The name of the courses without a syllabus will be added `output/coursesWithNoSyllabus/{session}`

Thank you!