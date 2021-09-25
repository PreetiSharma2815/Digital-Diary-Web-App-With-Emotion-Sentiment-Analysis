from flask import Flask, render_template, request, redirect, jsonify, json, flash
from datetime import datetime
from datetime import date
from model_prediction import *
import os

import tzlocal 
import pytz

port = int(os.environ.get("PORT", 5000))
# print(port)

# Flask Object
app = Flask(__name__)

#app.secret_key = 'SecretKey'

# Get datetime specific to local timezone
# tz = pytz.timezone(str(tzlocal.get_localzone()))
# localtime_now = datetime.now(tz)

# print(tzlocal.get_localzone())
# print(localtime_now)

# Date Today
# date_time = date.today().strftime("%A %d %B %Y")
# date_time = localtime_now.strftime("%A %d %B %Y")

# Global Variables
text=""
predicted_emotion=""
predicted_emotion_img_url=""

# Define API Routes
@app.route("/", methods=["GET"])
def home():
    
    local_datetime=""
    if request.method == "GET":      
        # Get Top 3 dates, text entries, emotion and url
        date1, date2, date3 ,entry1, entry2, entry3, emotion1, emotion2, emotion3,emotion_url_1,emotion_url_2,emotion_url_3 = show_entry()
    
        # Render HTML Page
        return render_template("index.html", InputText=text, Predicted_Emotion=predicted_emotion,predicted_emotion_img_url=predicted_emotion_img_url, Date1=date1.strftime("%A, %d %B %Y"),Entry1=entry1, emotion_img_url_1=emotion_url_1, Emotion1=emotion1,Date2=date2.strftime("%A, %d %B %Y"),Entry2=entry2,  emotion_img_url_2=emotion_url_2, Emotion2=emotion2,Date3=date3.strftime("%A, %d %B %Y"),Entry3=entry3, emotion_img_url_3=emotion_url_3, Emotion3=emotion3)
    

@app.route("/predict-emotion", methods=["GET", "POST"])
def predict_emotion():
        if request.method == "POST":
            input_text = request.json.get("text")
           
            if input_text!="":
                predicted_emotion, predicted_emotion_img_url = predict(input_text)                         
                return jsonify([predicted_emotion, predicted_emotion_img_url])
        

@app.route("/save-entry", methods=["GET", "POST"])
def save_entry():
        if request.method == "POST":
            date = request.json.get("date")            
            save_text = request.json.get("text")
            emotion = request.json.get("emotion")
         
            entry = f'"{date}","{save_text}","{emotion}"\n'         
            with open("./static/assets/data_files/data_entry.csv", "a") as f:
                f.write(entry)
            return jsonify("Success")
           
                
    