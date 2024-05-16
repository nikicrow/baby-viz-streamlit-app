import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
import seaborn as sns
import matplotlib as mpl
import math

def create_bar_chart_with_rolling_average(x,y,
                                          x_colname,y_colname,
                                          x_title,y_title,
                                          title,period=7):
    df = pd.DataFrame(x).join(pd.DataFrame(y))
    df['rolling_average'] = y.rolling(window=period).mean()

    fig = px.bar(df, x=x_colname, y=y_colname, labels={x_colname: x_title, y_colname: y_title}, title=title)
    fig.add_scatter(x=df[x_colname], y=df['rolling_average'], mode='lines', name=f'{period} Day Rolling Average')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=1.1,
        xanchor="right",
        x=1
    ))
    st.plotly_chart(fig)

def create_bar_chart(x,y,
                    x_colname,y_colname,
                    x_title,y_title,
                    title):
    df = pd.DataFrame(x).join(pd.DataFrame(y))
    fig = px.bar(df, x=x_colname, y=y_colname, labels={x_colname: x_title, y_colname: y_title}, title=title)
    st.plotly_chart(fig)

def create_scatter_plot(x,y,
                        x_colname,y_colname,
                        x_title,y_title,
                        title):
    df = pd.DataFrame(x).join(pd.DataFrame(y))
    fig = px.scatter(df,x=x_colname, y=y_colname, labels={x_colname: x_title, y_colname: y_title}, title=title)
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=1.1,
        xanchor="right",
        x=1
    ))
    st.plotly_chart(fig)

def create_scatter_plot_with_rolling_average(x,y,
                                          x_colname,y_colname,
                                          x_title,y_title,
                                          title,period=7):
    df = pd.DataFrame(x).join(pd.DataFrame(y))
    df['rolling_average'] = y.rolling(window=period).mean()
    fig = px.scatter(df,x=x_colname, y=y_colname, labels={x_colname: x_title, y_colname: y_title}, title=title)
    fig.add_scatter(x=df[x_colname], y=df['rolling_average'], mode='lines', name=f'{period} Day Rolling Average')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=1.1,
        xanchor="right",
        x=1
    ))
    st.plotly_chart(fig)

def create_scatter_plot_with_rolling_average_2(x,y,
                                          x_colname,y_colname,
                                          x_title,y_title,
                                          title,period=21):
    df = pd.DataFrame(x).join(pd.DataFrame(y))
    df['rolling_average'] = y.rolling(window=period).mean()
    fig = px.line(df,x=x_colname, y='rolling_average', labels={x_colname: x_title, y_colname: y_title,'rolling_average':f'{period} Day Rolling Average'}, title=title)
    fig.add_scatter(x=df[x_colname], y=df[y_colname])
    # Update the layout to change the legend location to be above the chart
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=1.1,
        xanchor="right",
        x=1
    ))
    st.plotly_chart(fig)

def create_histogram_with_colours(data,x_label,colour_label,x_title,title):
    fig = px.histogram(data, 
                       x=x_label, 
                       color=colour_label, 
                       title=title,
                       labels={x_label: x_title}, 
                       nbins=30, barmode='overlay')
    st.plotly_chart(fig)

def create_histogram(data,x_label,x_title,title):
    fig = px.histogram(data, 
                       x=x_label, 
                       title=title,
                       labels={x_label: x_title}, 
                       nbins=30, barmode='overlay')
    st.plotly_chart(fig)


def create_boxplot(data,x_label,y_label,x_title,y_title,title):
    # Create the boxplot chart
    fig = px.box(data, 
                 x=x_label, y=y_label, 
                 title=title,
                labels={x_label: x_title, y_label: y_title})

    # Display the chart using Streamlit
    st.plotly_chart(fig)

def create_multiple_line_chart(df,x_column,y_column,color_column,x_title,y_title,title):
    fig = px.line(df, x=x_column, y=y_column, color=color_column, labels={x_column: x_title, y_column: y_title}, title=title)
    # put legend at top
    fig.update_layout(
        legend_title="Lines",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(fig)

def create_stacked_bar_chart(df,x_column,y_column,color_column,x_title,y_title,title):
    # Create a 100% stacked bar chart
    fig = px.bar(df, x=x_column, y=y_column, color=color_column, barmode='stack', labels={x_column: x_title, y_column: y_title}, title=title)
    fig.update_layout(barmode="stack")
    # Display the chart using Streamlit
    st.plotly_chart(fig)



def enumerate_labels(date_num: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    hour_labels = [f"{num}:00" for num in range(24)]
    week_labels = [str(num) for num in range(0, math.ceil(date_num / 7), 2)]

    return hour_labels, week_labels

def format_24h_week_plot_vertical(fig_axis: mpl.figure, date_num: int) -> None:
    AXIS_FONT_SIZE_LG = 12
    # Create the tick labels
    hour_labels, week_labels = enumerate_labels(date_num)

    # Set title and axis labels
    fig_axis.set_xlabel(
        "Age (weeks)",
        fontsize=AXIS_FONT_SIZE_LG,
        rotation=0,
    )
    fig_axis.set_ylabel("Time of Day", fontsize=AXIS_FONT_SIZE_LG)

    # Format y axis - clock time
    fig_axis.set_ylim(24, 0)
    fig_axis.yaxis.set_ticks(np.arange(0, 24, 1))
    fig_axis.set_yticklabels(hour_labels, rotation=0)
    fig_axis.invert_yaxis()
    fig_axis.set_title("Sleeping time of day over time",fontsize=18)

    # Format x axis - bottom, week number
    fig_axis.set_xlim(1, date_num)
    fig_axis.xaxis.set_ticks(np.arange(1, date_num + 1, 14))
    fig_axis.set_xticklabels(week_labels, rotation=90)

def create_24_hour_sleep_plot(data):
    # Plot setup
    sns.set(style="darkgrid")
    figure = plt.figure(figsize=(10, 7))
    fig_ax = figure.add_subplot(111)
    BAR_SIZE = 1

    
    # Find sessions with offsets and plot the offset with day_number+1
    data.loc[data.index].apply(
        lambda row: fig_ax.broken_barh(
            [(row["day_number"] + 1, BAR_SIZE)],
            [0, row["offset"]],
        ),
        axis=1,
    )
    # Loop through each row and plot the duration
    data.apply(
        lambda row: fig_ax.broken_barh(
            [(row["day_number"], BAR_SIZE)],
            [row["timestamp_hour"], row["duration"]],
        ),
        axis=1,
    )
    
    # End date - one year or full
    end_date = data.iloc[-1]['day_number']
    # Format plot - vertical or horizontal
    format_24h_week_plot_vertical(fig_ax, end_date)

