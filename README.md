# AI SYSTEM AGENT

AI Agent that performs:

✔ Copy database  
✔ Create DB user  
✔ Grant DB permissions  
✔ Create folder in file system  
✔ Set permissions  
✔ Copy files  

## Installation
pip install -r requirements.txt

## Run Server
uvicorn main:app --reload

## Test API (POST)
URL: http://127.0.0.1:8000/ask
Body:
{
    "message": "Create a new folder /home/data/newapp"
}

