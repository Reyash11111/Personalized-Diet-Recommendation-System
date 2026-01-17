"""
Recommendation Engine for personalized diet plans
"""

def calculate_calories(weight, height, age, gender, activity_level, goal):
    """
    Calculate daily caloric needs using Harris-Benedict formula
    """
    # Basal Metabolic Rate (BMR)
    if gender.lower() == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    # Activity multiplier
    activity_multipliers = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Very Active": 1.9
    }
    
    tdee = bmr * activity_multipliers.get(activity_level, 1.55)
    
    # Goal adjustment
    if goal == "Weight Loss":
        return int(tdee - 500)  # 500 cal deficit per day
    elif goal == "Muscle Gain":
        return int(tdee + 300)  # 300 cal surplus per day
    else:  # Maintenance
        return int(tdee)


def get_meal_recommendations(calories, goal, restrictions):
    """
    Generate meal recommendations based on caloric needs
    """
    restriction_list = restrictions.split(",") if restrictions != "None" else []
    
    # Macro distribution
    if goal == "Muscle Gain":
        protein_ratio = 0.35  # 35% protein
        carbs_ratio = 0.45    # 45% carbs
        fat_ratio = 0.20      # 20% fats
    elif goal == "Weight Loss":
        protein_ratio = 0.40  # 40% protein
        carbs_ratio = 0.35    # 35% carbs
        fat_ratio = 0.25      # 25% fats
    else:  # Maintenance
        protein_ratio = 0.30
        carbs_ratio = 0.50
        fat_ratio = 0.20
    
    # Calculate macros
    protein_cals = int(calories * protein_ratio)
    carbs_cals = int(calories * carbs_ratio)
    fat_cals = int(calories * fat_ratio)
    
    # Meal breakdown
    breakfast_cals = int(calories * 0.25)
    lunch_cals = int(calories * 0.35)
    snack_cals = int(calories * 0.10)
    dinner_cals = int(calories * 0.30)
    
    # Sample meals database (South Indian foods + natural options)
    meals_db = {
        "breakfast": [
            {"name": "Idli with Sambar & Coconut Chutney", "calories": 300, "protein": 10},
            {"name": "Masala Dosa with Coconut Chutney", "calories": 420, "protein": 8},
            {"name": "Pongal with Pepper & Ghee ", "calories": 380, "protein": 12},
            {"name": "Ragi Malt  with Jaggery", "calories": 320, "protein": 6},
            {"name": "Upma with Vegetables and Peanuts", "calories": 350, "protein": 10},
        ],
        "lunch": [
            {"name": "Sambar Rice with Vegetables and Rasam", "calories": 600, "protein": 18},
            {"name": "Curd Rice with Cucumber and lemon pickle", "calories": 520, "protein": 12},
            {"name": "Millet Khichdi with Vegetables", "calories": 550, "protein": 16},
            {"name": "Grilled Fish  with Steamed Rice", "calories": 560, "protein": 42},
            {"name": "Egg Curry with Brown Rice", "calories": 580, "protein": 36},
        ],
        "snack": [
            {"name": "Fresh Banana with Coconut Pieces", "calories": 120, "protein": 1},
            {"name": "Tender Coconut Water and Flesh", "calories": 110, "protein": 2},
            {"name": "Sprouted Moong Salad with Lemon", "calories": 160, "protein": 12},
            {"name": "Roasted Chickpeas", "calories": 150, "protein": 8},
            {"name": "Buttermilk  with Curry Leaves", "calories": 80, "protein": 3},
        ],
        "dinner": [
            {"name": "Grilled Paneer Tikka with Mixed Vegetables", "calories": 480, "protein": 30},
            {"name": "Fish Curry with Rice", "calories": 520, "protein": 40},
            {"name": "Mixed Vegetable Pulav with Raita", "calories": 450, "protein": 12},
            {"name": "Masoor Dal with Millet Rotis", "calories": 420, "protein": 22},
            {"name": "Vegetable Kurma with Ragi Rotis", "calories": 400, "protein": 10},
        ],
    }
    
    # Filter meals based on restrictions
    filtered_meals = {}
    for meal_type, meals_list in meals_db.items():
        filtered_meals[meal_type] = [
            meal for meal in meals_list
            if not any(restriction in meal["name"] for restriction in [
                "Meat" if "Vegetarian" in restriction_list else "",
                "Animal" if "Vegan" in restriction_list else "",
                "Gluten" if "Gluten-Free" in restriction_list else "",
                "Dairy" if "Dairy-Free" in restriction_list else "",
                "Nut" if "Nut-Free" in restriction_list else "",
            ])
        ]
    
    # Select meals close to target calories
    selected_meals = {}
    calorie_targets = {
        "breakfast": breakfast_cals,
        "lunch": lunch_cals,
        "snack": snack_cals,
        "dinner": dinner_cals,
    }
    
    for meal_type, target_cal in calorie_targets.items():
        available = filtered_meals.get(meal_type, meals_db[meal_type])
        if not available:
            selected_meals[meal_type] = []
            continue

        # Sort available meals by calories
        sorted_avail = sorted(available, key=lambda x: x["calories"])

        # Choose ordering based on goal to bias calories across the week
        if goal == "Muscle Gain":
            ordered = list(reversed(sorted_avail))  # higher-calorie first
        elif goal == "Weight Loss":
            ordered = sorted_avail  # lower-calorie first
        else:
            # Maintenance: use a balanced order (smallest -> largest -> middle -> repeat)
            mid = len(sorted_avail) // 2
            ordered = sorted_avail[mid:] + sorted_avail[:mid]

        # Build a 7-day list by cycling through ordered options
        week_list = [ordered[i % len(ordered)] for i in range(7)]
        selected_meals[meal_type] = week_list
    
    return selected_meals


def generate_weekly_plan(daily_meals, restrictions=None):
    """
    Generate a weekly meal plan from 7-day lists in daily_meals.
    Expects daily_meals[meal_type] to be a list of 7 meal dicts.
    Returns a list of dicts for Sunday -> Saturday.
    `restrictions` is a comma-separated string (e.g. 'Vegetarian') used to pick sensible defaults per diet.
    """
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    # Determine diet type from restrictions string
    diet_type = None
    if restrictions:
        parts = [p.strip().lower() for p in restrictions.split(',') if p.strip()]
        if 'vegan' in parts:
            diet_type = 'Vegan'
        elif 'vegetarian' in parts:
            diet_type = 'Vegetarian'
        elif 'non-vegetarian' in parts or 'nonveg' in parts or 'non veg' in parts:
            diet_type = 'Non-Vegetarian'

    if diet_type is None:
        # default to Vegetarian to match frontend default
        diet_type = 'Vegetarian'

    weekly_data = []
    for i, day in enumerate(days):
        breakfast = daily_meals.get("breakfast", [])
        lunch = daily_meals.get("lunch", [])
        snack = daily_meals.get("snack", [])
        dinner = daily_meals.get("dinner", [])

        # Fallback defaults per diet type
        if diet_type == 'Vegetarian':
            defaults = {
                "breakfast": {"name": "Idli with Sambar", "calories": 300},
                "lunch": {"name": "Millet Khichdi with Vegetables", "calories": 520},
                "snack": {"name": "Fresh Fruit (Seasonal)", "calories": 120},
                "dinner": {"name": "Masoor Dal with Millet Rotis", "calories": 420},
            }
        elif diet_type == 'Vegan':
            defaults = {
                "breakfast": {"name": "Ragi Malt (Vegan)", "calories": 320},
                "lunch": {"name": "Millet Khichdi (Vegan)", "calories": 550},
                "snack": {"name": "Sprouted Moong Salad", "calories": 160},
                "dinner": {"name": "Vegetable Kurma with Ragi Rotis", "calories": 400},
            }
        else:  # Non-Vegetarian
            defaults = {
                "breakfast": {"name": "Idli with Sambar", "calories": 300},
                "lunch": {"name": "Grilled Fish with Steamed Rice", "calories": 560},
                "snack": {"name": "Tender Coconut Water and Flesh", "calories": 110},
                "dinner": {"name": "Fish Curry with Rice", "calories": 520},
            }

        if i < len(breakfast):
            b_name = breakfast[i].get("name", "N/A")
            b_cal = breakfast[i].get("calories", 0)
            b = f"{b_name} ({b_cal} cal)"
        else:
            b_name = defaults["breakfast"]["name"]
            b_cal = defaults["breakfast"]["calories"]
            b = f"{b_name} ({b_cal} cal)"

        if i < len(lunch):
            l_name = lunch[i].get("name", "N/A")
            l_cal = lunch[i].get("calories", 0)
            l = f"{l_name} ({l_cal} cal)"
        else:
            l_name = defaults["lunch"]["name"]
            l_cal = defaults["lunch"]["calories"]
            l = f"{l_name} ({l_cal} cal)"

        if i < len(snack):
            s_name = snack[i].get("name", "N/A")
            s_cal = snack[i].get("calories", 0)
            s = f"{s_name} ({s_cal} cal)"
        else:
            s_name = defaults["snack"]["name"]
            s_cal = defaults["snack"]["calories"]
            s = f"{s_name} ({s_cal} cal)"

        if i < len(dinner):
            d_name = dinner[i].get("name", "N/A")
            d_cal = dinner[i].get("calories", 0)
            d = f"{d_name} ({d_cal} cal)"
        else:
            d_name = defaults["dinner"]["name"]
            d_cal = defaults["dinner"]["calories"]
            d = f"{d_name} ({d_cal} cal)"

        total_cals = 0
        # sum calories using actual meal if present, otherwise default
        meal_arrays = {"breakfast": breakfast, "lunch": lunch, "snack": snack, "dinner": dinner}
        for mtype, arr in meal_arrays.items():
            if i < len(arr):
                total_cals += arr[i].get("calories", 0)
            else:
                total_cals += defaults[mtype]["calories"]

        weekly_data.append({
            "Day": day,
            "Breakfast": b,
            "Lunch": l,
            "Snack": s,
            "Dinner": d,
            "Total Calories": total_cals,
        })

    return weekly_data
