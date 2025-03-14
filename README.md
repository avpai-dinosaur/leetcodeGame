# Build and Run

First activate your python virtual environment

```
source env/bin/activate
```

If you don't have a virtual environment create one with

```
python3 -m venv env
```

Install dependencies (make sure your virtual environment is activated!)

```
pip install -r requirements.txt
```

Run with

```
cd game
python3 main.py
```

# Todo in rough order of importance

- Connect to leetcode account and detect that a question was solved
- add unit tests
- Boss fight
- Camera motions at start of level
- Make clickable elements change color when clicked (plus cursor image changes)

- Add a mental health notes (new feature)
- Make dance floor lights look nicer
- Add type annotations
- Consolidate some sprite behaviors into a base class
- Consolidate some menu UI behavior into a base controls class
- Figure out why music isn't working
- don't initialize every single level at once
