import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fuzzywuzzy import process
import re
import speech_recognition as sr

# Function to normalize column names
def normalize_column_name(name):
    return re.sub(r'[^a-zA-Z0-9]', '', name.lower())

# Function to match spoken column names or numbers
def match_column_input(input_str, df):
    if input_str.isdigit() and int(input_str) < len(df.columns):
        return df.columns[int(input_str)]
    else:
        column_names = df.columns.tolist()
        normalized_columns = {normalize_column_name(col): col for col in column_names}
        best_match, score = process.extractOne(normalize_column_name(input_str), normalized_columns.keys())
        return normalized_columns[best_match] if score > 50 else None

# Python sorting function for improved performance
def python_sort(data):
    return sorted(data)

# Improved Voice recognition for hands-free command input
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Improved noise calibration
        st.info("Listening for voice command... Speak now.")
        try:
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=8)
            command = recognizer.recognize_google(audio).lower()
            st.success(f"Command recognized: {command}")
            return command
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            st.error("Network error. Please check your connection.")
            return None

# Improved fuzzy matching for commands
def fuzzy_match_command(command):
    possible_commands = [
        "show columns", "show first rows", "check missing values",
        "clean data", "show histogram", "show scatter plot",
        "show correlation heatmap", "export data", "exit"
    ]
    best_match, score = process.extractOne(command, possible_commands)
    return best_match if score > 60 else None

# Streamlit UI
st.title("Voice-Driven Data Analyst")

uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)

    st.success("Dataset loaded successfully!")

    if st.button("Show Columns"):
        st.write(df.columns.tolist())

    if st.button("Show First Rows"):
        st.write(df.head())

    if st.button("Check Missing Values"):
        st.write(df.isnull().sum())

    if st.button("Clean Dataset"):
        df.fillna(method='ffill', inplace=True)
        st.success("Missing values filled using forward fill.")

    if st.button("Export Data"):
        df.to_csv("processed_data.csv", index=False)
        st.success("Data exported successfully as 'processed_data.csv'.")

    # New Features: Visualization Options
    if st.button("Show Histogram"):
        column = st.selectbox("Select a column for histogram", df.select_dtypes(include='number').columns)
        plt.figure(figsize=(6, 4))
        sns.histplot(df[column], kde=True)
        st.pyplot(plt)

    if st.button("Show Correlation Heatmap"):
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        if numeric_df.shape[1] > 1:
            plt.figure(figsize=(8, 6))
            sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
            st.pyplot(plt)
            st.write("### Summary of Correlation Values:")
            st.write(numeric_df.corr())
        else:
            st.warning("Insufficient numeric data for correlation heatmap.")

    if st.button("Show Scatter Plot"):
        x_column = st.selectbox("Select X-axis column", df.select_dtypes(include='number').columns)
        y_column = st.selectbox("Select Y-axis column", df.select_dtypes(include='number').columns)
        plt.figure(figsize=(6, 4))
        sns.scatterplot(x=df[x_column], y=df[y_column])
        st.pyplot(plt)

    # Continuous Voice Command Mode
    if st.button("Start Continuous Voice Mode"):
        st.info("Listening continuously... Say 'exit' to stop.")
        st.write("### Available Commands:")
        st.write("- 'Show columns'")
        st.write("- 'Show first rows'")
        st.write("- 'Check missing values'")
        st.write("- 'Clean data'")
        st.write("- 'Show histogram'")
        st.write("- 'Show scatter plot'")
        st.write("- 'Show correlation heatmap'")
        st.write("- 'Export data'")
        st.write("- 'Exit' (to stop continuous listening)")

        while True:
            command = recognize_speech()
            if command:
                command = fuzzy_match_command(command)
                if command == "exit":
                    st.success("Voice mode ended.")
                    break
                elif command == "show columns":
                    st.write(df.columns.tolist())
                elif command == "show first rows":
                    st.write(df.head())
                elif command == "check missing values":
                    st.write(df.isnull().sum())
                elif command == "clean data":
                    df.fillna(method='ffill', inplace=True)
                    st.success("Missing values filled using forward fill.")
                elif command == "show histogram":
                    column = st.selectbox("Select a column for histogram", df.select_dtypes(include='number').columns)
                    plt.figure(figsize=(6, 4))
                    sns.histplot(df[column], kde=True)
                    st.pyplot(plt)
                elif command == "show correlation heatmap":
                    numeric_df = df.select_dtypes(include=['float64', 'int64'])
                    if numeric_df.shape[1] > 1:
                        plt.figure(figsize=(8, 6))
                        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
                        st.pyplot(plt)
                        st.write("### Summary of Correlation Values:")
                        st.write(numeric_df.corr())
                    else:
                        st.warning("Insufficient numeric data for correlation heatmap.")
                else:
                    st.error("Command not recognized. Try again.")
