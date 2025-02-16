import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Stock Market Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to",
                        ["Project Info", "Data Analysis & Visualization", "Project Overview & Self Introduction"])

# File Upload Section
st.sidebar.title("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload Stock Data CSV", type=["csv"], accept_multiple_files=False)


def load_data():
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df["Date"] = pd.to_datetime(df["Date"])

        # Remove duplicates
        df = df.drop_duplicates(subset=["Date", "Symbol"], keep="last")
        return df
    else:
        st.warning("Please upload a CSV file to proceed.")
        return pd.DataFrame()


data = load_data()

# Project Info Page
if page == "Project Info":
    st.title("Stock Market Analysis Dashboard")
    st.write("This project analyzes Nifty 50 stock performance using various financial metrics.")
    st.write(
        "It includes interactive data visualizations, stock correlation analysis, and insights into market trends.")

# Data Analysis & Visualization Page
elif page == "Data Analysis & Visualization":
    st.title("Stock Market Data Analysis")

    if not data.empty:
        # Stock Selection
        stocks = data["Symbol"].unique()
        selected_stock = st.selectbox("Select a stock:", stocks)

        # Date Range Filter
        min_date = data["Date"].min()
        max_date = data["Date"].max()
        start_date, end_date = st.date_input("Select Date Range:", [min_date, max_date], min_value=min_date,
                                             max_value=max_date)

        # Filtered Data
        filtered_data = data[(data["Symbol"] == selected_stock) & (data["Date"] >= pd.to_datetime(start_date)) & (
                    data["Date"] <= pd.to_datetime(end_date))]

        # Stock Price Line Chart
        fig = px.line(filtered_data, x="Date", y="Close", title=f"Stock Price of {selected_stock}")
        st.plotly_chart(fig)

        # Stock Volatility Analysis
        filtered_data["Daily Return"] = filtered_data["Close"].pct_change()
        fig_volatility = px.line(filtered_data, x="Date", y="Daily Return", title=f"Volatility of {selected_stock}")
        st.plotly_chart(fig_volatility)

        # Cumulative Return Calculation
        filtered_data["Cumulative Return"] = (1 + filtered_data["Daily Return"]).cumprod()
        fig_cumulative = px.line(filtered_data, x="Date", y="Cumulative Return",
                                 title=f"Cumulative Return of {selected_stock}")
        st.plotly_chart(fig_cumulative)

        # Sector-Wise Performance Overview
        sector_performance = data.groupby("Symbol")["Close"].mean()
        fig_sector = px.bar(sector_performance, title="Sector-Wise Stock Performance")
        st.plotly_chart(fig_sector)

        # Top Gainers & Losers
        latest_data = data[data["Date"] == data["Date"].max()]
        top_gainers = latest_data.nlargest(5, "Close")
        top_losers = latest_data.nsmallest(5, "Close")

        st.write("### Top 5 Gainers")
        st.dataframe(top_gainers)
        st.write("### Top 5 Losers")
        st.dataframe(top_losers)

        # Stock Correlation Matrix
        if data.duplicated(subset=['Date', 'Symbol']).any():
            st.warning(
                "Warning: Dataset contains duplicate (Date, Symbol) entries. They have been handled automatically.")

        correlation_matrix = data.pivot_table(index='Date', columns='Symbol', values='Close', aggfunc='mean').corr()
        st.write("### Stock Price Correlation Matrix")
        st.dataframe(correlation_matrix)

        # Download CSV
        csv = filtered_data.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv, file_name=f"{selected_stock}_data.csv", mime='text/csv')
    else:
        st.warning("No data available. Please upload the required CSV file.")

# Project Overview & Self Introduction Page
elif page == "Project Overview & Self Introduction":
    st.title("Project Overview & Self Introduction")
    st.write(
        "This project is built as part of a data-driven stock analysis initiative using Streamlit, Pandas, and Power BI.")
    st.write("### About Me")
    st.write(
        "I am a final-year Computer Application student with a passion for Machine Learning and AI. This project demonstrates my ability to work with real-time financial data and create interactive dashboards.")
