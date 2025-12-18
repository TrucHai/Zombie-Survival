import os
from settings import HIGHSCORE_FILE, GOLD_FILE

# Highscore
def load_highscore():
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    with open(HIGHSCORE_FILE, "r") as f:
        try:
            return int(f.read())
        except:
            return 0

def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

# Gold
def load_gold():
    if not os.path.exists(GOLD_FILE):
        return 0
    with open(GOLD_FILE, "r") as f:
        try:
            return int(f.read())
        except:
            return 0

def save_gold(gold):
    with open(GOLD_FILE, "w") as f:
        f.write(str(gold))
