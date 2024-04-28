import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from visualisation_functions import (create_scatter_plot_with_rolling_average, 
                                     create_scatter_plot_with_rolling_average_2,
                                     create_boxplot, 
                                     create_histogram_with_colours, 
                                     create_bar_chart_with_rolling_average,
                                     create_multiple_line_chart,
                                     create_bar_chart,
                                     create_stacked_bar_chart)

st.title('Feeding data visualisations')

# get feed data
ember_feed_df = pd.read_csv('data/ember_nursing_30march_updated.csv')
ember_feed_df['feed_date'] = pd.to_datetime(ember_feed_df['feed_date'])
birth_date = pd.to_datetime('2023-08-18')

# Calculate months since birth
ember_feed_df['months_since_birth'] = (ember_feed_df['feed_date'].dt.year - birth_date.year) * 12 + (ember_feed_df['feed_date'].dt.month - birth_date.month)

st.subheader('Time spent feeding')

# Base chart with total feed time per day
feed_total_per_day_df = ember_feed_df[['days_since_birth', 'total_min']].groupby('days_since_birth').sum()
feed_total_per_day_df = feed_total_per_day_df.reset_index()
create_scatter_plot_with_rolling_average(feed_total_per_day_df['days_since_birth'], feed_total_per_day_df['total_min']/60,
                                      'days_since_birth','total_min',
                                      'Days since birth','Total feed duration (hours)',
                                      'Total time on boob per day over time',14)

# cumulative sum of hours spent breastfeeding
feed_total_per_day_df['cumsum_total_min'] = feed_total_per_day_df['total_min'].cumsum()
feed_total_per_day_df['cumsum_total_hour'] = feed_total_per_day_df['cumsum_total_min']/60
create_bar_chart(feed_total_per_day_df['days_since_birth'],feed_total_per_day_df['cumsum_total_hour'],
                 'days_since_birth','cumsum_total_hour',
                 'Days since birth','Hours spent breastfeeding',
                 'Cumulative Sum of total hours breastfeeding')

st.subheader('How long does each feed take?')
# Can we see how the duration of each feed has evolved since birth?
feed_month_data = ember_feed_df[['months_since_birth', 'total_min']]

# box plot
create_boxplot(feed_month_data,
               'months_since_birth','total_min',
               'Months since birth','Feed duration (minutes)',
               'Feed duration in minutes by month')
# histogram

create_histogram_with_colours(feed_month_data,
                              'total_min','months_since_birth',
                              'Feed duration (mins)',
                              'Feed duration in minutes by month')

st.subheader("How long is the gap between feeds?")
# What is the gap between feeds (excluding night feeds)?
feed_month_data_exc_longest = ember_feed_df[ember_feed_df['is_longest_feed_gap_today']==False][['months_since_birth', 'hours_since_last_feed']]

create_boxplot(feed_month_data_exc_longest,
               'months_since_birth','hours_since_last_feed',
               'Months since birth','Time since last feed (hours)',
               'Gap between milk feeds (hours) by month (excluding night gap)')

feed_day_data_exc_longest = ember_feed_df[ember_feed_df['is_longest_feed_gap_today']==False][['days_since_birth', 'hours_since_last_feed']]
create_scatter_plot_with_rolling_average(feed_day_data_exc_longest['days_since_birth'],feed_day_data_exc_longest['hours_since_last_feed'],
                                          'days_since_birth','hours_since_last_feed',
                                          'Days since birth','Gap between feeds (hours)',
                                          'Gap between milk feeds (hours) over time (excluding night gap)',21)

# What is the gap between feed over time for night feeds?
feed_month_data_inc_longest = ember_feed_df[ember_feed_df['is_longest_feed_gap_today']][['days_since_birth', 'hours_since_last_feed']]
create_scatter_plot_with_rolling_average(feed_month_data_inc_longest['days_since_birth'],feed_month_data_inc_longest['hours_since_last_feed'],
                                          'days_since_birth','hours_since_last_feed',
                                          'Days since birth','Gap between feeds (hours)',
                                          'Gap between milk feeds (hours) overnight',21)

st.subheader('Left vs right boob')
# What is total amount of left vs right on boob? 
feed_left_per_day_df = ember_feed_df[['days_since_birth', 'left_duration_min']].groupby('days_since_birth').sum()
feed_left_per_day_df['side'] = 'left'
feed_left_per_day_df['duration_min'] = feed_left_per_day_df['left_duration_min']
feed_left_per_day_df = feed_left_per_day_df.reset_index()
feed_right_per_day_df = ember_feed_df[['days_since_birth', 'right_duration_min']].groupby('days_since_birth').sum()
feed_right_per_day_df['side'] = 'right'
feed_right_per_day_df['duration_min'] = feed_right_per_day_df['right_duration_min']
feed_right_per_day_df = feed_right_per_day_df.reset_index()
feed_side_per_day_df = pd.concat([feed_left_per_day_df[['days_since_birth','side','duration_min']], feed_right_per_day_df[['days_since_birth','side','duration_min']]])

# create a line chart with right boob and left boob duration per day
create_multiple_line_chart(feed_side_per_day_df,
                           'days_since_birth','duration_min','side',
                           'Days since birth','Feed Duration (minutes)',
                           'Total duration on right vs left boob')

# calculate the percentage on that side in a day
feed_total_per_day_df = ember_feed_df[['days_since_birth', 'total_min']].groupby('days_since_birth').sum()
feed_total_per_day_df = feed_total_per_day_df.reset_index()
feed_perc_per_day_df = pd.merge(feed_side_per_day_df, feed_total_per_day_df, on='days_since_birth', how='inner')
feed_perc_per_day_df['percentage_on_side'] = feed_perc_per_day_df['duration_min']/feed_perc_per_day_df['total_min']*100

# create a 100% stacked bar chart with the percentage that I fed in each side for.
create_stacked_bar_chart(feed_perc_per_day_df,
                         'days_since_birth','percentage_on_side','side',
                         'Days Since Birth', 'Percentage on that boob side',
                         'Percentage on each side of boob per day')