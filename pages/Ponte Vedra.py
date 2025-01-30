###### Import Packages
import pandas as pd
import numpy as np
import streamlit as st
import openpyxl
from datetime import datetime, timedelta


###########Coefficients for Ponte Vedra Campus

coefficients = {
    '09:00:00': {
        'intercept' : 45.8364,
        'sunday_date' :-0.0013, 
        'week_number' : -0.0119,
        'Guest Pastor' : -1.708413,
        'Executive Pastor' :  -1.202008,
        'Pastor Joby' : 0.983648,
        'Easter' : 4.9653,
       	'Promotion Week' : 1.4468,
        'Back to School' : 1.4468,
        'Saturated Sunday' : 1.9425,
        'kids_projection' : 0.22,
        'kids_easter' : .12,
        'Christmas' : 3.021,
        'Inclement Weather' : .15
        

    },
    
  '11:22:00': {

       	'intercept' : 19.6101,
       	'sunday_date' : -0.0002,
        'week_number' : -0.0174,
       	'Guest Pastor' :  -1.751985,
      	'Executive Pastor' : -1.373052,
       	'Pastor Joby' : 0.204181,
        'Easter' : 6.1558,
        'Promotion Week' : 1.952,
        'Back to School' : 1.952,
        'Saturated Sunday' : 3.5193,
        'kids_projection' : .15,
        'kids_easter' : .12,
        'kids_labor' : 17.64,
        'Christmas' : 4.3488,
        'Inclement Weather' : .15
    },
    
}


### logo
logo_file = "https://raw.githubusercontent.com/aarmobley/CoE22/main/E22%20Logo.png"
st.image(logo_file, width=150)


with st.sidebar:
    st.markdown("""
                Important Dates: 
                - 08-11-2024 (Promotion Week)  
                - 09-15-2024 (Saturated)
                - 12-22-2024 (Christmas)
                - 01-05-2025 (Back to School)
                - 04-20-2025 (Easter) """)

title = st.title("Ponte Vedra Attendance Projection")




##### number of weeks for projecting out - 104 weeks
num_week = [week for _ in range(2) for week in range(1, 53)]
if len(num_week) < 104:
    num_week.apend(53)
#momentum = ['Easter', 'Back to School-August', 'Christmas', 'Back to School-January', 'Easter 2025']


##listing service times based on coefficients
service_times = list(coefficients.keys()) 


##create dates for 2 year projection
start_date = datetime(2025, 1, 5)  # Start date
date_range = [start_date + timedelta(weeks=i) for i in range(104)]  # 104 weeks range

# Create date mapping with numerical values as days since Unix epoch (1970-01-01)
epoch = datetime(1970, 1, 1)
date_mapping = {date.strftime('%m-%d-%Y'): (date - epoch).days for date in date_range}


#creating sunday date and week numbers for same drop down
date_week_options = [f"{date.strftime('%m-%d-%Y')} (Week {week})" for date, week in zip(date_range, num_week)]

#select box for sunday date and wekk number
date_options = st.selectbox("Select Sunday Date", date_week_options)                                                    #list(date_mapping.keys())


selected_date_str = date_options.split(' ')[0]
select_week = int(date_options.split('Week ')[-1].strip(')'))



#list events


event_options = ['None', 'Easter', 'Promotion Week', 'Saturated Sunday', 'Christmas', 'Back to School']

#iw = ['Yes', 'No']

####creating selectbox options
#select_date = st.selectbox("Select a Sunday Date", date_options)

#select_week = st.selectbox("Select Week Number", num_week)

select_service = st.selectbox("Select a Service", service_times)


select_event = st.selectbox("Select Event", event_options)




numerical_date = date_mapping[selected_date_str]                                                         #numerical_date = date_mapping[select_date]

service_options = coefficients[select_service]

weeknum_effect = service_options['week_number'] * (select_week)
sundaydate_effect = service_options['sunday_date'] * (numerical_date)


### No Event coefficient needs to be 0
no_event = 0

if select_event != 'None':
    no_event = service_options[select_event]



####predict button

if st.button("Make Projection"):
    
        

        # Calculate prediction for the selected service
    prediction = ((service_options['intercept']) + sundaydate_effect + weeknum_effect + no_event)
    prediction1 = prediction ** 2
    
    kids_1122 = prediction1 * service_options['kids_projection']
    
    kids_easter = prediction1 * service_options['kids_easter']
    
    #kids_labor = prediction1 * service_options['kids_labor']
    
    
    capacity = prediction1 / 545 * (100)
    
    kids_capacity = kids_1122 / 210 * (100)
    
    kids_easter_capacity = kids_easter / 210 *(100)
    
        
    

    
    #divider before projected attendance
    st.divider()
    
    st.write(f"Projected Adult Attendance: {prediction1:.0f}")
    
    
    ### HTML and MArkdown for adult capacity
    color = "red" if capacity > 80 else "blue"
    
    st.markdown(f"<p style='color:{color}; font-size:18px;'>Capacity: {capacity:.0f}%</p>", unsafe_allow_html=True)                                       #st.write(f"Adult Capacity: {capacity: .0f}%")
    
    
  

    ###st.write(f"Weekly Total: {select_service: .0f} ")
    #####
    st.divider()
    
    
    if select_event == 'Easter':
        st.write(f"Projected Kids Attendance: {kids_easter: .0f}")
        color = "red" if kids_capacity > 80 else "blue"
        st.markdown(f"<p style='color:{color}; font-size:18px;'>Capacity: {kids_easter_capacity:.0f}%</p>", unsafe_allow_html=True)
    
    else: 
        st.write(f"Projected Kids Attendance: {kids_1122: .0f}")
         ## HTML and markdown for kids capacity
        color = "red" if kids_capacity > 80 else "blue"
        st.markdown(f"<p style='color:{color}; font-size:18px;'>Capacity: {kids_capacity:.0f}%</p>", unsafe_allow_html=True)
        