# TFRRS Data Scraper for Lehigh University Track & Field

![Lehigh Track & Field](lehigh_track_field_image.png)

## Overview

Welcome to the TFRRS Data Scraper project for Lehigh University Track & Field! This Python program is designed to scrape raw data from [TFRRS.org](https://www.tfrrs.org) regarding track and field performance metrics of Lehigh University's track team. It then organizes this data by creating a folder hierarchy where each athlete has their own directory. The collected data is used to generate performance graphs over time for each athlete's events.

### Prerequisites

- Python 3.x installed on your system.
- Basic knowledge of Python and web scraping.

### Installation

1. Clone this repository to your local machine:

   ```shell
   git clone https://github.com/yourusername/tfrrs-scraper-lehigh.git
Navigate to the project directory:
    cd tfrrs-scraper-lehigh
Install the required Python libraries:
    pip install -r requirements.txt
```
### Usage
To use the TFRRS Data Scraper, follow these steps:

Configure the scraper with the desired settings in config.py.

Run the scraper:

```shell
python scraper.py
The program will start scraping data from TFRRS.org and organize it in athlete-specific directories.
```
Once the scraping is complete, use the data for analysis or generate performance graphs using your preferred data visualization tools.

### Folder Hierarchy
The data collected by the scraper is organized in the following folder hierarchy:

tfrrs-scraper-lehigh/
│
├── data/
│   ├── athlete1/
│   │   ├── event1.csv
│   │   ├── event2.csv
│   │   └── ...
│   ├── athlete2/
│   │   ├── event1.csv
│   │   ├── event2.csv
│   │   └── ...
│   ├── ...
│
└── ...
Each athlete's data is stored in a separate directory under the data folder, with individual CSV files for each event they have participated in.

### Contributions
Contributions to this project are welcome. If you'd like to contribute:

Fork the repository.
Create a feature branch.
Make your changes and document them.
Test your changes thoroughly.
Submit a pull request for review.


### Contact
If you have any questions, suggestions, or issues regarding the TFRRS Data Scraper for Lehigh University Track & Field project, please feel free to contact the author:

Author: Alex Clevenger
Email: alexbclevenger@gmail.com 
GitHub: https://github.com/alclev
Thank you for using the TFRRS Data Scraper for your track and field performance analysis needs!