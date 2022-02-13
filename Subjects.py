from bs4 import BeautifulSoup
from SubjectPages import subject_pages
import os
import json


def remove_empty_lines(self):
    new_string_array = []
    for line in self:
        line = str(line)
        if str.isspace(line) or line == '':
            continue
        else:
            new_string_array.append(line)
    return new_string_array


def parseSubjectPage(page_key):
    soup = BeautifulSoup(Pages[page_key], 'lxml')
    resultsContainer = soup.find('div', class_ = 'span12')
    CourseNames = resultsContainer.find_all('h4')
    # [print(courseName.text) for courseName in CourseNames]

    if len(CourseNames) > 0:
        print('\tFound [{}] Courses in [{}]'.format(len(CourseNames), page_key))
    else:
        print(f'\tCould not locate any courses in [{page_key}]\n')
        investigate_subjects.append(page_key)
        return

    Courses = []

    course_tracker = 0
    for courseName in CourseNames:
        course_tracker += 1
        print('\t\tCollecting Data for course [{}]: [{}]...'.format(course_tracker, courseName.text))

        name = courseName.text
        print('\t\t\tFound Name: [{}]'.format(name))

        DescriptionElement = courseName.next_sibling.next_sibling
        descriptionText = remove_empty_lines(
            str.splitlines(str.replace(str(DescriptionElement.text), 'Course Description: ', '')))
        print('\t\t\tFound course description: {}'.format(descriptionText))

        Components = []
        ComponentsTableElement = DescriptionElement.next_sibling.next_sibling.find('tbody')
        componentElements = ComponentsTableElement.find_all('tr', recursive = False)
        if len(componentElements) > 0:
            print('\t\t\tFound [{}] components in course'.format(len(componentElements)))

            component_tracker = 0
            for component in componentElements:
                component_tracker += 1
                print('\t\t\t\tAnalyzing component [{}]'.format(component_tracker))

                componentDataElements = component.find_all('td', recursive = False)
                print('\t\t\t\tFound component data')

                section = componentDataElements[0]
                componentType = componentDataElements[1]
                componentNbr = componentDataElements[2]

                daysTableElement = componentDataElements[3]
                daysElements = daysTableElement.find_all('td')
                daysAvailable = []
                for day in daysElements:
                    if not str.isspace(str(day.text)):
                        daysAvailable.append(str(day.text))

                startTime = componentDataElements[4]
                endTime = componentDataElements[5]

                location = componentDataElements[6]
                instructor = componentDataElements[7]

                Notes = remove_empty_lines(str.splitlines(str.strip(str(componentDataElements[8].text))))

                status = componentDataElements[9]
                campus = componentDataElements[10]
                delivery = componentDataElements[11]

                Component = {
                    'Section': str.strip(section.string),
                    'Component': str.strip(componentType.string),
                    'Class Nbr': str.strip(componentNbr.string),
                    'Days': daysAvailable,
                    'Start Time': startTime.string if startTime.string != None else '',
                    'End Time': endTime.string if endTime.string != None else '',
                    'Location': str.strip(location.string),
                    'Instructor': str.strip(instructor.string) if instructor.string != None else '',
                    'Notes': Notes,
                    'Status': str.strip(status.string),
                    'Campus': str.strip(campus.string),
                    'Delivery': str.strip(delivery.string)
                }
                print('\t\t\t\tComponent data assembled'.format(Component))
                Components.append(Component)

        else:
            print('\t\t\tNo course components found in course'.format(len(componentElements)))
            try:
                investigate_subjects.index(page_key)
            except:
                investigate_subjects.append(page_key)

        course = {
            'Name': name,
            'Description': descriptionText,
            'Components': Components
        }
        print('\t\tCourse data assembled')
        print('\t\tFinished Extracting data for course [{}]\n'.format(course['Name']))
        Courses.append(course)

    return Courses


def Subjects_to_JSON(Subjects):
    if not os.path.exists(os.path.join(os.getcwd(), 'Subjects/SubjectsJSON')):
        os.mkdir(os.path.join(os.getcwd(), 'Subjects/SubjectsJSON'))
    print('\nSaving all subjects locally...')

    # saves a whole copy of subject data
    with open('Subjects/subjects.json', 'w') as file:
        json.dump(Subjects, file, indent = 2)

    # saves individual copies of subject data
    for subject in Subjects:
        code = subject['Code']
        with open(f'Subjects/SubjectsJSON/{code}.json', 'w') as file:
            json.dump(subject, file, indent = 2)
            print(f'\tSubject [{code}] saved!')

    print('\nAll subjects saved!')


def update_subjects():
    global Pages
    Pages = subject_pages()

    with open('Subjects/subject-codes.json') as file:
        data = json.load(file)
        Subjects = data

    print('\n----Starting to parse all subject pages...----')
    subject_counter = 0
    for key in Pages:
        subject_counter += 1
        print(f'\n[{subject_counter}] Searching subject [{key}]')
        subject_courses = parseSubjectPage(key)
        print('Collected all course data in subject [{}]: [{}]'.format(subject_counter, key))
        Subjects[subject_counter - 1].update({ 'Courses': subject_courses })

    print('\n----Finished parsing all subject pages!----')

    Subjects_to_JSON(Subjects)

    print(f'\nList of subjects to investigate: [{len(investigate_subjects)}]')
    print(investigate_subjects)


def retrieve_subjectsJSON(subject_codes = []):
    dir_path = 'Subjects/SubjectsJSON'

    if not os.path.exists(dir_path):
        print('Could not locate subject JSON data directory, try running update_subjects()')
        return

    main_dir = os.getcwd()
    os.chdir(dir_path)
    subjectJSONs = os.listdir()

    Subjects = {}
    for subjectJSON in subjectJSONs:
        with open(f'{subjectJSON}') as file:
            file_code = os.path.splitext(subjectJSON)[0]
            content = json.load(file)
        Subjects.update({file_code: content})

    if type(subject_codes) is not list:
        raise TypeError(f'Could not process paramater of type "{type(subject_codes)}", retry by sending a list')
        return

    if len(subject_codes) == 0:
        return Subjects
    else:
        send_Subjects = {}
        for code in subject_codes:
            try:
                send_Subjects.update({code: Subjects[code]})
                print(f'Located JSON for [{code}]')
            except:
                print(f'Invalid code {code}, could not find corresponding JSON')
        return send_Subjects

global investigate_subjects
investigate_subjects = []

# Runtime code ---------
update_subjects()                 #Update/make json directories of all subjects