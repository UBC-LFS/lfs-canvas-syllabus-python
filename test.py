import re
import requests

# syllabusHTML = "https://ubc.instructure.com/courses/73196/files/14765297/download?verifier=LYrtkjKfZVYB6Tp0B7Xw0rR60BxsMSXQOSjkX4qu&wrap=1 JDJDJD JDJDJ"
# # autoDownloadableSyllabus = re.findall(r"https://ubc.instructure.com/courses/[\d]+/files/[\d]+/download\W?verifier=\w*", syllabusHTML)

# # test = "hi/222hii122"
# # sss = re.findall(r"hi/[\d]+hii[\d]+", test)
# r = requests.get(syllabusHTML, allow_redirects=True)
# filename = re.findall("filename=(.+)", r.headers['content-disposition'])[0].replace("\"", "")
# open(f"./{filename}", 'wb').write(r.content)
# # print(autoDownloadableSyllabus)
# # print(sss)


# html = """
# <p><a class="instructure_file_link instructure_scribd_file" title="APBI 496 Course Syllabus - UBC LFS - version Nov 2020.pdf" href="https://ubc.instructure.com/courses/73196/files/14765297/download?verifier=LYrtkjKfZVYB6Tp0B7Xw0rR60BxsMSXQOSjkX4qu&amp;wrap=1" data-api-endpoint="https://ubc.instructure.com/api/v1/courses/73196/files/14765297" data-api-returntype="File">APBI 496 Course Syllabus - UBC LFS - version Nov 2020.pdf</a></p>
# <p>This practicum is designed for students to gain experience in potential fields of future<br>employment working with animals. Students will apply knowledge from previous coursework in<br>Applied Animal Biology to careers in wildlife rehabilitation, animal shelter management,<br>research and farm animal management.&nbsp;</p>
# <p>Learning Outcomes:<br>By the end of the course, students will be able to:<br>1. Apply key principles and concepts of Applied Animal Biology to the professions of<br>wildlife rehabilitation, animal shelter management, research animal management and<br>farm management;<br>2. Understand the professional field in which the practicum takes place, including its<br>governance, operations and standards of performance;<br>3. Relate animal welfare and animal management to practical situations in animal care and<br>human-animal interactions;<br>4. Recognize and discuss the complex ethical issues within the practicum field;<br>5. Create an applied communications piece for use at the field location; and,<br>6. Summarize and communicate experiential learning.</p>
# """

# html = html.replace("<p>", "<a>")
# print(html)

html="href='https://ubc.instructure.com/courses/73196/files/14765297/download?verifier=LYrtkjKfZVYB6Tp0B7Xw0rR60BxsMSXQOSjkX4qu&amp;wrap=1' data-api-endpoint='https://ubc.instructure.com/api/v1/courses/73196/files/14765297'"
autoDownloadableSyllabus = re.findall(r"https://ubc.instructure.com/courses/[\d]+/files/[\d]+/download\W?verifier=[\S]*", html)
print(autoDownloadableSyllabus)