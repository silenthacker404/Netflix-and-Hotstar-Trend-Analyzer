import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="CSV Data Analyzer", layout="wide")
st.title("📈 Smart CSV Data Analyzer (Netflix/Hotstar or Any Platform)")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip().str.lower()  # Normalize headers

        st.subheader("🧾 Detected Columns")
        st.write(df.columns.tolist())

        st.subheader("📊 Preview of the Data")
        st.dataframe(df.head())

        # Show some quick statistics for all columns
        st.subheader("📌 Quick Stats for Each Column")
        for col in df.columns:
            st.markdown(f"**🔸 {col}**")
            if df[col].dtype == "object":
                st.write("Top Categories / Values:", df[col].value_counts().head(5))
            else:
                st.write(df[col].describe())

        # Dropdown to pick a column for chart
        st.subheader("📊 Visualize Any Column")
        column_to_plot = st.selectbox("Select a column to analyze (categorical recommended):", df.columns)
        if df[column_to_plot].dtype == "object":
            plot_data = df[column_to_plot].dropna().str.split(',').explode().str.strip().value_counts().reset_index()
            plot_data.columns = ['value', 'count']
        else:
            plot_data = df[column_to_plot].value_counts().reset_index()
            plot_data.columns = ['value', 'count']

        fig_bar = px.bar(plot_data.head(20), x='value', y='count',
                         title=f"Top Values in '{column_to_plot}'", color='value')
        st.plotly_chart(fig_bar, use_container_width=True)

        # Optional word cloud
        st.subheader("☁️ Word Cloud from a Text Column")
        text_column = st.selectbox("Choose a column for word cloud (text-based):", df.columns)
        if df[text_column].dtype == "object":
            text_data = " ".join(df[text_column].dropna().astype(str))
            wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='Pastel1').generate(text_data)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.info("The selected column is not suitable for word cloud (text only).")

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.info("📁 Upload a CSV file to start analysis.")
