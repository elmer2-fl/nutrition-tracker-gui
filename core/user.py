class UserProfile:
    def __init__(self, name, age, gender, height, weight):
        self.name = name
        self.age = int(age)
        self.gender = gender
        self.height = float(height)
        self.weight = float(weight)
        self.goal = None
        self.pace = None
        self.workouts = 0
        self.duration = 0
        self.intensity = None