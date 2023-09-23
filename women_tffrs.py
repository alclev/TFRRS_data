import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import re

# Global variable
unit = None

def get_athlete_links(soup):
    """
    This function retrieves the links to the athlete profiles from a webpage.
    @return A list of links to athlete profiles.
    """
    base_url = "https://www.tfrrs.org/"
    div = soup.find_all('div', class_='col-lg-4')
    div = div[4]
    #extract the links from the div
    links = [a['href'] for a in div.find_all('a', href=True)]
    #join the base url to the links
    athletes = [urljoin(base_url, link) for link in links]
    return athletes

def get_athlete_data(link):
    """
    Retrieve data for an athlete.
    @return The athlete's data
    """
    base_dir = "Women's_TFRRS_Data"
    os.makedirs(base_dir, exist_ok=True)

    for athlete, events in athletes_data.items():
        athlete_dir = os.path.join(base_dir, athlete)
        os.makedirs(athlete_dir, exist_ok=True)

        for event, marks_dates in events.items():
            event_dir = os.path.join(athlete_dir, event)
            os.makedirs(event_dir, exist_ok=True)

            # Sort the list of tuples by date in ascending order
            marks_dates = sorted(marks_dates, key=lambda x: x[1])
            dates = [item[1] for item in marks_dates]
            marks = [item[0] for item in marks_dates]

            numeric_marks = [convert_mark(mark) for mark in marks]

            plt.figure(figsize=(10, 6))
            plt.plot(dates, numeric_marks, marker='o', label=event)
            plt.title(f'{athlete} {event} Performance')
            plt.xlabel('Date')
            plt.ylabel('Mark (meters)')
            plt.legend()
            plt.grid()

            # Rotate the date labels on the x-axis
            plt.xticks(rotation=45)
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %Y'))

            # Limit the number of x-axis ticks
            plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, prune='both'))

            output_file = os.path.join(event_dir, f'{event}_performance.png')
            plt.savefig(output_file, bbox_inches='tight')
            plt.close()

def interpret(athletes_data):
    """
    This code snippet defines a function called `RotationRetrieval` that takes two parameters: `cam_inputs` and `rotation_dictionary`. 
    """
    base_dir = "Women's_TFRRS_Data"
    os.makedirs(base_dir, exist_ok=True)

    for athlete, events in athletes_data.items():
        athlete_dir = os.path.join(base_dir, athlete)
        os.makedirs(athlete_dir, exist_ok=True)

        for event, marks_dates in events.items():
            dates = [item[1] for item in marks_dates]
            marks = [item[0] for item in marks_dates]
            # convert marks
            marks = [convert_mark(mark) for mark in marks]
            if(len(marks) <= 2):
                continue
            event_dir = os.path.join(athlete_dir, event)
            os.makedirs(event_dir, exist_ok=True)

            plt.figure(figsize=(12, 6))
            plt.plot_date(dates, marks, marker='o', linestyle='-', label=event)
            plt.title(f'{athlete} {event} Performance')
            plt.xlabel('Date')
            plt.ylabel(f'Mark ({unit})')
            plt.legend()
            plt.grid()
            plt.xticks(rotation=45)
            output_file = os.path.join(event_dir, f'{event}_performance.png')
            plt.savefig(output_file, bbox_inches='tight')
            plt.close()

def make_dirs(map):
    """
    Create directories if they do not already exist.
    @return None
    """
    # Specify the directory name
    base = "Men's_TFRRS_Data"
    os.mkdir(base)
    for athlete in map:
        os.mkdir(base + '/' + athlete)
        for event in map[athlete]:
            os.mkdir(base + '/' + athlete + '/' + event)

def convert_date(date):
    """
    Convert a date string to a different format.
    @param date - the date string to be converted
    @return The converted date string
    """
    month = date[:3]
    # get the day with regular expression
    pattern = r'\d+,'
    day = re.search(pattern, date).group(0)
    day = day[:-1]
    year = date[-4:]

    date_str = f'{month} {day}, {year}'
    date_format = '%b %d, %Y'
    date = datetime.datetime.strptime(date_str, date_format)
    return date

def convert_mark(mark):
    """
    Convert a mark to an understable metric.
    """
    global unit
    if(re.match(r'\d+.\d{2}m', mark)):
        unit = 'm'
        return float(mark[:-1])
    if(re.match(r'\d+:\d{2}.\d{1,2}', mark)):
        unit = 'min'
        minutes = int(mark[:mark.find(':')])
        seconds = float(mark[mark.find(':')+1:])
        return minutes + seconds/60.0
    if(re.match(r'\d{1,2}.\d{1,2}', mark)):
        unit = 's'
        return float(mark)

def load_file(file):
    """
    Load a file from the file system.
    @return The loaded file.
    """
    with open(file, 'r', newline='') as csvfile:
        data = list(csv.reader(csvfile))

        # Process the data
        athletes_data = {}
        for row in data[1:]:  # Skip the header row
            athlete, event, mark, date_str = row
            date = date_str
            if athlete not in athletes_data:
                athletes_data[athlete] = {}
            if event not in athletes_data[athlete]:
                athletes_data[athlete][event] = []

            date = convert_date(date)
            if mark == 'DNF' or mark == 'DQ' or mark == 'DNS' or mark == 'NM' or mark == 'NH' or mark == 'FOUL':
                continue

            athletes_data[athlete][event].append([mark, date])

    return athletes_data

                    
def write_to_csv(map):
    """
    Write a list of data to a CSV file.
    @param data - the list of data to write
    @param filename - the name of the CSV file to write to
    @return None
    """
    with open("female_lehigh_athletes.csv", "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        csv_writer.writerow(['Athlete', 'Event', 'Mark', 'Date'])
        for athlete in map:
            for event in map[athlete]:
                for mark in map[athlete][event]:
                    csv_writer.writerow([athlete, event, mark[0], mark[1]])
def scrape():
    """
    Scrape the data from the website.
    """
    print("Scraping...")
    response = requests.get("https://www.tfrrs.org/teams/tf/PA_college_f_Lehigh.html")
    soup = BeautifulSoup(response.content, 'html.parser')
    map = {}
    athlete_links = get_athlete_links(soup)
    for link in athlete_links:
        # get the athlete name
        name = link[link.rfind('/') + 1:link.rfind('.')]
        name = name.replace('_', ' ')
        map[name] = get_athlete_data(link)
    print("Finished!")

def main():
    """
    The main function is the entry point of the program. It is where the execution of the program starts.
    """
    scrape()
    map = load_file("female_lehigh_athletes.csv")
    interpret(map)
    
if __name__ == '__main__':
    main()
