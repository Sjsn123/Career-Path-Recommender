import streamlit as st
import pickle
import numpy as np

# Load the scaler, label encoder, model, and class names
scaler = pickle.load(open("model/scaler.pkl", 'rb'))
model = pickle.load(open("model/model.pkl", 'rb'))
class_names = ['Lawyer', 'Doctor', 'Government Officer', 'Artist', 'Unknown',
               'Software Engineer', 'Teacher', 'Business Owner', 'Scientist',
               'Banker', 'Writer', 'Accountant', 'Designer',
               'Construction Engineer', 'Game Developer', 'Stock Investor',
               'Real Estate Developer']

# Recommendations function
def Recommendations(gender, part_time_job, extracurricular_activities,
                    weekly_self_study_hours, math_score, history_score, physics_score,
                    chemistry_score, biology_score, english_score, geography_score,
                    total_score, average_score):
    # Encode categorical variables
    gender_encoded = 1 if gender.lower() == 'female' else 0
    part_time_job_encoded = 1 if part_time_job else 0
    extracurricular_activities_encoded = 1 if extracurricular_activities else 0

    # Create feature array
    feature_array = np.array([[gender_encoded, part_time_job_encoded, extracurricular_activities_encoded,
                               weekly_self_study_hours, math_score, history_score, physics_score,
                               chemistry_score, biology_score, english_score, geography_score, total_score,
                               average_score]])

    # Scale features
    scaled_features = scaler.transform(feature_array)

    # Predict using the model
    probabilities = model.predict_proba(scaled_features)

    # Get top three predicted classes along with their probabilities
    top_classes_idx = np.argsort(-probabilities[0])[:3]
    top_classes_names_probs = [(class_names[idx], probabilities[0][idx]) for idx in top_classes_idx]

    return top_classes_names_probs

# Streamlit UI setup
def main():
    # Set the page layout to wide
    st.set_page_config(page_title="📚 Education Recommendation System", page_icon="📚", layout="wide")
    st.title("📚 Education Recommendation System")
    
    st.write(
        """
        Welcome to the Education Recommendation System. This tool helps university students
        in selecting the most suitable studies and courses based on academic performance, interests,
        and career aspirations. Fill in the form below to get personalized recommendations.
        """
    )
    
    # Main Info Section
    st.header("Main Information")
    
    # Default values for form fields
    gender = st.selectbox("👤 Gender", ["Male", "Female"], index=1, key="gender")
    part_time_job = st.selectbox("💼 Part-Time Job", ["Yes", "No"], index=0, key="part_time_job")
    extracurricular_activities = st.selectbox("🎭 Extracurricular Activities", ["Yes", "No"], index=0, key="extracurricular_activities")
    weekly_self_study_hours = st.number_input("⏱ Weekly Self-Study Hours", min_value=0, max_value=100, step=1, value=5, key="weekly_study_hours")
    
    # Subject Scores Section with default value 40
    st.header("📊 Subject Scores")
    math_score = st.number_input("📐 Math Score", min_value=0, max_value=100, step=1, value=40, key="math_score")
    history_score = st.number_input("📜 History Score", min_value=0, max_value=100, step=1, value=40, key="history_score")
    physics_score = st.number_input("🧲 Physics Score", min_value=0, max_value=100, step=1, value=40, key="physics_score")
    chemistry_score = st.number_input("⚗️ Chemistry Score", min_value=0, max_value=100, step=1, value=40, key="chemistry_score")
    biology_score = st.number_input("🧬 Biology Score", min_value=0, max_value=100, step=1, value=40, key="biology_score")
    english_score = st.number_input("📖 English Score", min_value=0, max_value=100, step=1, value=40, key="english_score")
    geography_score = st.number_input("🌍 Geography Score", min_value=0, max_value=100, step=1, value=40, key="geography_score")

    # Automatically calculate Total and Average as user changes marks
    total_score = math_score + history_score + physics_score + chemistry_score + biology_score + english_score + geography_score
    average_score = total_score / 7
    
    # Display live total and average score
    st.write(f"**Total Score**: {total_score}")
    st.write(f"**Average Score**: {average_score:.2f}")
    
    # Submit button for getting recommendations
    submit_button = st.button("Get Recommendations")

    if submit_button:
        # Check if average score is below 40
        if average_score < 40:
            st.warning("⚠️ Your average score is below 40. Please aim to pass in all subjects before proceeding.")
        else:
            # Get recommendations based on user input
            recommendations = Recommendations(gender, part_time_job == "Yes", extracurricular_activities == "Yes",
                                              weekly_self_study_hours, math_score, history_score, physics_score,
                                              chemistry_score, biology_score, english_score, geography_score,
                                              total_score, average_score)
            
            # Recommendations Section with larger font size
            st.markdown("<h2 style='font-size: 36px;'>Top Recommended Studies</h2>", unsafe_allow_html=True)
            
            for rec in recommendations:
                st.markdown(f"<h3 style='font-size: 24px;'>{rec[0]}</h3>", unsafe_allow_html=True)
        
if __name__ == '__main__':
    main()
