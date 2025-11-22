# PassUTD - Secure password Manager
This app is a work in progress and is currently incomplete.

## Requirements
- Python 3.x
- Flask library `pip install flask`
- Flask DB Library `pip install flask_mysqldb`
- Dotenv `pip install dotenv`
- Docker Desktop
- mySQL version 8

## How to Run
1. Open PowerShell
2. Change working directory to installation folder (```cd $env:HOMEPATH\Documents\GitHub\PassUTD```)
3. If running for the first time: ```docker compose up --build -d```
3. If running anytime after: ```docker compose up -d```
4. Start mysql: ```mysql -h 127.0.0.1 -P 3307 -u root -p --execute="source Database Script.sql"```
5. Run app.py `python app.py`
6. Open local host in a web browser `http://localhost:5000/`

