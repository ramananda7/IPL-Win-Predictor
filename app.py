import streamlit as st
import pickle
import pandas as pd

teams = [
    'Royal Challengers Bangalore',
    'Kings XI Punjab',
    'Mumbai Indians',
    'Kolkata Knight Riders',
    'Rajasthan Royals',
    'Chennai Super Kings',
    'Sunrisers Hyderabad',
    'Delhi Capitals',
    'Lucknow Super Giants',
    'Gujarat Titans'
]

city = [
    'Bangalore', 'Chandigarh', 'Delhi', 'Mumbai', 'Kolkata', 'Jaipur',
    'Hyderabad', 'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban',
    'Centurion', 'East London', 'Johannesburg', 'Kimberley',
    'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
    'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
    'Bengaluru', 'Indore', 'Dubai', 'Sharjah', 'Navi Mumbai',
    'Lucknow', 'Guwahati', 'Mohali'
]
# Create your manual mapping
team_mapping = {
    'Royal Challengers Bangalore': 0,
    'Kings XI Punjab': 1,
    'Mumbai Indians': 2,
    'Kolkata Knight Riders': 3,
    'Rajasthan Royals': 4,
    'Chennai Super Kings': 5,
    'Sunrisers Hyderabad': 6,
    'Delhi Capitals': 7,
    'Lucknow Super Giants': 8,
    'Gujarat Titans': 9,
    'Pune Warriors': 10   # if needed
}
# Manual mapping for city
city_mapping = {
    'Bangalore': 0,
    'Chandigarh': 1,
    'Delhi': 2,
    'Mumbai': 3,
    'Kolkata': 4,
    'Jaipur': 5,
    'Hyderabad': 6,
    'Chennai': 7,
    'Cape Town': 8,
    'Port Elizabeth': 9,
    'Durban': 10,
    'Centurion': 11,
    'East London': 12,
    'Johannesburg': 13,
    'Kimberley': 14,
    'Bloemfontein': 15,
    'Ahmedabad': 16,
    'Cuttack': 17,
    'Nagpur': 18,
    'Dharamsala': 19,
    'Visakhapatnam': 20,
    'Pune': 21,
    'Raipur': 22,
    'Ranchi': 23,
    'Abu Dhabi': 24,
    'Bengaluru': 25,   # notice: different spelling from Bangalore
    'Indore': 26,
    'Dubai': 27,
    'Sharjah': 28,
    'Navi Mumbai': 29,
    'Lucknow': 30,
    'Guwahati': 31,
    'Mohali': 32
}

# # Apply mapping
# deliveries['city'] = deliveries['city'].map(city_mapping)
# # Apply mapping manually
# deliveries['batting_team'] = deliveries['batting_team'].map(team_mapping)
# deliveries['bowling_team'] = deliveries['bowling_team'].map(team_mapping)


# Load the model
pipe = pickle.load(open('pipe.pkl', 'rb'))

# App title
st.title('IPL Win Predictor')

# Layout with 2 columns
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select Batting Team', sorted(teams))

with col2:
    bowling_team = st.selectbox('Select Bowling Team', sorted(teams))

Selected_city = st.selectbox('City', sorted(city))
Target = st.number_input('Target')

col3,col4,col5 = st.columns(3)

with col3:
    score = st.number_input('Score')
with col4:
    overs = st.number_input('Overs completed')
with col5:
    wickets = st.number_input('Wickets out')

if st.button('Predict Probability'):
    runs_left = Target - score
    balls_left = 120 - (overs*6)
    wickets = 10 - wickets
    crr = score/overs
    rrr = (runs_left*6)/balls_left
    bat = team_mapping[batting_team]
    bowl = team_mapping[bowling_team]
    c= city_mapping[Selected_city]

    input_df = pd.DataFrame({'batting_team':[bat],'bowling_team':[bowl],'city':[c],'runs_left':[runs_left],'ball_left':[balls_left],'wicket_left':[wickets],'target_runs':[Target],'crr':[crr],'rrr':[rrr]})

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + "- " + str(round(win*100)) + "%")
    st.header(bowling_team + "- " + str(round(loss*100)) + "%")