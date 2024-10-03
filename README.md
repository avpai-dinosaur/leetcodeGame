# Build and Run
First activate your python virtual environment
```
source env/bin/activate
```
If you don't have a virtual environment create one with
```
python3 -m venv env
```
Install dependencies (make sure your virtual environemnt is activated!)
```
pip install -r requirements.txt
```
Run with
```
cd game
python3 main.py
```

# Database
Initialize database with
```
bin/db create
```
Reset databse with
```
bin/db reset
```
See all values in database with
```
bin/db dump
```
Delete databse with
```
bin/db destroy
```

