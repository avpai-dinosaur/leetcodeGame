import pygame

MAP_WIDTH = 30
MAP_HEIGHT = 20
TILE_SIZE = 32
INIT_PLAYER_POS = (256, 256)
ENEMY_SPEED = 0.5
ENEMY_CHASE_SPEED = 0.7

# Animation constants
PLAYER_SHEET_METADATA = {
    "frame_width": 48,
    "frame_height": 48,
    "scale": 1,
    "actions": {
        "idle": {
            "row": 0,
            "num_frames": 4,
            "cooldown": 500
        },
        "run" : {
            "row": 4,
            "num_frames": 10,
            "cooldown": 50
        },
        "jump" : {
            "row": 2,
            "num_frames": 4,
            "cooldown": 50
        },
        "punch" : {
            "row": 4,
            "num_frames": 3,
            "cooldown": 50
        }
    },
    "colorkey": (0, 0, 0)
}

ENEMY_SHEET_METADATA = {
    "frame_width": 48,
    "frame_height": 48,
    "scale": 1.5,
    "actions": {
        # "idle": {
        #     "row": 0,
        #     "num_frames": 5
        # },
        # "dead" : {
        #     "row": 0,
        #     "num_frames": 5, 
        # },
        "walk" : {
            "row": 0,
            "num_frames": 4
        }
    },
    "colorkey": (0, 0, 0)
}