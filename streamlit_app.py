from collections import namedtuple
import altair as alt
import math

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

"""
# Welcome to the Quick Recovery Tool!

With this visualization, your breakdown service can be brought to the next level.

By selecting the region of your interest, you can get insights on the trends within these regions regarding car accidents.
There is also a map provided to gain a geographical overview of where your employees will most likely be necessary during their work hours.
"""

# The code below is all created for the Data Visualization Final Project
with st.echo(code_location='below'):
    # SQ1 --> Heat Map
    df = pd.read_csv("dft-road-casualty-statistics-accident-2020.csv")

    # Read the longitude and latitude and drop empty rows
    map = pd.DataFrame()
    map['latitude'] = df['latitude'].dropna()
    map['longitude'] = df['longitude'].dropna()
    st.map(map)

    # Selection Box
    guide = pd.read_csv("regions-labels.csv")
    guide = pd.Series(guide.label.values, index=guide.id).to_dict()
    medium = df.local_authority_district.unique().tolist()

    # Remove instances where the local_authority_district was -1
    medium.remove(-1)

    # Create a sorted list with all regions
    region_setup = []
    for item in medium:
        region_name = guide[item]
        region_setup.append(region_name)
    region_setup = sorted(region_setup)

    # Transform the list to a Pandas dataframe and create a list with all the codes in order to link code and region
    region = pd.Series(region_setup, index=medium).to_dict()
    region_rev = pd.Series(medium, index=region_setup).to_dict()
    option_setup = st.selectbox("Which region do you want to view?", sorted(region.values()))
    option = region_rev[option_setup]

    # SQ2 --> Create a Pie Chart with the overturn type distribution
    df_v = pd.read_csv("dft-road-casualty-statistics-vehicle-2020.csv", low_memory=False)
    df_v = df_v.drop(df_v.index[df_v['skidding_and_overturning'] == -1])

    # Merge the overturn variable of the vehicles dataset with the accidents dataset
    df_s = df[['accident_index', 'local_authority_district']]
    df_m = pd.merge(df_v, df_s, on="accident_index")
    df_2 = df_m.loc[df_m['local_authority_district'] == option]

    # Fill a list with the counts of overturning types
    turnover = [0,0,0,0,0,0,0]
    for item in df_2['skidding_and_overturning']:
        if item == 9:
            turnover[5] += 1
        else:
            turnover[item] += 1

    # Plot the pie chart
    fig1, ax1 = plt.subplots()
    labels = '0 = None', '1 = Skidded', '2 = Skidded and Overturned', '3 = Jackknifed', '4 = Jackknifed and Overturned', '5 = Overturned', '9 = Unknown'
    ax1.pie(turnover, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    fig1.legend()

    st.pyplot(fig1)


    # SQ3 --> Create a Bar Chart with the severity level
    labels = 'Slight', 'Serious', 'Fatal'
    df_3 = df.loc[df['local_authority_district'] == option]

    severity_count_setup = df_3['accident_severity'].value_counts().tolist()
    severity_count = pd.DataFrame(severity_count_setup, index=['1 = Slightly', '2 = Serious', '3 = Fatal'])

    st.bar_chart(severity_count)

    # SQ4 --> Create a Line Chart with the accident trends per month
    df_4 = df.loc[df['local_authority_district'] == option]

    datetime = pd.to_datetime(df_4['date'], infer_datetime_format=True)
    month = datetime.dt.month
    month = month.value_counts().tolist()

    month_count = pd.DataFrame(month,
                                  index=['01 = January', '02 = February', '03 = March', '04 = April', '05 = May', '06 = June', '07 = July', '08 = August', '09 = September', '10 = October', '11 = November', '12 = December'])
    st.line_chart(month_count)

    # SQ5 --> Create a Bar Chart with accidents per day of the week
    df_5 = df.loc[df['local_authority_district'] == option]

    week_count_setup = df_5['day_of_week'].value_counts().tolist()
    week = np.divide(week_count_setup, 52)

    severity_count = pd.DataFrame(week, index=['1 = Monday', '2 = Tuesday', '3 = Wednesday', '4 = Thursday', '5 = Friday', '6 = Saturday', '7 = Sunday'])
    st.bar_chart(severity_count)
