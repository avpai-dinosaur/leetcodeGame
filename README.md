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

# Todo

- When player runs into an obstacle, continue movement animation
- Add a mental health note
- Make dance floor lights look nicer
- Make clickable elements change color when clicked (plus cursor image changes)
- Add type annotations
- Consolidate some sprite behaviors into a base class
- Consolidate some menu UI behavior into a base controls class
- Connect to leetcode account and detect that a question was solved
- Boss fight
- Level loading
- Figure out why music isn't working
- switch handling of game objects to level class from map class. map class should only parse and present data from tiled
- related, an object creating factory to communicate to level class what types of objects to create based on parsed map data
