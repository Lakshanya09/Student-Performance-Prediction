import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
import time
st.set_page_config(
    page_title="AI Student Performance Predictor",
    page_icon="🎓",
    layout="wide"
)

model = joblib.load("random_forest_model.pkl")
encoder = joblib.load("label_encoder.pkl")
confidence = None
performance = None
st.markdown("""
# 🎓 AI Student Performance Prediction

### Predict student performance using Machine Learning and Random Forest

---
""")
c1,c2,c3,c4=st.columns(4)

c1.metric("🤖 Model","Random Forest")
c2.metric("📊 Features","11")
c3.metric("🎯 Target","Performance")
c4.metric("⚡ Prediction","Instant")
st.markdown("---")
st.header("📝 Student Details")

left, right = st.columns(2)

# ==========================
# Academic Details
# ==========================

with left:

    st.subheader("📚 Academic Details")

    attendance = st.slider(
        "Attendance (%)",
        0, 100, 80
    )

    study_hours = st.slider(
        "Study Hours (per day)",
        0.0, 12.0, 5.0, 0.5
    )

    assignment_score = st.slider(
        "Assignment Score",
        0, 100, 75
    )

    quiz_score = st.slider(
        "Quiz Score",
        0, 100, 70
    )

    previous_semester_marks = st.slider(
        "Previous Semester Marks",
        0, 100, 75
    )

    class_engagement = st.slider(
        "Class Engagement",
        0, 100, 80
    )

# ==========================
# Lifestyle Details
# ==========================

with right:

    st.subheader("🌿 Lifestyle Details")

    sleep_hours = st.slider(
        "Sleep Hours",
        0.0, 12.0, 7.0, 0.5
    )

    screen_time = st.slider(
        "Screen Time (Hours)",
        0.0, 12.0, 3.0, 0.5
    )

    stress_level = st.slider(
        "Stress Level",
        0, 10, 5
    )

    weekend_study_hours = st.slider(
        "Weekend Study Hours",
        0.0, 15.0, 4.0, 0.5
    )

    commute_time = st.slider(
        "Commute Time (Minutes)",
        0, 180, 30
    )
    st.markdown("")

predict = st.button(
    "🎯 Predict Student Performance",
    use_container_width=True
)
if predict:

    input_data = pd.DataFrame([{

        "Attendance": attendance,

        "Study_Hours": study_hours,

        "Sleep_Hours": sleep_hours,

        "Screen_Time": screen_time,

        "Stress_Level": stress_level,

        "Class_Engagement": class_engagement,

        "Assignment_Score": assignment_score,

        "Quiz_Score": quiz_score,

        "Previous_Semester_Marks": previous_semester_marks,

        "Weekend_Study_Hours": weekend_study_hours,

        "Commute_Time": commute_time

    }])

        # ==========================
    # AI Prediction
    # ==========================

    with st.spinner("🤖 AI is analysing the student's performance..."):
        time.sleep(2)

        prediction = model.predict(input_data)[0]
        performance = encoder.inverse_transform([prediction])[0]

        confidence = None

        if hasattr(model, "predict_proba"):
            confidence = model.predict_proba(input_data).max() * 100
            st.markdown("---")

    st.markdown(
        f"""
        <div style="
            background:linear-gradient(135deg,#2563EB,#7C3AED);
            padding:30px;
            border-radius:20px;
            color:white;
            text-align:center;
            box-shadow:0px 10px 25px rgba(0,0,0,.25);
        ">

        <h2>🎯 Predicted Performance</h2>

        <h1>{performance}</h1>

        </div>
        """,
        unsafe_allow_html=True
    )

if confidence is not None:

        st.markdown("### 🤖 Model Confidence")

        st.progress(confidence/100)

        st.success(f"Confidence : {confidence:.2f}%")
        st.markdown("---")

        st.subheader("💡 AI Recommendations")

recommendations=[]

if attendance < 75:
        recommendations.append("📌 Improve attendance for better academic consistency.")

if study_hours < 4:
        recommendations.append("📚 Increase daily study hours.")

if assignment_score < 70:
        recommendations.append("📝 Focus on improving assignment scores.")

if quiz_score < 70:
        recommendations.append("📖 Revise regularly to improve quiz performance.")

if sleep_hours < 6:
        recommendations.append("😴 Sleep at least 7–8 hours every day.")

if screen_time > 6:
        recommendations.append("📱 Reduce unnecessary screen time.")

if stress_level > 7:
        recommendations.append("🧘 Practice stress management.")

if weekend_study_hours < 3:
        recommendations.append("📅 Spend more productive time studying during weekends.")

if class_engagement < 70:
        recommendations.append("🙋 Participate more actively in class.")

if commute_time > 90:
        recommendations.append("🚍 Long commute detected. Try to manage study time during travel.")

if len(recommendations)==0:

        st.success("🎉 Excellent! The student's academic profile looks balanced.")

else:

        for item in recommendations:

            st.info(item)

            st.markdown("---")

            st.subheader("📋 Student Summary")

        c1,c2,c3,c4=st.columns(4)

        c1.metric("Attendance",f"{attendance}%")

        c2.metric("Study Hours",study_hours)

        c3.metric("Stress",stress_level)

        c4.metric("Quiz Score",quiz_score)


st.markdown("---")
st.header("📊 Student Analytics Dashboard")

col1, col2 = st.columns(2)

with col1:

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=attendance,
        title={"text":"Attendance (%)"},
        gauge={
            "axis":{"range":[0,100]},
            "bar":{"color":"royalblue"},
            "steps":[
                {"range":[0,50],"color":"#ffcccc"},
                {"range":[50,75],"color":"#ffe699"},
                {"range":[75,100],"color":"#b6f2c6"}
            ]
        }
    ))

    fig.update_layout(height=350)

    st.plotly_chart(fig,use_container_width=True)

with col2:

    chart = pd.DataFrame({

        "Feature":[
            "Attendance",
            "Assignment",
            "Quiz",
            "Previous Sem"
        ],

        "Score":[
            attendance,
            assignment_score,
            quiz_score,
            previous_semester_marks
        ]

    })

    fig = px.bar(
        chart,
        x="Feature",
        y="Score",
        text="Score",
        color="Score"
    )

    fig.update_layout(height=350)

    st.plotly_chart(fig,use_container_width=True)
    st.markdown("---")

lifestyle = pd.DataFrame({

    "Category":[
        "Study Hours",
        "Sleep",
        "Screen",
        "Weekend Study"
    ],

    "Hours":[
        study_hours,
        sleep_hours,
        screen_time,
        weekend_study_hours
    ]

})

fig = px.line(

    lifestyle,

    x="Category",

    y="Hours",

    markers=True

)

fig.update_layout(height=400)

st.plotly_chart(fig,use_container_width=True)
if confidence is not None:

    st.markdown("---")

    st.subheader("🤖 AI Confidence")

    fig = go.Figure(go.Indicator(

        mode="gauge+number",

        value=confidence,

        title={"text":"Prediction Confidence (%)"},

        gauge={

            "axis":{"range":[0,100]},

            "bar":{"color":"green"}

        }

    ))

    fig.update_layout(height=350)

    st.plotly_chart(fig,use_container_width=True)
    st.markdown("---")

confidence_text = (
    f"{confidence:.2f}%"
    if confidence is not None
    else "Not Available"
)

report = f"""
AI STUDENT PERFORMANCE REPORT

Predicted Performance : {performance}

Attendance : {attendance}
Study Hours : {study_hours}
Sleep Hours : {sleep_hours}
Screen Time : {screen_time}
Stress Level : {stress_level}
Class Engagement : {class_engagement}
Assignment Score : {assignment_score}
Quiz Score : {quiz_score}
Previous Semester Marks : {previous_semester_marks}
Weekend Study Hours : {weekend_study_hours}
Commute Time : {commute_time}

Prediction Confidence : {confidence_text}
"""

st.download_button(

    label="📄 Download Report",

    data=report,

    file_name="Student_Report.txt",

    mime="text/plain"

)
st.markdown("---")

st.markdown(
"""
<center>

### 🎓 AI Student Performance Prediction System

Built using

**Python • Streamlit • Random Forest • Plotly**

Developed by **Lakshanyawanti B**

</center>
""",
unsafe_allow_html=True
)
