# Toll fee calculator

## Overview

A toll fee calculator CLI, supply a CSV file for a certain day the CLI will calculate the total daily toll for that vehicle.

## Task

Since the objective was very open and missed alot of requirements I made the decision to create something "real", a CLI which can together with csv file calculate a total tax for a certain day.

## Usage

"python main.py /PATH/TO/CLI"

## Requirements

- Python 3.7+
- Pipenv https://pipenv.readthedocs.io
- Linux (Developed on Ubuntu 18.04)

## Test

Test are written for Pytest, https://pytest.org  
You should be able to run the tests via "pytest /PATH/TO/test/" from anywhere but it has mostly been tested from the project folder  
from project root, run "pytest test"

## Step by step usage/test instructions

Make sure you have Python 3.7+ and Pipenv installed  
naviate to the project folder  
"pipenv install --d" to install developmen requirements (pytest basicly)  
"pipenv shell" to activate the shell  
"python src/main.py /PATH/TO/CSV" to calculate a toll  
("python src/main.py test_csvs/abc123-regular.csv") for a test file  
"pytest test" to run tests

## CSV Format

licence_plate,date_of_pass  
str, YYYY-mm-dd HH:MM:SS

## Based on these requirements:

Fees will differ between 9 SEK and 22 SEK, depending on the time of day.  
The maximum fee for one day is 60 SEK.  
Only the highest fee should be charged for multiple passages within a 60 minute period.  
Some vehicle types are fee-free.  
Fee-free days are; Saturdays, Sundays, holidays and day before holidays and the whole month of July. See Transportstyrelsen for details.
