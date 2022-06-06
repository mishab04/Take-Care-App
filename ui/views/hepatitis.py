# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 11:01:55 2022

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


layout_page = html.Div([html.H3('Hepatitis-C Indicator',className="display-4 text-center"),
               html.Div([
                       html.Div([
                                html.Header('Age'),
                                daq.Slider(
                                       id ='hc_age',
                                       min = 0,
                                       max = 100,
                                       step = 1,
                                       value = 25,
                                       marks = {i:str(i) for i in range(0,101,10)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),   
                                html.Br(),
                                html.Header('Sex'),
                                dcc.RadioItems(id= 'hc_sex',options=[{'label':'Male','value':0}, {'label':'Female','value':1}], value=0, labelStyle = {'display': 'inline-block'}),           
                                html.Br(),
                                html.Header('Albumin Blood Test'),
                                daq.Slider(
                                        id ='hc_alb',
                                       min = 15,
                                       max = 80,
                                       step = .5,
                                       value = 30,
                                       marks = {i:str(i) for i in range(15,81,5)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),
                                html.Br(),
                                html.Header('Alkaline phosphatase'),
                                daq.Slider(
                                        id ='hc_alp',
                                       min = 0,
                                       max = 400,
                                       step = 10,
                                       value = 70,
                                       marks = {i:str(i) for i in range(0,401,50)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),
                                html.Br(),
                                html.Header('Alanine Transaminase'),
                                daq.Slider(
                                       id ='hc_alt',
                                       min = 0,
                                       max = 400,
                                       step = 10,
                                       value = 30,
                                       marks = {i:str(i) for i in range(0,401,50)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),
                                html.Br(),        
                                html.Header('Aspartate Transaminase'),
                                daq.Slider(
                                        id ='hc_ast',
                                       min = 0,
                                       max = 400,
                                       step = 10,
                                       value = 40,
                                       marks = {i:str(i) for i in range(0,401,50)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),
                                
                                     ],className='col-sm-12 col-md-3 order-1 order-md-1'),
                        html.Div([dcc.Graph(id = 'hepatitiswaterfall',style = {'display':'None'}),
                                  html.Div(id = 'hepatitisprediction')], className = 'col-sm-12 col-md-6 order-3 order-md-2 font-weight-bold'),
                        html.Div([
                                html.Header('Bilirubin'),
                                daq.Slider(
                                       id ='hc_bil',
                                       min = 0,
                                       max = 200,
                                       step = 10,
                                       value = 40,
                                       marks = {i:str(i) for i in range(0,201,25)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),                                             
                                html.Br(),
                                html.Header('Acetylcholinesterase'),
                                daq.Slider(
                                       id ='hc_che',
                                       min = 0,
                                       max = 16,
                                       step = .1,
                                       value = 6,
                                       marks = {i:str(i) for i in range(0,17,2)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),                                                
                                html.Br(),                                        
                                html.Header('Cholesterol'),
                                daq.Slider(
                                        id ='hc_cho',
                                       min = 1,
                                       max = 10,
                                       step = .1,
                                       value = 1.2,
                                       marks = {i:str(i) for i in range(1,11,1)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),                                         
                                html.Br(),                                        
                                html.Header('Creatinine'),
                                daq.Slider(
                                        id ='hc_crea',
                                       min = 0,
                                       max = 500,
                                       step = 5,
                                       value = 40,
                                       marks = {i:str(i) for i in range(0,500,50)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),                                         
                                html.Br(),                                        
                                html.Header('Gamma-Glutamyl Transferase'),
                                daq.Slider(
                                        id ='hc_ggt',
                                       min = 0,
                                       max = 500,
                                       step = 5,
                                       value = 40,
                                       marks = {i:str(i) for i in range(0,500,50)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),                                         
                                html.Br(),                                        
                                html.Header('Proteins'),
                                daq.Slider(
                                        id ='hc_prot',
                                       min = 40,
                                       max = 100,
                                       step = 1,
                                       value = 44,
                                       marks = {i:str(i) for i in range(40,101,5)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),                                         
                                html.Br(),
                                dbc.Button(id='submit-hepatitis',children='Submit',n_clicks=0,style = {'background':"#F64C72",'color':'white'})                                                                                 
                                ],className = 'col-sm-12 col-md-3 order-2 order-md-3')],className = 'row')
    
    ],className = 'container-lg')


@app.callback([Output('hepatitisprediction', 'children'),
              Output('hepatitiswaterfall', 'figure'),
              Output('hepatitiswaterfall', 'style')],              
              [Input('submit-hepatitis','n_clicks')],
              [State('hc_age','value'),
               State('hc_sex', 'value'),
               State('hc_alb', 'value'),
               State('hc_alp', 'value'),
               State('hc_alt', 'value'),
               State('hc_ast', 'value'),
               State('hc_bil', 'value'),
               State('hc_che', 'value'),
               State('hc_cho', 'value'),
               State('hc_crea', 'value'),
               State('hc_ggt', 'value'),
               State('hc_prot', 'value'),])
def predict_hepatitis(n_clicks,value1,value2,value3,value4,value5,value6,value7,value8,value9,value10,value11,value12):
    if n_clicks is None:
        raise PreventUpdate
    col_names = ['Age', 'Sex', 'ALB', 'ALP', 'ALT', 'AST', 'BIL', 'CHE','CHOL', 'CREA', 'GGT', 'PROT']
    model = call_model('../models/hepatitisC/hepatitisC_model.pkl')
    X_single_point = pd.DataFrame(data = np.array([[value1,value2,value3,value4,value5,value6,value7,value8,value9,value10,value11,value12]]),
                              columns = col_names            
                              )
    predicted_prob = model.predict_proba(X_single_point)[0]
    predicted_prob = list(predicted_prob)[1]
    explainer = call_model('../models/hepatitisC/hepatitisC_explainer.pkl')
    sv = explainer(X_single_point)
    exp = shap.Explanation(sv.values[:,:,1], 
                  sv.base_values[:,1], 
                  data=X_single_point.values, 
                  feature_names= col_names)
    
    dt = pd.DataFrame({'feature': col_names,'feature_value': exp[0].values})
    text = 'Probability of Having Hepatitis-C is : {}'.format(round(predicted_prob,4))
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