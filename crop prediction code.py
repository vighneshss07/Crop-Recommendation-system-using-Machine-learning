import pyttsx3 
import pandas as pd
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier 
import numpy as np
import PySimpleGUI as sg

# Read the dataset
cr = pd.read_csv(r"d:\Users\Admin\Desktop\C_R.csv") 
print(cr)
print(cr.shape)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices') 
rate = engine.getProperty('rate') 
engine.setProperty('rate', rate-20) 
engine.setProperty('voice',voices[0].id)
 
def speak(audio):
    engine.say(audio) 
    engine.runAndWait()

le = preprocessing.LabelEncoder() 
crop = le.fit_transform(list(cr["label"]))

NITROGEN = list(cr["N"]) 
PHOSPHORUS = list(cr["P"]) 
POTASSIUM = list(cr["K"])
TEMPERATURE = list(cr["Temperature"]) 
HUMIDITY = list(cr["Humidity"])
PH = list(cr["ph"])
RAINFALL = list(cr["Rainfall"])
 
features = np.array([NITROGEN, PHOSPHORUS, POTASSIUM, TEMPERATURE, HUMIDITY, PH, RAINFALL]).transpose()
print(features.shape) 
print(crop.shape)

model = KNeighborsClassifier(n_neighbors=3) 
model.fit(features, crop)

layout = [[sg.Text('Crop Recommender', font=("Helvetica", 30), text_color='Pink')],
          [sg.Text('Please enter the following details :-', font=("Helvetica", 20), text_color='Yellow')],
          [sg.Text('Enter ratio of Nitrogen in the soil:', font=("Helvetica", 20)), sg.Input(font=("Helvetica",20), size=(20,1))],
          [sg.Text('Enter ratio of Phosphorous in the soil:', font=("Helvetica", 20)), sg.Input(font=("Helvetica",20), size=(20,1))],
          [sg.Text('Enter ratio of Potassium in the soil:', font=("Helvetica", 20)), sg.Input(font=("Helvetica",20), size=(20,1))],
          [sg.Text('Enter average Temperature value around the field:', font=("Helvetica", 20)), sg.Input(font=("Helvetica",20), size=(20,1)), sg.Text('*C', font=("Helvetica", 20))],
          [sg.Text('Enter average percentage of Humidity around the field:', font=("Helvetica", 20)), sg.Input(font=("Helvetica",20), size=(20,1)), sg.Text('%', font=("Helvetica", 20))],
          [sg.Text('Enter PH value of the soil:', font=("Helvetica", 20)), sg.Input(font=("Helvetica",20), size=(20,1))],
          [sg.Text('Enter average amount of Rainfall around the field:', font=("Helvetica", 20)), sg.Input(font=("Helvetica",20), size=(20,1)), sg.Text('mm', font=("Helvetica", 20))],
          [sg.Text(size=(50,1), font=("Helvetica", 20), text_color='yellow', key='-OUTPUT1-')],
          [sg.Button('Submit', font=("Helvetica", 20)), sg.Button('Quit', font=("Helvetica", 20))]]

window = sg.Window('Crop Recommendation Assistant', layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break 

    nitrogen_content = values[0] 
    phosphorus_content = values[1] 
    potassium_content = values[2] 
    temperature_content = values[3]
    humidity_content = values[4] 
    ph_content = values[5] 
    rainfall = values[6]

    # Convert user input to numeric values
    predict1 = np.array([nitrogen_content, phosphorus_content, potassium_content, temperature_content, humidity_content, ph_content, rainfall], dtype=float)
    predict1 = predict1.reshape(1,-1) 
    predict1 = model.predict(predict1) 

    crop_name = le.inverse_transform(predict1)[0]

    if 1 <= int(humidity_content) <= 33 :
        humidity_level = 'low humid'
    elif 34 <= int(humidity_content) <= 66: 
        humidity_level = 'medium humid'
    else:
        humidity_level = 'high humid'
    
    if 0 <= int(temperature_content) <= 6: 
        temperature_level = 'cool'
    elif 7 <= int(temperature_content) <= 25: 
        temperature_level = 'warm'
    else:
        temperature_level = 'hot'
    
    if 1 <= int(rainfall) <= 100: 
        rainfall_level = 'less'
    elif 101 <= int(rainfall) <= 200: 
        rainfall_level = 'moderate'
    else:
        rainfall_level = 'heavy rain'
    
    if 1 <= int(nitrogen_content) <= 50: 
        nitrogen_level = 'less'
    elif 51 <= int(nitrogen_content) <= 100: 
        nitrogen_level = 'not to less but also not to high'
    else:
        nitrogen_level = 'high'

    if 1 <= int(phosphorus_content) <= 50: 
        phosphorus_level = 'less'
    elif 51 <= int(phosphorus_content) <= 100: 
        phosphorus_level = 'not to less but also not to high'
    else:
        phosphorus_level = 'high'

    if 1 <= int(potassium_content) <= 50: 
        potassium_level = 'less'
    elif 51 <= int(potassium_content) <= 100: 
        potassium_level = 'not to less but also not to high'
    else:
        potassium_level = 'high'
    
    if 0 <= float(ph_content) <= 5: 
        phlevel = 'acidic'
    elif 6 <= float(ph_content) <= 8: 
        phlevel = 'neutral'
    else:
        phlevel = 'alkaline'

    speak(f"Sir, according to the data provided, the ratio of nitrogen in the soil is {nitrogen_level}, phosphorus is {phosphorus_level}, potassium is {potassium_level}, temperature is {temperature_level}, humidity is {humidity_level}, pH is {phlevel}, and the amount of rainfall is {rainfall_level}.")

    window['-OUTPUT1-'].update('The best crop that you can grow : ' + crop_name) 
    speak("The best crop that you can grow is " + crop_name)

window.close()
