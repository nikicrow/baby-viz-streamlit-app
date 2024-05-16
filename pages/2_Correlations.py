import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from visualisation_functions import (create_scatter_plot,
                                     create_boxplot,
                                     create_histogram
                                     )

st.title('Correlations')

# get feed data
ember_feed_df = pd.read_csv('data/ember_nursing_30march_updated.csv')
ember_feed_df['feed_date'] = pd.to_datetime(ember_feed_df['feed_date'])
feed_total_min = ember_feed_df[['days_since_birth', 'total_min']].groupby('days_since_birth').sum()
feed_total_min = feed_total_min.rename(columns={'total_min': 'total_mins'})
feed_mean_min = ember_feed_df[['days_since_birth', 'total_min']].groupby('days_since_birth').mean()
feed_mean_min = feed_mean_min.rename(columns={'total_min': 'average_mins'})
feed_count = ember_feed_df[['days_since_birth', 'total_min']].groupby('days_since_birth').count()
feed_count = feed_count.rename(columns={'total_min': 'num_feeds'})
feed_agg_df = pd.merge(feed_total_min, feed_mean_min, on='days_since_birth', how='inner').merge(feed_count, on='days_since_birth', how='inner')
feed_agg_df = feed_agg_df.reset_index()

# load sleep data
ember_sleep_df = pd.read_csv('data/ember_sleep_30march_updated.csv')
ember_sleep_df['duration'] = ember_sleep_df['hours_duration'].astype(float)
sleep_total_duration = ember_sleep_df[['days_since_birth', 'duration']].groupby('days_since_birth').sum()/60
sleep_total_duration = sleep_total_duration.rename(columns={'duration': 'duration_hours'})
nap_duration = ember_sleep_df[ember_sleep_df['night_sleep'] == False][['days_since_birth', 'duration']].groupby('days_since_birth').mean()
nap_duration = nap_duration.rename(columns={'duration': 'nap_duration_mins'})
nap_count = ember_sleep_df[ember_sleep_df['night_sleep'] == False][['days_since_birth', 'duration']].groupby('days_since_birth').count()
nap_count = nap_count.rename(columns={'duration': 'nap_count'})
sleep_agg_df = pd.merge(sleep_total_duration, nap_duration, on='days_since_birth', how='inner').merge(nap_count, on='days_since_birth', how='inner')
sleep_agg_df = sleep_agg_df.reset_index()

# Join the two tables on the column 'days_since_birth'
ember_day_df = pd.merge(sleep_agg_df, feed_agg_df, on='days_since_birth', how='inner')

create_scatter_plot(ember_day_df['duration_hours'],ember_day_df['total_mins'],
                        'duration_hours','total_mins',
                        'Hours of sleep','Total time feeding',
                        'Time spent feeding vs time spent sleeping')

create_scatter_plot(ember_day_df['nap_duration_mins'],ember_day_df['average_mins'],
                        'nap_duration_mins','average_mins',
                        'Nap duration in minutes','Average time feeding',
                        'Average nap duration vs average time spent feeding')