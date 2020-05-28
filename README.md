# Scraping Indeed with Selenium

## 1 Intro:
In this repo you will learn how to make a basic scrape in Indeed using Selenium

## 2 Goals:
The goal of the project is to automate your job seek and display the jobs you are interested in a csv file

## 3 Steps:
- Install Selenium and the Chrome WebDriver
- Import libraries
- Change the variables

## 4 Final Output:
The final output is a csv file with the links to the jobs you are interested in, the tittle of the job, the company offering it, the number of days since the release and the condition/s you require

## How it works:
- Install Selenium --> https://pypi.org/project/selenium/
- Install Chrome WebDriver --> https://www.liquidweb.com/kb/how-to-install-selenium-tools-on-ubuntu-18-04/
- Go to indeed.py
- Type the indeed domain of you country --> variable "url"
- Type the job you are looking for and the location --> variable "keyword"
- Change "días" to "days" or the translation in your language --> variable "release_date"
- Type your condition --> variable "condition"
