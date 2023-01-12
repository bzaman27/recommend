# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 18:43:59 2023

@author: Bushra
"""
#from flask import Flask, render_template, request, Markup
import numpy as np
import pickle
import pandas as pd
from PIL import Image
import jsonify
import json
import requests
import sklearn
from sklearn.preprocessing import StandardScaler
import streamlit as st

#app = Flask(__name__)
crop_recommendation_model = pickle.load(open('RandomForest.pkl', 'rb'))
#@app.route('/',methods=['GET'])
def welcome():
    return "Welcome All"

def weather_fetch(city_name):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    api_key = "9762f6211b8885103b23e53733cf933c"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    #https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}

    complete_url = base_url + "q=" + city_name +"&appid=" + api_key
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    else:
        return None
    
   
def crop_recommend(N, P, K, temperature, humidity, ph, rainfall):
    
    """Let's Predict the Crop Yield 
    This is using docstrings for specifications.
    ---
    parameters:  
      - name: N
        in: query
        type: number
        required: true
      - name: P
        in: query
        type: number
        required: true
      - name: K
        in: query
        type: number
        required: true
      - name: temperature
        in: query
        type: number
        required: true
      - name: humidity
        in: query
        type: number
        required: true
      - name: ph
        in: query
        type: number
        required: true
      - name: rainfall
        in: query
        type: number
        required: true
    responses:
        200:
            description: The output values
        
    """
   
    prediction=crop_recommendation_model.predict([[N, P, K, temperature, humidity, ph, rainfall]])
    print(prediction)
    return prediction 
   
def main():
    st.title("Crop Recommendation")
    html_temp = """
    <div style="background-color:green;padding:10px">
    <h2 style="color:white;text-align:center;">Crop Recommendation ML App </h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    N = st.text_input("nitrogen", "Enter value")
    P = st.text_input("phosphorous", "Enter value")
    K = st.text_input("pottasium", "Enter value")
    ph = st.text_input("ph", "Enter value")
    rainfall = st.text_input("rainfall", "Enter value")
    
    #state = request.form.get("stt")
    #city = st.text.input(request.form.get("city"))
    #city = st.selectbox("city", cities_1) 
    #city = request.form.get("city")
    city=st.text_input("city", "Enter value")
    if weather_fetch(city) != None:
        temperature, humidity = weather_fetch(city)
        return temperature, humidity
    if st.button("Predict"):
        result=crop_recommend(N, P, K, temperature, humidity, ph, rainfall)
        st.success('You can grow [ {} ]'.format(result))
        if st.button("About"):
            st.text("Lets Learn")
            st.text("Built with Streamlit")    
    result=""
    
if __name__=='__main__':
    main()