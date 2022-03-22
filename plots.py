from datetime import timedelta
import plotly.graph_objects as go
import pandas as pd

#colors
blue_100_color = 'rgba(0,101,159,1)'
blue_75_color = 'rgba(0,101,159,0.75)'
blue_50_color = 'rgba(0,101,159,0.5)'
blue_25_color = 'rgba(0,101,159,0.25)'
red_100_color = 'rgba(181,44,56,1)'
yellow_100_color = 'rgba(255,149,43,1)'

axis_color = 'rgba(204,204,204,1)'
axis_grid_color = 'rgba(204,204,204,0.5)'
text_color = 'rgba(119,119,119,1)'
background_color = 'rgba(255,255,255,1)'

def CreateBoxChart(df, output_name, data_name, category, area, start_date, end_date):
    """Creates a categorized box chart with data filtered to specifications.

    Args:
        df (dataframe): a pandas dataframe that contains the data to use
        output_name (str): the name of the file to be output along with it's path inside the images folder
        data_name (str): the header for the dataframe column to pull data points from
        category (str): the header for the dataframe column to categorize data points on
    """

    # Sets the order of the x axis
    if category == "Day":
        cat_order = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    elif category == "Hour":
        cat_order = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    elif category == "Window":
        cat_order = ["0-6","6-18","18-24"]

    # Generate Title
    title_data = {'TEMP F': 'Temperature (F)', 'RH %': 'Relative Humidity (%)'}
    title_cat = {'Day': 'Weekday', 'Hour': 'Hour', 'Window': 'Time Window'}
    title = f"Distribution of {title_data[data_name]} by {title_cat[category]} ({start_date} - {end_date}) -- {area}"

    # Create Chart
    fig = go.Figure()
    fig.add_trace(
        go.Box(
            x = df[category],
            y = df[data_name],
            boxmean = True,
            boxpoints = 'outliers',
            fillcolor = blue_25_color,
            line = dict(
                color = blue_100_color,
                width = 2,
            ),
            marker = dict(
                color = blue_50_color,
                line = dict(
                    color = blue_100_color,
                    width = 0.2,
                ),
                size = 2,
            ),
            notched = False,
        )
    )
    fig.update_xaxes(
        categoryorder = 'array', 
        categoryarray = cat_order,
        linecolor = axis_color,
        linewidth = 2,
        tickfont = dict(
            family = 'Open Sans, Arial, Helvetica, sans-serif',
            size = 14,
            color = text_color,
        ),
        tickmode = 'linear',
    )
    fig.update_yaxes(
        gridcolor = axis_grid_color,
        gridwidth = 1,
        linecolor = axis_color,
        linewidth = 2,
        tickfont = dict(
            family = 'Open Sans, Arial, Helvetica, sans-serif',
            size = 14,
            color = text_color,
        ),
        title = dict(
            font = dict(
                family = 'Open Sans, Arial, Helvetica, sans-serif',
                size = 21,
                color = text_color,
            ),
            standoff = 4,
            text = title_data[data_name],
        ),
    )
    fig.update_layout(
        autosize = False,
        height = 1080,
        paper_bgcolor = background_color,
        plot_bgcolor = background_color,
        title = dict(
            font = dict(
                family = 'Open Sans, Arial, Helvetica, sans-serif',
                size = 28,
                color = text_color,
            ),
            text = title,
            x = 0.5,
            xanchor = 'center',
        ),
        width = 1920,
    )

    # Save the image
    fig.write_image(output_name + ".png")


def createControlChart(df, output_name, data_name, categories, area, start_date, end_date):
    """Creates a chart showing the change in measured data overtime as well as the control limits for the data set.

    Args:
        df (dataframe): a pandas dataframe containing rh/temp data
        output_name (string): the name of the file to be output
        data_name (string): the category of data to be charted
        categories (list): the categories by which the dataframe is filtered
    """

    # Generate Title
    title_data = {'TEMP F': 'Temperature (F)', 'RH %': 'Relative Humidity (%)'}
    title_cat = {'Day': 'weekday', 'DATE': 'date', 'Hour': 'hour', 'Window': 'time window'}
    title = f"Control Chart of {title_data[data_name]} by {', '.join([title_cat[cat] for cat in categories])} ({start_date} - {end_date}) -- {area}"

    # Create Chart
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            line =  dict(
                color = red_100_color,
                dash = 'dash',
                width = 2,
            ),
            mode = 'lines',
            name = 'X-UCL',
            x = df['idx'],
            y = df['UCL'],
        )
    )
    fig.add_trace(
        go.Scatter(
            line =  dict(
                color = red_100_color,
                dash = 'dash',
                width = 2,
            ),
            mode = 'lines',
            name = 'X-LCL',
            x = df['idx'],
            y = df['LCL']
        )
    )
    fig.add_trace(
        go.Scatter(
            line =  dict(
                color = yellow_100_color,
                dash = 'dot',
                width = 2,
            ),
            mode = 'lines',
            name = 'X-Bar',
            x = df['idx'],
            y = df['x-bar']
        )
    )
    fig.add_trace(
        go.Scatter(
            line =  dict(
                color = blue_75_color,
                width = 3,
            ),
            marker = dict(
                color = blue_100_color,
                size = 6,
            ),
            mode = 'lines+markers',
            name = 'Data',
            x = df['idx'],
            y = df['avg'],
        )
    )
    fig.update_xaxes(
        linecolor = axis_color,
        linewidth = 2,
        tickfont = dict(
            family = 'Open Sans, Arial, Helvetica, sans-serif',
            size = 14,
            color = text_color,
        ),
    )
    fig.update_yaxes(
        gridcolor = axis_grid_color,
        gridwidth = 1,
        linecolor = axis_color,
        linewidth = 2,
        tickfont = dict(
            family = 'Open Sans, Arial, Helvetica, sans-serif',
            size = 14,
            color = text_color,
        ),
        title = dict(
            font = dict(
                family = 'Open Sans, Arial, Helvetica, sans-serif',
                size = 21,
                color = text_color,
            ),
            standoff = 4,
            text = title_data[data_name]
        ),
    )
    fig.update_layout(
        autosize = False,
        height = 540,
        paper_bgcolor = background_color,
        plot_bgcolor = background_color,
        title = dict(
            font = dict(
                family = 'Open Sans, Arial, Helvetica, sans-serif',
                size = 28,
                color = text_color,
            ),
            text = title,
            x = 0.5,
            xanchor = 'center',
        ),
        width = 1920,
    )

    # Save the image
    fig.write_image(output_name + "-ControlChart.png")


def createRangeChart(df, output_name, data_name, categories, area, start_date, end_date):
    """Creates a chart showing the magnitude of the changes in measured data for consecutive points over time.

    Args:
        df (dataframe): a pandas dataframe containing rh/temp data
        output_name (string): the name of the file to be output
        data_name (string): the category of data to be charted
        categories (list): the categories by which the dataframe is filtered
    """

    # Generate Title
    title_data = {'TEMP F': 'Temperature (F)', 'RH %': 'Relative Humidity (%)'}
    title_cat = {'Day': 'weekday', 'DATE': 'date', 'Hour': 'hour', 'Window': 'time window'}
    title = f"Range Chart of {title_data[data_name]} by {', '.join([title_cat[cat] for cat in categories])} ({start_date} - {end_date}) -- {area}"

    # Create Chart
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            line =  dict(
                color = red_100_color,
                dash = 'dash',
                width = 2,
            ),
            mode = 'lines',
            name = 'R-UCL',
            x = df['idx'],
            y = df['R UCL'],
        )
    )
    fig.add_trace(
        go.Scatter(
            line =  dict(
                color = yellow_100_color,
                dash = 'dot',
                width = 2,
            ),
            mode = 'lines',
            name = 'R-Bar',
            x = df['idx'],
            y = df['r-bar']
        )
    )
    fig.add_trace(
        go.Scatter(
            line =  dict(
                color = blue_75_color,
                width = 3,
            ),
            marker = dict(
                color = blue_100_color,
                size = 6,
            ),
            mode = 'lines+markers',
            name = 'Data',
            x = df['idx'],
            y = df['diff'],
        )
    )
    fig.update_xaxes(
        linecolor = axis_color,
        linewidth = 2,
        tickfont = dict(
            family = 'Open Sans, Arial, Helvetica, sans-serif',
            size = 14,
            color = text_color,
        ),
    )
    fig.update_yaxes(
        gridcolor = axis_grid_color,
        gridwidth = 1,
        linecolor = axis_color,
        linewidth = 2,
        tickfont = dict(
            family = 'Open Sans, Arial, Helvetica, sans-serif',
            size = 14,
            color = text_color,
        ),
        title = dict(
            font = dict(
                family = 'Open Sans, Arial, Helvetica, sans-serif',
                size = 21,
                color = text_color,
            ),
            standoff = 4,
            text = title_data[data_name]
        ),
    )
    fig.update_layout(
        autosize = False,
        height = 540,
        paper_bgcolor = background_color,
        plot_bgcolor = background_color,
        title = dict(
            font = dict(
                family = 'Open Sans, Arial, Helvetica, sans-serif',
                size = 28,
                color = text_color,
            ),
            text = title,
            x = 0.5,
            xanchor = 'center',
        ),
        width = 1920,
    )

    #Save the image
    fig.write_image(output_name + "-RangeChart.png")


def CreateControlRangeCharts(df, output_name, data_name, categories, area, start_date, end_date):#, days=0):
    """Modifies the data frame in order to create control and range charts for given data

    Args:
        df (dataframe): a pandas dataframe containing rh/temp data
        output_name (string): the name of the file to be output
        data_name (string): the category of data to be charted
        categories (list): the categories by which the dataframe is filtered
    """

    # Filter df to include only most recent 'days' days
    #if days > 0:
        #in_days = df['DATE'] >= df['DATE'].max()-timedelta(days)
        #df = df[in_days]

    df = pd.DataFrame({'avg' : df.groupby(categories)[data_name].mean()}).reset_index()
    df['diff'] = abs(df['avg'].diff(1))

    # Variables used for control chart columns
    x_bar = df['avg'].mean()
    r_bar = df['diff'].mean()
    ucl = x_bar + 2.66*r_bar
    lcl = max(0, x_bar - 2.66*r_bar)
    r_ucl = 3.268*r_bar

    # Create cols needed for control charts
    df['idx'] = pd.Series([i for i in range(len(df.index))])
    df['x-bar'] = pd.Series([x_bar for _ in range(len(df.index))])
    df['r-bar'] = pd.Series([r_bar for _ in range(len(df.index))])
    df['UCL'] = pd.Series([ucl for _ in range(len(df.index))])
    df['LCL'] = pd.Series([lcl for _ in range(len(df.index))])
    df['R UCL'] = pd.Series([r_ucl for _ in range(len(df.index))])

    # Create Control and Range Chart with modified data frame
    createControlChart(df, output_name, data_name, categories, area, start_date, end_date)#, days)
    createRangeChart(df, output_name, data_name, categories, area, start_date, end_date)#, days)

if __name__ == "__main__":
    pass