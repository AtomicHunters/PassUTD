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


### Change working directory (after pulling database)

```cd $env:HOMEPATH\Documents\GitHub\PassUTD```

### Build and Run docker container:

```docker compose up --build -d```

### Only run docker container: 
```docker compose up -d```

- Only do this if docker container is ever stopped and needs to be started back up
### Connect to mySQL (will not have to do this in the future):
```mysql -h 127.0.0.1 -P 3307 -u root -p --execute="source Database Script.sql"```
- 3307 may be changed to another port if you've decided to use something else
- Database script path is the relative path from

