import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from visualisation_functions import (create_bar_chart_with_rolling_average,
                                     create_scatter_plot_with_rolling_average,
                                     create_histogram_with_colours,
                                     create_boxplot,
                                     create_histogram
                                     )

st.title('Sleep data visualisations')

import streamlit as st
from PIL import Image

# 24 hour visualisation of all her sleeps
image = Image.open('pics/24_hour_sleep_plot.png')

# Display image
st.image(image, use_column_width=True)

# load data
ember_sleep_df = pd.read_csv('data/ember_sleep_30march_updated.csv')
ember_sleep_df['sleep_date'] = pd.to_datetime(ember_sleep_df['sleep_date'])
fixed_date = pd.to_datetime('2023-08-18')

# Calculate months since birth
ember_sleep_df['months_since_birth'] = (ember_sleep_df['sleep_date'].dt.year - fixed_date.year) * 12 + (ember_sleep_df['sleep_date'].dt.month - fixed_date.month)

st.subheader('How much sleep does she have per day?')
# calculate total sleep time per day
total_sleep_data = ember_sleep_df[['days_since_birth', 'hours_duration']].groupby('days_since_birth').sum()
total_sleep_data = total_sleep_data.reset_index()

# total sleep duration vs days since birth
create_bar_chart_with_rolling_average(total_sleep_data['days_since_birth'],total_sleep_data['hours_duration'],
                                      'days_since_birth','hours_duration',
                                      'Days since birth','Total sleep duration (hours)',
                                      'Total sleep duration per day vs days since birth',14)

st.header('How long are her naps? How have her naps changed over time?')

# get average nap duration without night sleeps
nap_data = ember_sleep_df[ember_sleep_df['night_sleep'] == False][['days_since_birth', 'hours_duration']].groupby('days_since_birth').mean()
nap_data = nap_data.reset_index()

# average nap duration per day vs days since birth
create_scatter_plot_with_rolling_average(nap_data['days_since_birth'], nap_data['hours_duration'],
                                      'days_since_birth','hours_duration',
                                      'Days since birth','Average nap duration (hours)',
                                      'Average nap duration per day vs days since birth',14)

# remove night sleeps
nap_month_data = ember_sleep_df[ember_sleep_df['night_sleep'] == False][['months_since_birth', 'hours_duration']]
# Nap duration histogram
create_histogram(nap_month_data,
                'hours_duration',
                'Nap duration (hours)',
                'Nap duration distribution')

# Nap duration by month
create_boxplot(nap_month_data,
               'months_since_birth','hours_duration',
               'Months since birth','Nap duration (hours)',
               'Nap duration in hours by month')


st.header('How long does she stay awake between naps (wake windows)?')

# get wake window data
wake_month_data = ember_sleep_df[ember_sleep_df['night_sleep'] == False][['months_since_birth', 'wake_window_hours']]

# Wake windows by month
create_boxplot(wake_month_data,
               'months_since_birth','wake_window_hours',
               'Months since birth','Wake window (hours)',
               'Wake window in hours by month')

wake_window_day = ember_sleep_df[['days_since_birth', 'wake_window_hours']].groupby('days_since_birth').sum()
wake_window_day = wake_window_day.reset_index()
# wake window per day vs days since birth
create_bar_chart_with_rolling_average(wake_window_day['days_since_birth'], wake_window_day['wake_window_hours'],
                                      'days_since_birth','wake_window_hours',
                                      'Days since birth','Total wake time (hours)',
                                      'Total waking hours per day vs days since birth',14)

