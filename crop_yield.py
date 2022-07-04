
from flask import render_template, request, jsonify, Flask
import joblib
import numpy as np
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb
import MySQLdb
import requests



gmail_list=[]
password_list=[]
gmail_list1=[]
password_list1=[]

dictionary_crops={'Maize': 1, 'Arhar/Tur': 2, 'Bajra': 3, 'Gram': 4, 'Jowar': 5, 'Moong(Green Gram)': 6, 'Pulses total': 7, 'Ragi': 8, 'Rice': 9, 'Sugarcane': 10, 'Total foodgrain': 11, 'Urad': 12, 'Other  Rabi pulses': 13, 'Wheat': 14, 'Cotton(lint)': 15, 'Castor seed': 16, 'Groundnut': 17, 'Niger seed': 18, 'Other Cereals & Millets': 19, 'Other Kharif pulses': 20, 'Sesamum': 21, 'Soyabean': 22, 'Sunflower': 23, 'Linseed': 24, 'Safflower': 25, 'Small millets': 26, 'Rapeseed &Mustard': 27, 'other oilseeds': 28, 'Banana': 29, 'Grapes': 30, 'Mango': 31, 'Onion': 32, 'Tomato': 33, 'Tobacco': 34}


dictionary_seasons={'Kharif     ':1, 'Whole Year ':2, 'Autumn     ':3, 'Rabi       ':4, 'Summer     ':5, 'Winter     ':6}


dictionary_districts={'AHMEDNAGAR': 1, 'AKOLA': 2, 'AMRAVATI': 3, 'AURANGABAD': 4, 'BEED': 5, 'BHANDARA': 6, 'BULDHANA': 7, 'CHANDRAPUR': 8, 'DHULE': 9, 'GADCHIROLI': 10, 'GONDIA': 11, 'HINGOLI': 12, 'JALGAON': 13, 'JALNA': 14, 'KOLHAPUR': 15, 'LATUR': 16, 'NAGPUR': 17, 'NANDED': 18, 'NASHIK': 19, 'OSMANABAD': 20, 'PARBHANI': 21, 'PUNE': 22, 'SANGLI': 23, 'SATARA': 24, 'THANE': 25, 'WARDHA': 26, 'WASHIM': 27, 'YAVATMAL': 28}

dictionary_soil={'Sandy':1, 'Loamy':2, 'Silty':3, 'Clay':4}

model1=joblib.load('pickle_model2.pkl')

app= Flask(__name__)

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def register():
    int_features2= [str(x) for x in request.form.values()]
    r1=int_features2[0]
    print(r1)

    r2=int_features2[1]
    print(r2)
    logi1=int_features2[0]
    passw1=int_features2[1]
    
    import MySQLdb
    db= MySQLdb.Connect("localhost","root","","ddbb")
    cursor=db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()

    for row1 in result1:
        print(row1)
        print(row1[0])
        gmail_list1.append(str(row1[0]))


    print(gmail_list)
    if logi1 in gmail_list1:
        return render_template('register.html', text="This username is already in use")
    else: 


        sql= "INSERT INTO user_register(user,password) VALUES (%s,%s)"
        val=(r1,r2)

        try:
            cursor.execute(sql,val)
            db.commit()

        except:
            db.rollback()

        db.close()
        return render_template('register.html',text="Successfully registered")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logedin', methods=['POST'])
def logedin():
    int_features3=[str(x) for x in request.form.values()]
    print(int_features3)
    logi=int_features3[0]
    passw=int_features3[1]

    import MySQLdb

    db= MySQLdb.Connect("localhost","root","","ddbb")

    cursor= db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()

    for row1 in result1:
        print(row1)
        print(row1[0])
        gmail_list.append(str(row1[0]))

    print(gmail_list)

    cursor1=db.cursor()
    cursor1.execute("SELECT password FROM user_register")
    result2=cursor1.fetchall()

    for row2 in result2:
        print(row2)
        print(row2[0])
        password_list.append(str(row2[0]))

    print(password_list)
    print(gmail_list.index(logi))
    print(password_list.index(passw))

    if gmail_list.index(logi)==password_list.index(passw):
        return render_template('yield.html')
    else:
        return render_template('login.html',text='The proper username and password')

@app.route('/production',methods=['POST'])
def production():
    int_features1=[str(x) for x in request.form.values()]
    print(int_features1)
    a=int_features1
    district=a[0]
    season=a[1]
    crop=a[2]
    soil=a[3]
    area=int(a[4])

    r=requests.get('https://api.openweathermap.org/data/2.5/weather?q={0}&appid=725e4455b846393b3b21618426c4a059'.format(district))
    param= r.json()
    print(param)
    temp_k=float(param['main']['temp'])
    temp=temp_k-273
    humi= float(param['main']['humidity'])
    rainfall=87.38

    data = { 'District Name':[district], 'Season':[season], 'Crop':[crop], 'Soil':[soil], 'Area':[area], 'Temperature':[temp], 'Precipitation':[rainfall],'Humidity':[humi]}
    df=pd.DataFrame(data)
    print(df)
    

    
    df['District Name']=df['District Name'].map(dictionary_districts)
    df['Season']=df['Season'].map(dictionary_seasons)
    df['Crop']=df['Crop'].map(dictionary_crops)
    df['Soil']=df['Soil'].map(dictionary_soil)
    
    prediction=model1.predict(df)
    prediction=int(prediction)/10
    print(prediction)

    return render_template('yield.html',prediction_text="You will get yield of {} tonnes".format(prediction))

@app.route('/yield')
def yield1():
    return render_template('yield.html')
    
if __name__=="__main__":
    app.run(debug=False)

#AdaBoost, short for Adaptive Boosting, is a statistical classification meta-algorithm formulated by Yoav Freund and Robert Schapire, who won the 2003 Gödel Prize for their work. It can be used in conjunction with many other types of learning algorithms to improve performance. The output of the other learning algorithms ('weak learners') is combined into a weighted sum that represents the final output of the boosted classifier. AdaBoost is adaptive in the sense that subsequent weak learners are tweaked in favor of those instances misclassified by previous classifiers. In some problems it can be less susceptible to the overfitting problem than other learning algorithms. The individual learners can be weak, but as long as the performance of each one is slightly better than random guessing, the final model can be proven to converge to a strong learner.    

                   





    



