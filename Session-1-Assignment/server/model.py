from enum import Enum


class Goal(str, Enum):
    build_muscle = "Build muscle"
    lose_fat = "Lose fat"
    general_fitness = "General fitness"
    improve_endurance = "Improve endurance"


class Experience(str, Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"


class Equipment(str, Enum):
    none = "No equipment"
    dumbbells = "Home dumbbells"
    full_gym = "Full gym"
