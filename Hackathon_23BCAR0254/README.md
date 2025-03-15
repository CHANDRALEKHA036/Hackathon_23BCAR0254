# Voice-Driven Data Analyst

This is a Streamlit-based voice assistant for data analysis. It supports various tasks like data visualization, cleaning, and exploring datasets through voice commands.

## How to Run the App
1. **Clone the Repository**  
Run this command in your terminal or command prompt:  
```
git clone https://github.com/CHANDRALEKHA036/Hackathon_23BCAR0254.git
cd Hackathon_23BCAR0254/Hackathon_23BCAR0254
```

2. **Install Dependencies**  
Run this command to install the required libraries:  
```
pip install -r requirements.txt
```

3. **Run the App**  
Run the following command to start the application:  
```
streamlit run "Voice Data App.py"
```

4. **Using Voice Commands**  
Once the app opens:
- Upload a CSV or Excel dataset.
- Use voice commands like:
  - **"Show columns"**
  - **"Show first rows"**
  - **"Check missing values"**
  - **"Show histogram"**
  - **"Show correlation heatmap"**
  - **"Exit"** (to stop continuous voice mode).

5. **Troubleshooting**  
- If errors occur with `speechrecognition`, check microphone permissions.
- If libraries are missing, run `pip install -r requirements.txt` again.
