'''
Imports for dash, pandas and plotly
'''

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output,Input
import plotly.graph_objects as go
import pandas as pd

#Import Data from file
df = pd.read_csv('./Data/test.csv')
print(df)
#Filtering data on date column to get data for a perticular day
date_list = df['Date'].unique()
print(date_list)

date_options = []
for date in date_list:
    date_options.append({'label':date, 'value': date})


print(date_options)

# date_filter = df[df['Date']=='3/3/2020']
# print(date_filter)

app = dash.Dash()

app.layout = html.Div([
    dcc.Dropdown(id='date-picker',value=min(date_list),options=date_options),
    dcc.Graph(id='memory'),
    dcc.Graph(id='cpu'),
    dcc.Graph(id='response')
])


@app.callback([Output('memory','figure'),Output('cpu','figure'),Output('response','figure')],
              [Input('date-picker','value')])
def update_chart(selected_date):
    print(selected_date)
    date_filter = df[df['Date'] == selected_date]
    memory_columns = ['total memory','used memory']

    memory_data = [go.Scatter(
        x = pd.to_datetime(date_filter['time'],format= '%H:%M:%S').dt.time,
        y= date_filter[memory_column],
        mode='lines',
        name= memory_column)
        for memory_column in memory_columns]

    memory_fig = {
        'data': memory_data,
        'layout': go.Layout(
            xaxis={'type': '-', 'title': 'Time'},
            yaxis={'title': 'Memory Utilization'},
            hovermode='closest'
        )
    }

    cpu_columns = ['cpu1','cpu2','cpu3','cpu4']

    cpu_data = [go.Scatter(
        x = pd.to_datetime(date_filter['time'],format= '%H:%M:%S').dt.time,
        y= date_filter[cpu],
        mode='lines',
        name= cpu)
        for cpu in cpu_columns]

    cpu_fig = {
        'data': cpu_data,
        'layout': go.Layout(
            xaxis={'type': '-', 'title': 'Time'},
            yaxis={'title': 'CPU Utilization'},
            hovermode='closest'
        )
    }

    response_data = [go.Scatter(
        x = pd.to_datetime(date_filter['time'],format= '%H:%M:%S').dt.time,
        y= date_filter['Response time'],
        mode='lines',
        name= 'Response')]

    response_fig = {
        'data': response_data,
        'layout': go.Layout(
            xaxis={'type': '-', 'title': 'Time'},
            yaxis={'title': 'Response Time in Seconds'},
            hovermode='closest'
        )
    }


    return memory_fig,cpu_fig,response_fig


if __name__ == '__main__':
    app.run_server()