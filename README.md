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

# Leaderboard

Run leaderboard locally with

```
cd leaderboard
flask --app leaderboard.py run
```

## API

Submit a new score with

```
curl -X POST http://localhost:5000/api/upload/ -F "username=[user name here]" -F "score=[score here]"
```

Get board in json with

```
curl -X GET http://localhost:5000/api/board/
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

# Todo

- When player runs into an obstacle, continue movement animation
- Add back the start menu, with a menu class
- Add a mental health note
- Make dance floor lights look nicer
- Make clickable elements change color when clicked (plus cursor image changes)
- Add type annotations
- Consolidate some sprite behaviors into a base class
- Connect to leetcode account and detect that a question was solved

- Fix text wrapping on roomba speech bubble DONE
- Make the prompt to open the door bigger and nicer DONE
- Make laser doors look nicer DONE
- Make the problems appear on the computers and the laser door connected to solving enough problems DONE
- Add some story elements through SMS between computers DONE
