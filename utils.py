import os

FILE_NAME = "highscore.txt"

def load_highscore():
    if not os.path.exists(FILE_NAME):
        return 0
    with open(FILE_NAME, "r") as f:
        try:
            return int(f.read())
        except:
            return 0

def save_highscore(score):
    with open(FILE_NAME, "w") as f:
        f.write(str(score))
