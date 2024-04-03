# UWO Course Data Scraper

## Description

UWO Course Data Scraper is a Python-based web scraper designed to retrieve course data from the University of Western Ontario's timetable builder. It utilizes the Requests library to send HTTP requests, BeautifulSoup for HTML parsing, and JSON for data storage.

## Features

- **SubjectPages.py**: Fetches HTML pages of UWO timetables, stores them locally, and handles captcha challenges.
- **Subjects.py**: Parses HTML pages into organized JSON files containing course data.

## How to Use

### Setup

1. Clone the repository.
2. Ensure you have Python installed.
3. Install the required dependencies using `pip install -r requirements.txt`.

### Running the Scripts

1. **SubjectPages.py**:
   - Run `python SubjectPages.py` to fetch HTML pages of UWO timetables.
   - Optionally, customize the script's parameters.
2. **Subjects.py**:
   - Run `python Subjects.py` to parse HTML pages into JSON files.
   - Ensure you have the required HTML pages stored locally.

## Scripts Overview

### SubjectPages.py

- **Setup Directory**: Creates a directory for storing HTML pages if not already present.
- **Fetch Site**: Retrieves HTML content from the provided URL or through a POST request with form data.
- **Get Subject Codes**: Retrieves and saves subject codes locally.
- **Download Subject Codes**: Downloads subject codes from the website.
- **Get Subject Pages**: Retrieves and stores HTML pages for each subject.
- **Download Page**: Downloads a specific subject's HTML page.
- **Captcha Test**: Tests for captcha challenges and retries if encountered.
- **Subject Pages**: Initiates the session and retrieves subject pages.

### Subjects.py

- **Remove Empty Lines**: Utility function to remove empty lines from a string.
- **Parse Subject Page**: Parses HTML content of a subject page into JSON format.
- **Subjects to JSON**: Saves subject data in JSON format.
- **Update Subjects**: Updates or creates JSON directories for all subjects.
- **Retrieve Subjects JSON**: Retrieves JSON data for specified subject codes.

## File Structure

- **SubjectPages.py**: Contains functions to fetch HTML pages of UWO timetables.
- **Subjects.py**: Contains functions to parse HTML pages into organized JSON files.
- **subject-codes.json**: Contains subject codes for reference.
- **Subjects/SubjectsHTML**: Directory to store downloaded HTML pages.
- **Subjects/SubjectsJSON**: Directory to store JSON files for each subject.
