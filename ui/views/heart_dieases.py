# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 11:25:43 2022

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

layout_page = html.Div([html.H3('Heart Dieases Indicator',className="display-4 text-center"),
               html.Div([
                       html.Div([
                                html.Header('Age'),
                                daq.Slider(
                                       id ='h_age',
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
                                dcc.RadioItems(id= 'h_sex',options=[{'label':'Male','value':'M'}, {'label':'Female','value':'F'}], value='M', labelStyle = {'display': 'inline-block'}),           
                                html.Br(),
                                html.Header('Chest Pain Type'),
                                dcc.RadioItems(id= 'h_chestpaintype',options=[{'label':'ATA','value':'ATA'}, {'label':'NAP','value':'NAP'},
                                                                              {'label':'ASY','value':'ASY'},{'label':'TA','value':'TA'}], value='ATA', labelStyle = {'display': 'inline-block'}),           
                                html.Br(),
                                html.Header('RestingBP'),
                                daq.Slider(
                                        id ='h_restingbp',
                                       min = 0,
                                       max = 200,
                                       step = 5,
                                       value = 120,
                                       marks = {i:str(i) for i in range(0,210,20)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),
                                html.Br(),
                                html.Header('Cholesterol'),
                                daq.Slider(
                                        id ='h_cholesterol',
                                       min = 0,
                                       max = 600,
                                       step = 10,
                                       value = 70,
                                       marks = {i:str(i) for i in range(0,610,100)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),
                                html.Br(),        
                                html.Header('FastingBS'),
                                dcc.RadioItems(id= 'h_fastingbs',options=[{'label':'0','value':0}, {'label':'1','value':1}], value=0, labelStyle = {'display': 'inline-block'}),                                                          
                                     ],className='col-sm-12 col-md-3 order-1 order-md-1'),
                        html.Div([dcc.Graph(id = 'heartwaterfall',style = {'display':'None'}),
                                  html.Div(id = 'heartprediction')], className = 'col-sm-12 col-md-6 order-3 order-md-2 font-weight-bold'),
                        html.Div([
                                html.Header('Resting ECG'),
                                dcc.RadioItems(id= 'h_restingECG',options=[{'label':'Normal','value':'Normal'}, {'label':'ST','value':'ST'},
                                                                              {'label':'LVH','value':'LVH'}], value='LVH', labelStyle = {'display': 'inline-block'}),           
                                         
                                html.Br(),
                                html.Header('Max Heart Rate'),
                                daq.Slider(
                                        id ='h_mhr',
                                       min = 60,
                                       max = 200,
                                       step = 1,
                                       value = 120,
                                       marks = {i:str(i) for i in range(60,201,20)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),                                                
                                html.Br(),                                        
                                html.Header('Exercise Angina'),
                                dcc.RadioItems(id= 'h_exerciseangina',options=[{'label':'Yes','value':'Y'}, {'label':'No','value':'N'}], value='Y', labelStyle = {'display': 'inline-block'}),                                                          
                                html.Br(),                                        
                                html.Header('Oldpeak'),
                                daq.Slider(
                                        id ='h_oldspeak',
                                       min = -3,
                                       max = 7,
                                       step = .1,
                                       value = 1.2,
                                       marks = {i:str(i) for i in range(-3,8,1)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),                                         
                                html.Br(),
                                html.Header('ST Slope'),
                                dcc.RadioItems(id= 'h_stslope',options=[{'label':'Up','value':'Up'}, {'label':'Flat','value':'Flat'},
                                                                              {'label':'Down','value':'Down'}], value='Up', labelStyle = {'display': 'inline-block'}),                                                   
                                dbc.Button(id='submit-heart',children='Submit',n_clicks=0,style = {'background':"#F64C72",'color':'white'})                                                                                 
                                ],className = 'col-sm-12 col-md-3 order-2 order-md-3')],className = 'row')
    
    ],className = 'container-lg')


@app.callback([Output('heartprediction', 'children'),
              Output('heartwaterfall', 'figure'),
              Output('heartwaterfall', 'style')],              
              [Input('submit-heart','n_clicks')],
              [State('h_age', 'value'),
               State('h_sex', 'value'),
               State('h_chestpaintype', 'value'),
               State('h_restingbp', 'value'),
               State('h_cholesterol', 'value'),
               State('h_fastingbs', 'value'),
               State('h_restingECG', 'value'),
               State('h_mhr', 'value'),
               State('h_exerciseangina', 'value'),
               State('h_oldspeak', 'value'),
               State('h_stslope', 'value'),])
def predict_heart(n_clicks,value1,value2,value3,value4,value5,value6,value7,value8,value9,value10,value11):    
    if n_clicks is None:
        raise PreventUpdate
    col_names = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS',
       'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope']
    
    cat_cols = ['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope']
    
    num_cols = ['Age','RestingBP','Cholesterol','FastingBS','MaxHR','Oldpeak']
    
    model = call_model('../models/heart/heart_model.pkl')
    one_hot = call_model('../models/heart/one_hot_heart.pkl')
    X_single_point = pd.DataFrame(data = np.array([[value1,value2,value3,value4,value5,value6,value7,value8,value9,value10,value11]]),
                              columns = col_names            
                              )
    cat_data = one_hot.transform(X_single_point[cat_cols])
    cat_columns = ['sex_female','sex_male','chestpain_asy','chestpain_ata','chestpain_nap','chestpain_ta','RestingECG_LVH','RestingECG_Normal','RestingECG_ST','ExerciseAngina_N','ExerciseAngina_Y','ST_Slope_Down','ST_Slope_Flat','ST_Slope_Up']
    cat_data = pd.DataFrame(cat_data,columns = cat_columns)
    X = pd.concat([X_single_point[num_cols],cat_data],axis = 1)
    predicted_prob = model.predict_proba(X)[0]
    predicted_prob = list(predicted_prob)[1]
    explainer = call_model('../models/heart/explainer.pkl')
    sv = explainer(X,check_additivity=False)
    exp = shap.Explanation(sv.values[:,:,1], 
                  sv.base_values[:,1], 
                  data=X.values, 
                  feature_names= list(X.columns))
    
    dt = pd.DataFrame({'feature': list(X.columns),'feature_value': exp[0].values})
    text = 'Probability of Having Heart Dieases is : {}'.format(round(predicted_prob,4))
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