
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
import sklearn.metrics as sm

data= pd.read_csv('final_data1.csv')
data=data.drop('Crop_Year', axis=1)
data=data.drop('State_Name',axis=1)
print(data)

#print(data.head(10))
#print(data.info())
#print(data.isnull().sum())
data=data.dropna()
#print(data.isnull().sum())


data['Area']=data['Area'].astype('float32')
data['Production']=data['Production'].astype('float32')


cropnames=[data.Crop.unique()]
#print(cropnames)
dictionary_crops={'Maize': 1, 'Arhar/Tur': 2, 'Bajra': 3, 'Gram': 4, 'Jowar': 5, 'Moong(Green Gram)': 6, 'Pulses total': 7, 'Ragi': 8, 'Rice': 9, 'Sugarcane': 10, 'Total foodgrain': 11, 'Urad': 12, 'Other  Rabi pulses': 13, 'Wheat': 14, 'Cotton(lint)': 15, 'Castor seed': 16, 'Groundnut': 17, 'Niger seed': 18, 'Other Cereals & Millets': 19, 'Other Kharif pulses': 20, 'Sesamum': 21, 'Soyabean': 22, 'Sunflower': 23, 'Linseed': 24, 'Safflower': 25, 'Small millets': 26, 'Rapeseed &Mustard': 27, 'other oilseeds': 28, 'Banana': 29, 'Grapes': 30, 'Mango': 31, 'Onion': 32, 'Tomato': 33, 'Tobacco': 34}
data['Crop']=data['Crop'].map(dictionary_crops)


#state_names=[data.State_Name.unique()]
#dictionary_states={'Andaman and Nicobar Islands':1, 'Andhra Pradesh':2, 'Arunachal Pradesh':3, 'Assam':4, 'Bihar':5, 'Chandigarh':6, 'Chhattisgarh':7, 'Dadra and Nagar Haveli':8, 'Goa':9, 'Gujarat':10, 'Haryana':11, 'Himachal Pradesh':12, 'Jammu and Kashmir':13, 'Jharkhand':14, 'Karnataka':15, 'Kerala':16, 'Madhya Pradesh':17, 'Maharashtra':18, 'Manipur':29, 'Meghalaya':20, 'Mizoram':21, 'Nagaland':22, 'Odisha':23, 'Puducherry':24, 'Punjab':25, 'Rajasthan':26, 'Sikkim':27, 'Tamil Nadu':28, 'Telangana':29, 'Tripura':30, 'Uttar Pradesh':31, 'Uttarakhand':32, 'West Bengal':33}
#data['State_Name']=data['State_Name'].map(dictionary_states)


district_names=[data.District_Name.unique()]
#print(district_names)
dictionary_districts={'AHMEDNAGAR': 1, 'AKOLA': 2, 'AMRAVATI': 3, 'AURANGABAD': 4, 'BEED': 5, 'BHANDARA': 6, 'BULDHANA': 7, 'CHANDRAPUR': 8, 'DHULE': 9, 'GADCHIROLI': 10, 'GONDIA': 11, 'HINGOLI': 12, 'JALGAON': 13, 'JALNA': 14, 'KOLHAPUR': 15, 'LATUR': 16, 'NAGPUR': 17, 'NANDED': 18, 'NASHIK': 19, 'OSMANABAD': 20, 'PARBHANI': 21, 'PUNE': 22, 'SANGLI': 23, 'SATARA': 24, 'THANE': 25, 'WARDHA': 26, 'WASHIM': 27, 'YAVATMAL': 28}
data['District_Name']=data['District_Name'].map(dictionary_districts)


season_names=[data.Season.unique()]
#print(season_names)
dictionary_seasons={'Kharif     ':1, 'Whole Year ':2, 'Autumn     ':3, 'Rabi       ':4, 'Summer     ':5, 'Winter     ':6}
data['Season']=data['Season'].map(dictionary_seasons)

dictionary_soil={'Sandy':1, 'Loamy':2, 'Silty':3, 'Clay':4}
data['Soil_Type']=data['Soil_Type'].map(dictionary_soil)


y=data.Production
X=data.drop('Production',axis=1)
print(X)
print(y)
X = np.nan_to_num(X) 


X_train, X_test, y_train, y_test= train_test_split(X, y, test_size=0.2, random_state=0)

print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)


from sklearn.ensemble import RandomForestRegressor
model= RandomForestRegressor(n_estimators=100)


model.fit(X_train, y_train)
y_pred=model.predict(X_test)


accuracy=sm.r2_score(y_test,y_pred)
print('Accuracy of build model is {:.2f}'.format(accuracy*100))


import joblib
joblib.dump(model, 'pickle_model2.pkl')
final_model= joblib.load('pickle_model2.pkl')
pred= final_model.predict(X_test)
accuracy=sm.r2_score(y_test,y_pred)

print("Accuracy of final model is {:.2f}".format(accuracy*100))



