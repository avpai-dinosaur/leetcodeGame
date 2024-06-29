import pygame

MAP_WIDTH = 40
MAP_HEIGHT = 25
TILE_SIZE = 64
INIT_PLAYER_POS = (256, 256)

# Animation constants
PLAYER_SHEET_METADATA = {
    "frame_width": 16,
    "frame_height": 16,
    "scale": 3,
    "actions": {
        "idle": {
            "row": 0,
            "num_frames": 2,
            "cooldown": 500
        },
        "run" : {
            "row": 1,
            "num_frames": 6,
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
    "frame_width": 64,
    "frame_height": 64,
    "scale": 0.75,
    "actions": {
        "idle": {
            "row": 1,
            "num_frames": 5
        },
        "dead" : {
            "row": 0,
            "num_frames": 5, 
        },
        "walk" : {
            "row": 5,
            "num_frames": 7
        }
    },
    "colorkey": (0, 0, 0)
}