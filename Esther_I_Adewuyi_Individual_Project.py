#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 20:48:18 2021

@author: esthercrystal
"""

import requests

import json

import pandas as pd

import matplotlib.pyplot as plt

import dash

import dash_core_components as dcc

import dash_html_components as html

from dash.dependencies import Input, Output

import plotly.express as px

import pandas as pd

# API address

api = 'https://data.boston.gov/api/3/action/datastore_search?offset={offset}&resource_id=4582bec6-2b4f-4f9e-bc55-cbaa73117f4c&limit=32000'

 

# Clean the raw dataframe. Returns clean df with given status, between given dates.

'''

    df = data frame to clean

    status= 'Fail' or 'Pass'

    start_date = '2000-01-01'

    end_date = '2021-04-09'

'''

def keepRelevantData(df, status,start_date, end_date):

   

    # Get only those rows where violstatus = provided status. 

    df_status= df[df['violstatus'] == status]

 

    # Conver the resultdttm column into datetime type.

    df_status['resultdttm'] = pd.to_datetime(df_status['resultdttm'])

 

    # Create a date filter.

    dateFilter = (df_status['resultdttm'] > start_date) & (df_status['resultdttm'] <= end_date)
    df_status_date = df_status[dateFilter]
    return df_status_date

 

# Method to call API end point and get the final df as output.

'''

# no_of_records = total rows to fetch.

status= 'Fail' or 'Pass'

start_date = '2000-01-01'

end_date = '2021-04-09'

'''

def apiCall(start_row, end_row, status, start_date,end_date):

   

    # Initialize the dataframe to store the final results.

    Final_df = pd.DataFrame()  

    

    # Counter for while loop.

    i=start_row

 

    # Run until all rows are downloaded.

    while i <end_row:

 

        print('Fetching 32000 records at a time. At row number {rows}.'.format(rows=i))

 

        # Format the api call with updated offset parameter.

        apiString =api.format(offset = i)

 

        # Request a response from the API and make df

        request_response = requests.get(apiString)

        response_json = json.loads(request_response.text)

        request_response.close()

        df = pd.DataFrame(response_json['result']['records'])

 

        # Send this df to cleaning method where only limited data is selected and returned back.

        cleaned_df = keepRelevantData(df, status, start_date, end_date)

 

        # Append the cleaned _df to Final_df to be returned.

        Final_df = Final_df.append(cleaned_df, ignore_index=True)

 

        # Finally in the end , increment i by 32000 as the api call can only download 32000 rows at a time.

        i= i+32000

    return Final_df;

start_row = 1

end_row= 96000

start_date = '2020-07-01'

end_date = '2020-12-09'

status= 'Fail'

 

boston_inspection = apiCall(start_row, end_row, status, start_date, end_date)

boston_food=pd.DataFrame(boston_inspection)

boston_food_cleaned=boston_inspection.replace({'city':{'BOSTON':'Boston','DORCHESTER':'Dorchester', 'JAMAICA PLAIN':'Jamaica Plain', 'WEST ROXBURY':'West Roxbury','SOUTH BOSTON':'South Boston','ROSLINDALE':'Roslindale','BRIGHTON':'Brighton','EAST BOSTON':'East Boston', 'MATTAPAN':'Mattapan' }})

 

boston_food_new=boston_food_cleaned.rename(columns={'businessname':'Name', 'city':'City', 'licstatus':'License Status','violstatus':'Violation Status','comments':'Inspection Comments','zip':'Zip Code','result':'Result','descript':'Description', 'viollevel':'Violation Level'})

df = boston_food_new[['Name', 'City','License Status','Violation Status','Inspection Comments','Zip Code','Result','Description','Violation Level']]

print(df.City)

 

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

 

# pandas dataframe to html table

def generate_table(dataframe, max_rows=50):

    return html.Table([

        html.Thead(

            html.Tr([html.Th(col) for col in dataframe.columns])

        ),

        html.Tbody([

            html.Tr([

                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns

            ]) for i in range(min(len(dataframe), max_rows))

        ])

    ])

 

app = dash.Dash(__name__, external_stylesheets=stylesheet)

server = app.server

app.layout = html.Div([

    html.H1('Food Inspections', style={'textAlign': 'center', 'color': 'blue'}),
    html.Div(children='''
        Individual MA705 Project | Esther I Adewuyi''', style={'textAlign': 'center'}),

    html.H4('The Dashboard compiles data from the Health Division of the Department of Inspectional Services which  ensures that all food establishments in City of Boston meet relevant sanitary codes and standards. Inspections are done once a year along with a followup.', style={'textAlign':'center'}),
    html.H6('This Dashboard provides customer easy reference to search for the restaurants whether they fail to meet the inspection criteria and the reasons.', style={'textAlign':'center'}),
    html.Div(

        [

            html.H4('Select City'),

                dcc.Dropdown(options=[{'label': 'Allston', 'value': 'Allston'},

                            {'label': 'Boston', 'value': 'Boston'},

                            {'label': 'Brighton', 'value': 'Brighton'},

                            {'label': 'Charlestown', 'value': 'Charlestown'},

                            {'label': 'Dorchester', 'value': 'Dorchester'},

                            {'label': 'East Boston', 'value': 'East Boston'},

                            {'label': 'Fenway', 'value': 'Fenway'},

                            {'label': 'Hyde Park', 'value': 'Hyde Park'},

                            {'label': 'Jamaica Plain', 'value': 'Jamaica Plain'},

                            {'label': 'Mattapan', 'value': 'Mattapan'},

                            {'label': 'Mission Hill', 'value': 'Mission Hill'},

                            {'label': 'Roslindale', 'value': 'Roslindale'},

                            {'label': 'Roxbury', 'value': 'Roxbury'},

                            {'label': 'South Boston', 'value': 'South Boston'},

                            {'label': 'South End', 'value': 'South End'},

                            {'label': 'West Roxbury', 'value': 'West Roxbury'},

                            {'label': 'Columbia RD', 'value': 'Columbia RD'}],

                    id= "city_dropdown",

                    value = ['Boston']),
            html.H4('Sort table by:'),

                dcc.Dropdown(options= [{'label': 'City', 'value': 'City'},

                            {'label': 'Zip Code', 'value': 'Zip Code'}],

                   id='sort_by_dropdown',

                    value='City')],

              style={'width': '49%', 'display': 'inline-block'} 
               ),   
               html.H4 ("License Status"),

                dcc.Checklist(options=[{'label':'Active', 'value':'Active'},

                            {'label':'Inactive', 'value':'Inactive'}],

                    id="license_status",

                    value='Active'),    
         html.Div([

             dcc.Graph(id="graph", style={'display':'block',"margin-right":"auto","margin-left":"auto", "height":500, "width":900}),

    html.Div(html.Div(id="df_div"),

        style={'width': '49%', 'display':'inline-block','minWidth': '180px', 'width': '180px', 'maxWidth':'180px'}),             

    ])

])  
             



@app.callback(

    Output(component_id='graph', component_property='figure'),

    [Input(component_id='city_dropdown', component_property='value')]

)

 

def update_graph_output(city_dropdown):  

    if len(city_dropdown)<1:

        df_graph= df

    else:

       df_graph=df[df.City.isin(city_dropdown)] 

                

    fig = px.bar(df_graph, x='City', y='Result', color = 'Description')       

    fig.update_layout(xaxis_title="City",

                      yaxis_title="Result",

                      legend_title="Description")

                   

    return fig

    print(df_graph)

 

if __name__ == '__main__':

    app.run_server(debug=False)

           