from flask import Flask, render_template, request, jsonify
from database_helper import init_db, save_profile, get_profile, get_all_profiles, delete_profile
from recommendation_engine import calculate_calories, get_meal_recommendations, generate_weekly_plan

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    profiles = get_all_profiles()
    profile_list = []                                                                                                                                               
    for p in profiles:
        profile_list.append({
            'name': p[0],
            'age': p[1],
            'weight': p[2],
            'height': p[3],
            'gender': p[4],
            'goal': p[5],
            'restrictions': p[6]
        })
    return jsonify(profile_list)

@app.route('/api/profile', methods=['POST'])
def create_profile():
    data = request.json
    profile = {
        'name': data['name'],
        'age': int(data['age']),
        'weight': float(data['weight']),
        'height': int(data['height']),
        'gender': data['gender'],
        'goal': data['goal'],
        'restrictions': ','.join(data.get('restrictions', []))
    }
    save_profile(profile)
    return jsonify({'status': 'success', 'message': f"Profile saved for {data['name']}"})

@app.route('/api/recommendation/<name>', methods=['GET'])
def get_recommendation(name):
    profile = get_profile(name)
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    name, age, weight, height, gender, goal, restrictions = profile

    # Activity level removed from profile form — assume Moderate by default
    activity_level = 'Moderate'

    # Calculate calories
    calories = calculate_calories(weight, height, age, gender, activity_level, goal)
    
    # Get meal recommendations
    meals = get_meal_recommendations(calories, goal, restrictions)
    
    # Format response: send today's meals (index 0) for quick view and a full weekly_plan
    meals_response = {}
    for meal_type, meal_list in meals.items():
        if meal_list:
            m = meal_list[0]
            meals_response[meal_type] = [{'name': m['name'], 'calories': m['calories']}]
        else:
            meals_response[meal_type] = []
    
    return jsonify({
        'name': name,
        'age': age,
        'weight': weight,
        'height': height,
        'gender': gender,
        'goal': goal,
        'daily_calories': calories,
        'meals': meals_response,
        'weekly_plan': generate_weekly_plan(meals, restrictions)
    })

@app.route('/api/profile/<name>', methods=['DELETE'])
def delete_user_profile(name):
    delete_profile(name)
    return jsonify({'status': 'success', 'message': f"Profile {name} deleted"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)