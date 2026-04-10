from enum import Enum


class Difficulty(str, Enum):
    training = "Training"
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"
    legendary = "Legendary"


class HeistStatus(str, Enum):
    active = "Active"
    expired = "Expired"
    aborted = "Aborted"
