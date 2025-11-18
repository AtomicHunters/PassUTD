# PassUTD - Secure password Manager
This app is a work in progress and is currently incomplete.

## Requirements
- Python 3.x
- Flask library `pip install flask`
- docker desktop (for Windows based systems)
- mySQL version 8

## How to Run
1. Run app.py `python app.py`
2. Open local host in a web browser `http://localhost:5000/`

## Database Setup
DO THE FOLLOWING IN POWERSHELL:

````````````````````````````````````````````````````````
CHANGE WORKING DIRECTORY TO PASSUTD GITHUB DIRECTORY (after pulling database)

cd $env:HOMEPATH\Documents\GitHub\PassUTD
````````````````````````````````````````````````````````
TO CREATE AND RUN DOCKER THE FIRST TIME:

docker compose up --build -d
````````````````````````````````````````````````````````
TO CREATE AND RUN DOCKER AFTERWARDS

docker compose up -d
````````````````````````````````````````````````````````
CONNNECT TO THE SERVER
mysql -h 127.0.0.1 -P 3307 -u root -p --execute="source Database Script.sql"
////3307 may be changed to another port if you've decided to use something else
////Database script path is the relative path from
```````````````````````````````````````````````````````
