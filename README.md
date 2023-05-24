# LFS-Canva-Syllabus (with Python)
This application extracts syllabi from Canvas and saves it as an index.html file

## Prerequisites
1. **Install [Python 3.7 or greater](https://www.python.org/downloads/)**.
2. **Install [Git](https://git-scm.com/downloads)**.

## Installing and Setup
1. First, clone this repo. `git clone https://github.com/UBC-LFS/lfs-canvas-syllabus-python.git`

## Setting up
```
pip install virtualenv
virtualenv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file. 
This is where you'll specify the URL and token as show below. Don't add quotes. You can swap out the domain if you want to run it off production. 
```
CANVAS_API_TOKEN=PLACE YOUR TOKEN HERE
CANVAS_API_DOMAIN=https://ubc.beta.instructure.com/api/v1
```

Run `getSyllabi.py`