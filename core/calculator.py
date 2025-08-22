def calculate_bmr(user):
    if user.gender == 'male':
        return 10 * user.weight + 6.25 * user.height - 5 * user.age + 5
    else:
        return 10 * user.weight + 6.25 * user.height - 5 * user.age - 161

def calculate_tdee(bmr, user):
    factor = 1.2 + (user.workouts * user.duration / 300)
    return bmr * factor

def adjust_goal(tdee, goal, pace):
    pace_map = {
        "very slow": 150,
        "slow": 300,
        "standard": 500,
        "fast": 700,
        "very fast": 1000
    }
    adj = pace_map.get(pace, 500)

    if goal == 'lose fat':
        return tdee - adj
    elif goal == 'gain muscle':
        return tdee + adj
    return tdee

def calculate_macros(calories, user):
    protein = user.weight * (2.0 if user.goal == 'lose fat' else 1.6)
    fat = user.weight * 0.8
    carbs = (calories - (protein * 4 + fat * 9)) / 4
    return round(protein), round(carbs), round(fat)
