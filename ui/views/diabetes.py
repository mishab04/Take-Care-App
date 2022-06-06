# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 11:35:43 2022

@author: User
"""
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output,State
import numpy as np
import pandas as pd
import shap
from utils import *
import plotly.graph_objects as go

from app import app

layout_page = html.Div([html.H3('Diabetes Indicator',className="display-4 text-center"),
               html.Div([
                       html.Div([
                               html.Header('Pregnancies'),
                               daq.Slider(
                                       id='d_pregnancies',
                                       min = 0,
                                       max = 17,
                                       step = 1,
                                       value = 3,
                                       marks = {i:str(i) for i in range(0,18)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                       ),
                                html.Br(),
                                html.Header('Glucose'),
                                daq.Slider(
                                        id ='d_glucose',
                                           min = 0,
                                           max = 200,
                                           step = 5,
                                           value = 55,
                                           marks = {i:str(i) for i in range(0,210,20)},
                                           handleLabel={"showCurrentValue": True,"label": "Val"},
                                        color = "#F64C72"
                                        ),
                                html.Br(),
                                html.Header('Blood Pressure'),
                                daq.Slider(
                                        id = 'd_bloodpressure',
                                           min = 0,
                                           max = 130,
                                           step = 5,
                                           value = 80,
                                           marks = {i:str(i) for i in range(0,140,10)},
                                           handleLabel={"showCurrentValue": True,"label": "Val"},
                                        color = "#F64C72"
                                        ),
                                html.Br(),
                                html.Header('Skin Thickness'),
                                daq.Slider(
                                        id ='d_skinthickness',
                                       min = 0,
                                       max = 100,
                                       step = 1,
                                       value = 30,
                                       marks = {i:str(i) for i in range(0,110,10)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),                                               
                                     ],className='col-sm-12 col-md-3 order-1 order-md-1'),
                        html.Div([dcc.Graph(id = 'diabeteswaterfall',style = {'display':'None'}),
                                  html.Div(id = 'diabetesprediction')], className = 'col-sm-12 col-md-6 order-3 order-md-2 font-weight-bold'),
                        html.Div([
                                html.Header('Insulin'),
                               daq.Slider(
                                        id ='d_insulin',
                                       min = 0,
                                       max = 700,
                                       step = 10,
                                       value = 50,
                                       marks = {i:str(i) for i in range(0,710,100)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),                                                
                                html.Br(),
                                html.Header('Body Mass Index'),
                                daq.Slider(
                                        id ='d_bmi',
                                       min = 0,
                                       max = 70,
                                       step = 1,
                                       value = 25,
                                       marks = {i:str(i) for i in range(0,71,5)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),                                                
                                html.Br(),                                        
                                html.Header('Diabetes Pedigree Function'),
                                daq.Slider(
                                        id ='d_diabetespedigreefunction',
                                       min = 0,
                                       max = 2.5,
                                       step = .1,
                                       value = 1.2,
                                       marks = {0:str(0),
                                                0.5:str(0.5),
                                                1:str(1),
                                                1.5:str(1.5),
                                                2:str(2.0),
                                                2.5:str(2.5)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),                                                 
                                html.Br(),                                        
                                html.Header('Age'),
                                daq.Slider(
                                        id ='d_age',
                                       min = 0,
                                       max = 100,
                                       step = 1,
                                       value = 25,
                                       marks = {i:str(i) for i in range(0,101,10)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),                                          
                                html.Br(),                                        
                                dbc.Button(id='submit-diabetes',children='Submit',n_clicks=0,style = {'background':"#F64C72",'color':'white'})                                                                                 
                                ],className = 'col-sm-12 col-md-3 order-2 order-md-3')],className = 'row')
    
    ],className = 'container-lg')
                                
@app.callback([Output('diabetesprediction', 'children'),
              Output('diabeteswaterfall', 'figure'),
              Output('diabeteswaterfall', 'style')],              
              [Input('submit-diabetes','n_clicks')],
              [State('d_pregnancies', 'value'),
               State('d_glucose', 'value'),
               State('d_bloodpressure', 'value'),
               State('d_skinthickness', 'value'),
               State('d_insulin', 'value'),
               State('d_bmi', 'value'),
               State('d_diabetespedigreefunction', 'value'),
               State('d_age', 'value')])
def predict_diabetes(n_clicks,value1,value2,value3,value4,value5,value6,value7,value8):
    if n_clicks is None:
        raise PreventUpdate        
    col_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin','BMI', 'DiabetesPedigreeFunction', 'Age']
    model = call_model('../models/diabetes/diabetes_model.pkl')
    X_single_point = pd.DataFrame(data = np.array([[value1,value2,value3,value4,int(value5),int(value6),value7,value8]]),
                              columns = col_names            
                              )
    predicted_prob = model.predict_proba(X_single_point)[0]
    predicted_prob = list(predicted_prob)[1]
    explainer = call_model('../models/diabetes/diabetes_explainer.pkl')
    sv = explainer(X_single_point)
    exp = shap.Explanation(sv.values[:,:,1], 
                  sv.base_values[:,1], 
                  data=X_single_point.values, 
                  feature_names= col_names)
    
    dt = pd.DataFrame({'feature': col_names,'feature_value': exp[0].values})
    text = 'Probability of Having Diabetes is : {}'.format(round(predicted_prob,4))
    colors = []
    for val in dt['feature_value'].tolist():
        if (val <= 0):
            colors.append('#323aa8')
        else:
            colors.append('#a83432')
    fig = go.Figure(go.Bar(
            orientation = "h",
            y = dt['feature'],
            x = dt['feature_value'],
            marker_color = colors,
            ))
    fig.update_layout(title = "Effect of each variable on Prediction",
                      font = dict(color = 'white',size = 10),
                      paper_bgcolor='rgb(30, 30, 30)',
                      plot_bgcolor= 'rgb(30, 30, 30)',
                      title_x=0.3
                      )
    style = {'display':'inline'}
    return  text,fig,style                                