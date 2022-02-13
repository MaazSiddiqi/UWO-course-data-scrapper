import requests
from bs4 import BeautifulSoup
import time
import datetime
import random
import os
import json


def setup_dir(dir_name):
    dir_path = os.path.join(main_dir, local_dir_name, 'SubjectsHTML')

    if not os.path.exists(dir_path):
        print('Could not locate data directory, creating one now...\n')
        os.makedirs(dir_path)

    print('Located subject data directory\n')
    return dir_path


def fetch_site(s, url, form_data = None):
    if form_data is None:
        print(f'Fetching site [{url}]...')
        source = s.get(url).text
    else:
        print(f'Fetching data from [{url}]...')
        source = s.post(url, data = form_data).text
    soup = BeautifulSoup(source, 'lxml')
    return soup


def get_subject_codes():
    print('Retrieving saved subject codes...')
    if not os.path.exists(os.path.join(os.path.dirname(os.getcwd()), 'subject-codes.json')):
        print('Could not find subject codes. Attempting download:\n')
        return download_subject_codes()
    else:
        with open(os.path.join(os.path.dirname(os.getcwd()), 'subject-codes.json'), 'r') as file:
            return json.load(file)


def download_subject_codes():
    print('Downloading subject codes...')

    soup = fetch_site(s, url)

    print('Locating subjects \n')
    subject_input = soup.find('select', id = 'inputSubject')
    subject_options = subject_input.find_all('option', recursive = False)

    Subjects = {}

    for option in subject_options:
        if option['value'] == '':
            continue

        subject = {
            'Name': str.strip(str(option.string)),
            'Code': option['value'],
            # 'Courses': []
        }

        Subjects.append(subject)
        print('Found subject: [{}]'.format(subject['Code']))

        # Subjects.update({option['value'], str.strip(str(option.string))})

    print(f'\nIdentified [{len(Subjects)}] Subject Codes\n')

    print('Saving codes locally...')
    with open(os.path.join(os.path.dirname(os.getcwd()), 'subject-codes.json'), 'w') as file:
        json.dump(Subjects, file, indent = 2)
        print('Codes Saved! \n')

    return Subjects


def get_subject_pages(subjects = None):
    print('Retrieving pages for each subject...\n')
    if subjects is None:
        print('No subjects sent to retrieve')
        return None

    global total_stall_time
    global captcha_hit_count
    global subject_counter
    global download_counter

    Pages = { }
    saved_codes = [(os.path.splitext(os.path.basename(page))[0].replace('[', '').replace(']', '')) for page in
                   os.listdir()]
    for subject in subjects:
        subject_counter += 1
        print('\n[{}] Retrieving page for [{}]...'.format(subject_counter, subject['Code']))
        try:
            if saved_codes.index(subject['Code']) > -1:
                print('Found saved page for [{}]'.format(subject['Code']))
                with open('[{}].html'.format(subject['Code'], 'r')) as file:
                    page = file.read()
                    Pages.update({ f'{subject["Code"]}': page })
        except:
            print('No saved page for [{}] found, downloading page now...'.format(subject['Code']))
            download_counter += 1
            stall_length = random.randrange(1, 3)
            print(f'(Stalling for {stall_length}s to avoid captcha)')
            total_stall_time += stall_length
            time.sleep(stall_length)

            page = download_page(subject)
            Pages.update({ f'{subject["Code"]}': page })

    return Pages


def download_page(subject):
    form_params = {
        'subject': '',
        'Designation': 'Any',
        'CourseTime': 'All',
        'Component': 'All',
        'time': '',
        'end_time': '',
        'day': ['m', 'tu', 'w', 'th', 'f'],
        'LocationCode': 'Any',
        'command': 'search'
    }

    form_params['subject'] = subject['Code']

    global total_stall_time
    global captcha_hit_count

    page_downloaded = False
    captcha_retry_count = 0
    max_captcha_retry_attempts = 5
    while not page_downloaded:
        print('Attempting to retrieve page for subject [{}]...'.format(subject['Code']))
        content = fetch_site(s, url, form_params)

        if 'captcha' in str(content):
            stall_length = random.randrange(25, 35)
            print(f'Ran into captcha, stalling for {stall_length} seconds')
            captcha_hit_count += 1
            total_stall_time += stall_length
            time.sleep(stall_length)
            if captcha_retry_count <= max_captcha_retry_attempts:
                captcha_retry_count += 1
                print(f'Retrying (Attempt: {captcha_retry_count})..')
                continue
            else:
                raise TypeError(f'Could not get through captcha after {captcha_retry_count} attempts.')
        else:
            print('Found page for [{}]. Saving page to directory...'.format(subject['Code']))

            with open('[{}].html'.format(subject['Code']), 'w') as file:
                file.write(str(content))
                print('Page Saved!\n')
                page_downloaded = True
                return str(file)


def captcha_test(url):
    attemptNbr = 0
    subject_code = 'CA'
    form_params = {
        'subject': subject_code,
        'Designation': 'Any',
        'CourseTime': 'All',
        'Component': 'All',
        'time': '',
        'end_time': '',
        'day': ['m', 'tu', 'w', 'th', 'f'],
        'LocationCode': 'Any',
        'command': 'search'
    }

    s = requests.session()

    captcha_count = 0
    while True:
        attemptNbr += 1
        if attemptNbr % 8 == 0:
            print('\nCooling down requests for 5 seconds\n')
            time.sleep(5)
        source = s.post(url, data = form_params).text
        soup = BeautifulSoup(source, 'lxml')

        if 'captcha' in str(soup):
            captcha_count += 1
            print(f'Hit captcha {captcha_count} on attempt [{attemptNbr}]')

            if captcha_count <= 5:
                print('Stalling for 32 seconds to reset captcha...')
                time.sleep(32)
                print('Restarting captcha test\n')
                attemptNbr = 0
                continue
            else:
                break

    print('Ended captcha test')


def subject_pages(given_url = None, dir_name = None, test_partition_length = -1):
    print('Initiating Session...')
    global s
    s = requests.session()

    global url
    url = given_url if given_url is not None else default_url

    global local_dir_name
    local_dir_name = dir_name if dir_name is not None else default_local_dir_name

    basepath = os.getcwd()
    dir_path = setup_dir(local_dir_name)
    os.chdir(dir_path)


    Subjects = get_subject_codes()
    print(f'Found [{len(Subjects)}] subject codes\n')

    test_partition_length = test_partition_length if test_partition_length <= len(Subjects) else len(Subjects)
    Pages = get_subject_pages((Subjects[:test_partition_length] if test_partition_length != -1 else Subjects))

    os.chdir(basepath)
    s.close()

    print('\nFinished gathering pages!\n')
    run_summary()
    return Pages


def run_summary():
    global total_stall_time
    global captcha_hit_count
    global subject_counter
    global download_counter
    global start_time

    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    pure_runtime = elapsed_time.total_seconds() - total_stall_time
    average_download_time = (elapsed_time.total_seconds() / download_counter) if download_counter != 0 else 0
    print('----------- <SUMMARY> -----------')
    print(f'[Pages Retrieved: {subject_counter}, Download Count: {download_counter}]')
    print(f'[Catpchas Hit: {captcha_hit_count}, Stall Time: {total_stall_time}s]')
    print(f'[Time Elapsed: {elapsed_time}, Pure Runtime: {pure_runtime}s]')
    print(f'[Average Download Time: {average_download_time}s]')
    print('----------- </SUMMARY> ----------')

# Tracker variables [Don't change]
total_stall_time = 0
captcha_hit_count = 0
subject_counter = 0
download_counter = 0
main_dir = os.getcwd()
start_time = datetime.datetime.now()
default_url = 'https://studentservices.uwo.ca/secure/timetables/mastertt/ttindex.cfm'
default_local_dir_name = 'Subjects'

# User variables
url = 'https://studentservices.uwo.ca/secure/timetables/mastertt/ttindex.cfm'
local_dir_name = 'Subjects'
amount_to_retrieve = 150  # omit from function call for all

# Runtime code ---------
# subject_pages(url, local_dir_name)            #Download all subject page data, skip if saved page already found/downloaded in 'Subjects/SubjectsHTML'
