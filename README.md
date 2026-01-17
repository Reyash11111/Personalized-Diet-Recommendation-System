AI Personalized Diet Recommendation System
A web-based application that provides personalized diet recommendations based on user profiles, fitness goals, and dietary restrictions.
Features : 
    1.Profile Management: Create and manage multiple user profiles
    2.Caloric Calculations: Automatic calculation of daily caloric needs using    Harris-Benedict formula
    3.Personalized Recommendations: Get customized meal plans based on:
  - Age, weight, height, and gender
  - Activity level
  - Fitness goal (Weight Loss, Muscle Gain, Maintenance)
  - Dietary restrictions
    4.Meal Planning: Daily meal suggestions for breakfast, lunch, snack, and dinner
    5.Profile History: View all saved profiles

Setup Instructions :

1. Create Virtual Environment :
   python -m venv venv

2. Activate Virtual Environment:
     venv\Scripts\Activate.ps1
3. Install Dependencies:
   pip install -r requirements.txt

4. Run the Application:
   python app.py

5. Access the Application**:
   Open your browser and navigate to `http://localhost:5000`

Usage

1. Profile Setup Tab:
   - Enter your personal information (name, age, weight, height)
   - Select your gender and activity level
   - Choose your fitness goal
   - Select any dietary restrictions
   - Click "Save Profile"

2. Get Recommendations Tab:
   - Select your profile from the dropdown
   - Your profile statistics will display
   - View personalized meal recommendations for each meal type

3. View History Tab:
   - See all your saved profiles in a table format

Database

The application uses SQLite for data storage. User profiles are stored in `users.db` file.

 Technology Stack

- Backend: Flask (Python web framework)
- Frontend: HTML5, CSS3, JavaScript
- Database: SQLite
- Calculation Method: Harris-Benedict Formula for BMR calculation

Calculation Details

The system calculates daily caloric needs using the Harris-Benedict equation:
- BMR (Basal Metabolic Rate) is calculated based on gender, weight, height, and age
- TDEE (Total Daily Energy Expenditure) = BMR × Activity Multiplier
- Final Calories = TDEE adjusted by fitness goal:
  - Weight Loss: TDEE - 500 calories
  - Muscle Gain: TDEE + 300 calories
  - Maintenance: TDEE

 Files

- app.py: Main Flask application
- database_helper.py: Database operations
- recommendation_engine.py: Calorie calculations and meal recommendations
- templates/index.html: Web interface
- requirements.txt: Python dependencies
- users.db: SQLite database (created on first run)

 Notes

- All nutritional calculations are for informational purposes
- Consult with a healthcare professional for personalized dietary advice
- Meal database can be expanded with more options in `recommendation_engine.py`


