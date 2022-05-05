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
import plotly.express as px
from matplotlib import pyplot as plt

#read in the data
def get_data():
    return pd.read_csv('Cambridge_Property_Database_FY2022_8000_sample.csv')

#finds all properties in the cambridge area with the given parameters
def map_data(data, select_class = 'CNDO LUX', assessed_price = 5000000):
    df = data[(data['AssessedValue'] < assessed_price) & (data['PropertyClass'] == select_class)]
    COLUMNS = ('address', 'latitude', 'longitude')
    locations = df[['Address', 'Latitude', 'Longitude']]
    locations.columns = COLUMNS
    return locations

def property_tax(data, select_property_price = 500000, select_tax = 100): #graphs property tax data
    clean_data = data[(data['PropertyTaxAmount'] > select_tax) & (data['AssessedValue'] < select_property_price)]
    df = pd.pivot_table(data=clean_data, index=['AssessedValue'], values=['PropertyTaxAmount'])
    house_value = clean_data['AssessedValue']
    property_tax = clean_data['PropertyTaxAmount']
    fig = px.scatter(x = house_value, y = property_tax, labels={'x':'Property Value', 'y':'Property tax'},title="Property taxes based off property value")
    return fig, df

def land_data(data): #gets data for land and charts it
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

def residential_exemptions(data): #pie chart of residential_exemptions
    fig,ax = plt.subplots()
    #gets total of number of data entries
    total = len(data)
    df = data[data['ResidentialExemption'] == True]
    exempt = len(df)
    not_exempt = total - exempt
    label = ['Resedential Exemptions', 'Non Residential Exemptions']
    list = [exempt, not_exempt]
    ax.pie(list, labels=label, autopct='%1.2f%%')
    return plt

def mapping(locations): #maps the data unless
    #makes sure there is no error if faults in data
    try:
        st.map(locations)
    except:
        pass

def map_inputs(property_classes): #gets map inputs for map
    st.sidebar.header("Enter values then click button")
    select_class = st.selectbox('What type of property are you looking for?', property_classes)
    assessed_price = st.number_input('Property Price Limit')
    button = st.sidebar.button('Get map')

    return select_class, assessed_price, button

def tax_inputs(): #gets property tax inputs for graph
    #sidebar button
    st.sidebar.header("Enter values then click button")
    select_property_price = st.number_input('House prices less than:')
    select_tax = st.number_input('Property taxes greater than:')

    tax_button = st.sidebar.button('Update Graph')

    return select_property_price, select_tax, tax_button

def main():
    #sets up the page and gets key information
    num_pages = [str(i) for i in range(1,6)]  #creates the number of pages for the website using list comprehension
    pages = tuple(num_pages) #puts it into a tuple to protect it from changing
    st.set_page_config(page_title= "Cambridge Properties", page_icon= "Web_icon.jpg")
    page = st.sidebar.selectbox("Page: ", pages)
    data = get_data() # call the get_data() function and place it into the data variable
    property_classes = data.PropertyClass.unique() # find all property classes that are unique

    #checks to see what page you are on and displays the relevant information
    if page == '1': #1rst page
        st.header("Welcome to Adam Francis' Website")
        st.subheader('This project is about properties in Cambridge, MA')
        st.image('cambridge_photo.jpg')
    elif page == '2': #2nd page
        st.header("Finding specific properties by price")
        select_class, assessed_price, button = map_inputs(property_classes)
        locations = map_data(data, select_class, assessed_price)
        if button:
            mapping(locations)
            st.dataframe(locations)
    elif page == '3': #3rd page
        select_property_price, select_tax, tax_button = tax_inputs()

        st.header('Scatterplot of property taxes based off assessed value')
        st.write('Of houses under specified Assessed Value and property taxes over specified amount')
        if tax_button:
            try:
                fig, df = property_tax(data, select_property_price, select_tax)
                st.plotly_chart(fig)
                st.write('Error invalid inputs')
                df = df.sort_values(['PropertyTaxAmount'], ascending=True)
                st.write('Data Frame of the property tax amounts in ascending order')
                st.dataframe(df)
            except:
                st.write('Invalid Inputs')

    elif page == '4': #4th page
        st.header('Land prices')
        st.write('For land sized under 5000 sqf and above 0 sqf')
        st.pyplot(land_data(data))

    elif page == '5': #5th page
        st.header('Percent of Properties that are residential exemptions')
        st.pyplot(residential_exemptions(data))
main()

