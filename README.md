# LoL Esports drop collector
This script runs streams with drops enabled in the background until there is none live.

## Getting Started
### Requirements:
- Python 3
- Selenium (`pip install selenium`)
- dotenv (`pip install python-dotenv`)
- FireFox WebDriver (can be changed to chromedriver manually)
- Credentials stored in dotenv file

## Running the script
- Run `python dropcollector.py` or open the run.bat file. A new Firefox window be opened.
- Do whatever you want, the script will run until there are no streams live that have drops enabled.
- once finished it will print a message saying so.
