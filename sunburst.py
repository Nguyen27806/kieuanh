import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Sunburst: Field of Study and SAT Score Percentile Levels")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, sheet_name="education_career_success")

    # Tính các mốc phần trăm
    low = df['SAT_Score'].quantile(0.33)
    high = df['SAT_Score'].quantile(0.66)

    # Phân loại SAT Score theo phần trăm
    def sat_percentile(score):
        if score <= low:
            return 'Thấp (<= 33%)'
        elif score <= high:
            return 'Trung bình (33%-66%)'
        else:
            return 'Cao (> 66%)'

    df['SAT_Level'] = df['SAT_Score'].apply(sat_percentile)

    # Nhóm dữ liệu
    grouped = df.groupby(['Field_of_Study', 'SAT_Level']).size().reset_index(name='Count')

    # Vẽ sunburst
    fig = px.sunburst(
        grouped,
        path=['Field_of_Study', 'SAT_Level'],
        values='Count',
        title='Phân loại SAT Score theo phần trăm trong từng ngành học',
        color='Count',
        color_continuous_scale='YlGnBu'
    )

    st.plotly_chart(fig)