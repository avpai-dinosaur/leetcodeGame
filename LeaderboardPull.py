import pygame
import sqlite3
from flask import g, Flask

DATABASE = 'data/LeetStorage.db'

# Create the Flask application object
app = Flask(__name__)

def get_db():
    #db = getattr(g, '_database', None)
    #if db is None:
    #g._database =
    db =  sqlite3.connect(DATABASE)
    return db

def SubmitHighScore(playerName, score):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO Score_Tracker (Name, Score) VALUES (?,?)",
            (playerName, score)            
        )
        db.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False
    
    finally: 
        cursor.close()
    return True

def topScores():
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT Name, Score FROM Score_Tracker ORDER BY Score DESC LIMIT 10"
        )
        top_scores = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        cursor.close()
    return top_scores

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



