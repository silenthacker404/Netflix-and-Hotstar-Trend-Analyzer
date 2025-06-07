import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="📊 CSV Data Visualizer", layout="wide")
st.title("🎬 Smart CSV Data Analyzer (Netflix / Hotstar / Any Platform)")

uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip().str.lower()

        st.success("✅ File successfully loaded!")
        st.subheader("🧾 Available Columns")
        st.write(df.columns.tolist())

        st.subheader("👀 Data Preview")
        st.dataframe(df.head(10))

        st.subheader("📌 Summary Statistics")
        for col in df.columns:
            st.markdown(f"**🔹 {col.upper()}**")
            if df[col].dtype == 'object':
                st.write("Top 5 Frequent Values:")
                st.dataframe(df[col].value_counts().head(5))
            else:
                st.write(df[col].describe())

        st.subheader("📈 Visualize a Column")

        selected_col = st.selectbox("Select a column to visualize", df.columns)

        chart_type = st.radio("Select chart type", ["Bar Chart", "Pie Chart", "Line Chart"])

        if df[selected_col].dtype == "object":
            data = df[selected_col].dropna().str.split(',').explode().str.strip()
            chart_df = data.value_counts().reset_index()
            chart_df.columns = ['value', 'count']
        else:
            chart_df = df[selected_col].dropna().value_counts().sort_index().reset_index()
            chart_df.columns = ['value', 'count']

        fig = None

        if chart_type == "Bar Chart":
            fig = px.bar(chart_df.head(20), x='value', y='count',
                         color='count', title=f"Top 20 Values in '{selected_col}'",
                         labels={"value": selected_col.title(), "count": "Frequency"})
        elif chart_type == "Pie Chart":
            fig = px.pie(chart_df.head(10), values='count', names='value',
                         title=f"Top 10 Distribution in '{selected_col}'", hole=0.4)
        elif chart_type == "Line Chart":
            if df[selected_col].dtype != 'object':
                chart_df = chart_df.sort_values('value')
                fig = px.line(chart_df, x='value', y='count',
                              title=f"Line Chart of '{selected_col}'",
                              labels={'value': selected_col.title(), 'count': 'Frequency'})
            else:
                st.warning("Line chart is suitable only for numeric/date-based columns.")

        if fig:
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("🔍 Filter and Explore Data")
        with st.expander("🔧 Add Filters"):
            for col in df.select_dtypes(include=['object']).columns:
                options = st.multiselect(f"Filter {col}", df[col].dropna().unique())
                if options:
                    df = df[df[col].isin(options)]

            for col in df.select_dtypes(include=['float', 'int']).columns:
                min_val, max_val = float(df[col].min()), float(df[col].max())
                range_val = st.slider(f"Range for {col}", min_val, max_val, (min_val, max_val))
                df = df[df[col].between(*range_val)]

        st.subheader("🧾 Filtered Data Preview")
        st.dataframe(df.head(10))

        st.subheader("☁️ Word Cloud (Textual Insights)")
        text_col = st.selectbox("Select a text column for word cloud", df.columns)

        if df[text_col].dtype == "object":
            text = " ".join(df[text_col].dropna().astype(str))
            wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='Pastel1').generate(text)
            fig_wc, ax = plt.subplots(figsize=(12, 6))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig_wc)
        else:
            st.warning("Word cloud is only available for text-based columns.")

    except Exception as e:
        st.error(f"❌ Error loading file: {e}")

else:
    st.info("📂 Please upload a CSV file to begin your analysis.")
