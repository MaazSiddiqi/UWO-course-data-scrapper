# UWO-course-data-scrapper
Built in Python, uses Requests library to send HTTP requests to Uwo's timetable builder with form data for various faculty and extracts output from HTML and organizes it into a convenient JSON object currently stored in a subdirectory.


How-to-use
Two main scripts: SubjectPages.py and Subjects.py

SubjectPages.py:
    Uses 'requests' and 'bs4' to access HTML pages of uwo timetables from 'uwo.draftmyschedule.ca' database (ttindex.cfm ; found this through some inspect element magic) 
    Once pages are accessed, will write the bytes of (essentially downloads) each page and saves them in 'Subjects/SubjectsHTML' folder
    If you want to update any of the locally downloaded pages, just delete them and run SubjectPages.py again and it will replace it with the new latest page
    Similarly, you can delete all the pages or the whole 'SubjectsHTML' directory to redownload ALL the pages

    main function: subject_pages(url, local_dir_name)    **dont change the parameter names, they are default set. 

Subjects.py:
    Uses 'bs4' and 'lmxl' to read and parse each subject's HTML page into an organized json file
    Running script makes a universal json named 'subjects.json' which contains ALL subject data in ONE giant json object in the main project directory (outside of 'Subjects' directory)
    Script also makes an individualized json object for each subject found in 'Subjects/SubjectsJSON' directory (makes for easier accessiblity if you only want to work with certain subjects, not the whole database)
    Also creates a subject-codes.json in the main directory if you need that information (its used in the scripts but it could be useful for other projects)

    main function: update_subjects()
