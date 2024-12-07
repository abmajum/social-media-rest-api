How to run this app?
```
python3 -m venv .venv
source .venv/scripts/activate
pip3 install -r requirements.txt
```
Run in development mode
```
#export necessary variables
export dbconnectionstring='smstring'
fastapi dev app/main.py
```