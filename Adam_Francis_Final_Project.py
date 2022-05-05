"""
Name: Adam Francis
CS230: Section 1
Data: Properties in Cambridge, MA
URL: Link to your web application online

Description: This program gives information about properties in Cambridge Massachussets, such as...
all the properties that are under an assessed value. The module I used that we have not is plotly, which...
is another popular plotting module for python.
"""
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas
import plotly.express as px
from matplotlib import pyplot as plt

#read in the data
def get_data():
    return pd.read_csv('Cambridge_Property_Database_FY2022_8000_sample.csv')

#finds all properties in the cambridge area with the given parameters
def query1(data, select_class = 'CNDO LUX', assessed_price = 5000000):
    df = data[(data['AssessedValue'] < assessed_price) & (data['PropertyClass'] == select_class)]
    COLUMNS = ('address', 'latitude', 'longitude')
    locations = df[['Address', 'Latitude', 'Longitude']]
    locations.columns = COLUMNS
    return locations

def query2(data):
    clean_data = data[(data['PropertyTaxAmount'] > 100) & (data['AssessedValue'] < 750000)]
    df = pd.pivot_table(data=clean_data, index=['AssessedValue'], values=['PropertyTaxAmount'])
    house_value = clean_data['AssessedValue']
    property_tax = clean_data['PropertyTaxAmount']
    fig = px.scatter(x = house_value, y = property_tax, labels={'x':'Property Value', 'y':'Property tax'},title="Property taxes based off property value")
    return fig, df

def query4(data):
    fig,ax = plt.subplots()
    clean_data = data[(data["LandArea"] > 0) & (data['LandArea'] < 5000)]
    #calculate land values
    max_land_area = int(clean_data["LandArea"].max())
    mean_land_area = int(clean_data['LandArea'].mean())
    min_land_area = int(clean_data["LandArea"].min())

    land_labels = ['most land', 'average land amount', 'least land']
    land_values = [max_land_area, mean_land_area, min_land_area]

    ax.set_title('Amount of land for the highest, average, and least amount of land')
    ax.bar(land_labels, land_values, color='g')
    ax.set_ylabel("Land in square feet")
    ax.set_xlabel("Land amounts")
    return plt



def query5(data):
    fig,ax = plt.subplots()
    total = len(data)
    df = data[data['ResidentialExemption'] == True]
    exempt = len(df)
    not_exempt = total - exempt
    label = ['Resedential Exemptions', 'Non Residential Exemptions']
    list = [exempt, not_exempt]
    ax.pie(list, labels=label, autopct='%1.2f%%')
    return plt

def mapping(locations):
    try:
        st.map(locations)
    except:
        st.write("Map cannot be displayed Null values detected")
        pass

def map_inputs(property_classes):
    st.sidebar.header("Enter values then click button")
    select_class = st.selectbox('What type of property are you looking for?', property_classes)
    assessed_price = st.number_input('Property Price Limit')
    button = st.sidebar.button('Get map')

    return select_class, assessed_price, button

def main():

    st.set_page_config(page_title= "Cambridge Properties", page_icon= "Web_icon.jpg")
    page = st.sidebar.selectbox("Page: ", ('1','2','3', '4', '5'))
    data = get_data() # call the get_data() function and place it into the data variable
    property_classes = data.PropertyClass.unique() # find all property classes that are unique

    #checks to see what page you are on and displays the relevant information
    if page == '1':
        st.font = 'lobster'
        st.header("Welcome to Adam Francis' Website")
        st.subheader('This project is about properties in Cambridge, MA')
        st.image('cambridge_photo.jpg')
    elif page == '2':
        st.header("Finding specific properties by price")
        select_class, assessed_price, button = map_inputs(property_classes)
        locations = query1(data, select_class, assessed_price)
        if button:
            mapping(locations)
            st.dataframe(locations)
    elif page == '3':
        st.header('Scatterplot of property taxes based off assessed value')
        st.write('Of houses under 750k Assessed Value')
        c1, c2 = st.columns(2)
        fig, df = query2(data)
        st.plotly_chart(fig)
        df = df.sort_values(['PropertyTaxAmount'], ascending=True)
        st.write('Data Frame of the property tax amounts in ascending order')
        st.dataframe(df)
        #fig.show()

    elif page == '4':
        st.header('Land prices')
        st.write('For land sized under 5000 sqf and above 0 sqf')
        st.pyplot(query4(data))

    elif page == '5':
        st.header('Percent of Properties that are residential exemptions')
        st.pyplot(query5(data))

main()

