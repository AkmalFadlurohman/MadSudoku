# Mad Sudoku

## About

Sudoku games with with new challenges available daily (in the future). Solve the challenges fast and compete with other users on who can solve the challenges fastest.

## Features
- A Sudoku game with different difficulty levels and new challenge available daily
- View the Top 5 fastest users who have solved the challenges
- Sign-up and create a new account to play or just play as an anonymous Guest

## Software Requirements
Stack: Flask, SQLite, JQuery, Bootstrap

Browsers: Google Chrome, Mozilla Firefox, Microsoft Edge, Safari

## Setup
1. Download the repository files and unzip
2. Open terminal/command line and change directory to repository directory
3. Run "source venv/bin/activate" to activate python virtual environment
4. Install all libraries and dependencies using the command "pip install -r requirements.txt"
5. Run the game server using the command "python3 mad_sudoku.py"
6. Open the address http://localhost:5000 in your web browser

## Test Setup
# unit test
1. install coverage module using the command "pip install coverage"
2. run the command "coverage run --source=./app  -m unittest discover -p *case.py"
3. show the report via the command "coverage report"
4. show more detailed report on browser via the command "coverage html" and open the html file.
# api test
for api test, we used "postman".
1. install postman
2. import collection with a link below 
https://go.postman.co/workspace/UWA_AgileWebProject2~9248e373-d242-43d7-ab5d-b71d208844f0/collection/2629920-15d4ecf7-4451-4055-ac8b-71e24a407fda?action=share&creator=2629920
3. import environment with a link below:
https://go.postman.co/workspace/UWA_AgileWebProject2~9248e373-d242-43d7-ab5d-b71d208844f0/environment/2629920-b45416b6-dd00-42da-b06b-98120b472a25
4. run MadSudoku.
5. click on "..." button on the right side of collection "mad_sudoku"
6. click run "Run collection" and "Run mad_sudoku" blue button on the right side.

## Collaborators

|Student Number|Name|
|:--|:--|
|23020648|Akmal Fadlurohman|
|22948007|Changdae Jung|
