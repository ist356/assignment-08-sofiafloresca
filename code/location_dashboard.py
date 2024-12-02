'''
location_dashboard.py
'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(layout="wide")
st.title('Top Locations of Parking Tickets in Syracuse')
tickets_df = pd.read_csv('./cache/tickets_in_top_locations.csv')
locations_df = pd.read_csv('./cache/top_locations.csv')
location = st.selectbox('Select a location', locations_df['location'])
if location:
    filtered = tickets_df[tickets_df['location'] == location]
    num_tickets = len(filtered)
    amount = filtered['amount'].sum()

    fig1, ax1 = plt.subplots()
    ax1.set_title('Tickets Issued by Hour of Day')
    sns.barplot(data=tickets_df, x='dayofweek', y='count', estimator = 'sum', ax=ax1, hue='dayofweek')
    
    fig2, ax2 = plt.subplots()
    ax2.set_title('Tickets Issued by Day of Week')
    sns.lineplot(data=tickets_df, x='hourofday', y='count', estimator='sum', ax=ax2) 
   
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total tickets issued", num_tickets)
        st.pyplot(fig1)

    with col2:
        st.metric("Total amount", f"${amount}")
        st.pyplot(fig2)
    st.map(filtered[['lat', 'lon']])
