# Mad Sudoku

## About

Sudoku games with with new challenges available daily (in the future). Solve the challenges fast and compete with other users on who can solve the challenges fastest.

## Features
- A Sudoku game with different difficulty levels and new challenge available daily
- View the Top 5 fastest users who have solved the challenges
- Sign-up and play as your chosen username or just play as an anonymous Guest

## Software Requirements
Stack: Flask, SQLite, JQuery, Bootstrap 3

Browsers: Google Chrome, Mozilla Firefox, Microsoft Edge, Apple Safari

## Setup
1. Download the repository files and unzip
2. Open terminal/command line and change directory to repository directory
3. Run "source venv/bin/activate" to activate python virtual environment
4. Install all libraries and dependencies using the command "pip install -r requirements.txt"
5. Run the game server using the command "python3 mad_sudoku.py"
6. Open the address http://localhost:5000 in your web browser

## Test Setup
For unit test, the test files are those files with the *_case.py prefix which can be found under the /app folder.
### Unit Test
1. Install coverage module using the command "pip install coverage"
2. Run the command "coverage run --source=./app  -m unittest discover -p *case.py"
3. Show the report via the command "coverage report"
4. Show more detailed report on browser via the command "coverage html" and open the html file.

### API Test
1. Install Postman
2. Import test collection using the link below
https://go.postman.co/workspace/UWA_AgileWebProject2~9248e373-d242-43d7-ab5d-b71d208844f0/collection/2629920-15d4ecf7-4451-4055-ac8b-71e24a407fda?action=share&creator=2629920
3. Import test environment using the link below:
https://go.postman.co/workspace/UWA_AgileWebProject2~9248e373-d242-43d7-ab5d-b71d208844f0/environment/2629920-b45416b6-dd00-42da-b06b-98120b472a25
4. Run MadSudoku.
5. Click on "..." button on the right side of collection "mad_sudoku"
6. Click the blue "Run collection" and "Run mad_sudoku" button on the right side.

## Collaborators

|Student Number|Name|
|:--|:--|
|23020648|Akmal Fadlurohman|
|22948007|Changdae Jung|
