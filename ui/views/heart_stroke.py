# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 11:40:46 2022

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


layout_page = html.Div([html.H3('Heart Stoke Indicator',className="display-4 text-center"),
               html.Div([
                       html.Div([
                                html.Header('Sex'),
                                dcc.RadioItems(id= 'hs_sex',options=[{'label':'Male','value':'Male'}, {'label':'Female','value':'Female'}], value='Male', labelStyle = {'display': 'inline-block'}),           
                                html.Br(),
                                html.Header('Age'),
                                daq.Slider(
                                       id ='hs_age',
                                       min = 0,
                                       max = 100,
                                       step = 1,
                                       value = 25,
                                       marks = {i:str(i) for i in range(0,101,10)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),   
                                html.Br(),
                                html.Header('HyperTension'),
                                dcc.RadioItems(id= 'hs_hypertension',options=[{'label':'Yes','value':1}, {'label':'No','value':0}], value=1, labelStyle = {'display': 'inline-block'}),           
                                html.Br(),
                                html.Header('Heart Disease'),
                                dcc.RadioItems(id= 'hs_heartdisease',options=[{'label':'Yes','value':1}, {'label':'No','value':0}], value=1, labelStyle = {'display': 'inline-block'}),           
                                html.Br(),
                                html.Header('Ever Married'),
                                dcc.RadioItems(id= 'hs_evermarried',options=[{'label':'Yes','value':'Yes'}, {'label':'No','value':'No'}], value='Yes', labelStyle = {'display': 'inline-block'}),           
                                html.Header('Work Type'),
                                dcc.RadioItems(id= 'hs_worktype',options=[{'label':'Private','value':'Private'}, {'label':'Self-employed','value':'Self-employed'},
                                                                         {'label':'Govt_job','value':'Govt_job'},{'label':'Never_worked','value':'Never_worked'},
                                                                         {'label':'children','value':'children'}], value='Private', labelStyle = {'display': 'inline-block'}),           
                                         

                                     ],className='col-sm-12 col-md-3 order-1 order-md-1'),
                        html.Div([dcc.Graph(id = 'heartstrokewaterfall',style = {'display':'None'}),
                                  html.Div(id = 'heartstrokeprediction')], className = 'col-sm-12 col-md-6 order-3 order-md-2 font-weight-bold'),
                        html.Div([
                                html.Br(),
                                html.Header('Residence Type'),
                                dcc.RadioItems(id= 'hs_residencetype',options=[{'label':'Urban','value':'Urban'}, {'label':'Rural','value':'Rural'}], value='Rural', labelStyle = {'display': 'inline-block'}),           
                                html.Br(),                                        
                                html.Header('Avg Glucose Level'),
                                daq.Slider(
                                       id ='hs_avgglucoselevel',
                                       min = 50,
                                       max = 300,
                                       step = .5,
                                       value = 80,
                                       marks = {i:str(i) for i in range(50,301,50)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),                                         
                                html.Br(),
                                html.Header('BMI'),
                                daq.Slider(
                                       id ='hs_bmi',
                                       min = 10,
                                       max = 100,
                                       step = .1,
                                       value = 23,
                                       marks = {i:str(i) for i in range(10,101,10)},
                                       handleLabel={"showCurrentValue": True,"label": "Val"},
                                       color = "#F64C72"
                                        ),                                         
                                html.Br(),                                    
                                html.Header('Smoking Status'),
                                dcc.RadioItems(id= 'hs_smokingstatus',options=[{'label':'Formerly Smoked','value':'formerly smoked'}, {'label':'Never Smoked','value':'never smoked'},
                                                                              {'label':'Smokes','value':'smokes'},{'label':'Unknown','value':'Unknown'}], value='formerly smoked', labelStyle = {'display': 'inline-block'}),                                                   
                                dbc.Button(id='submit-heartstroke',children='Submit',n_clicks=0,style = {'background':"#F64C72",'color':'white'})                                                                                 
                                ],className = 'col-sm-12 col-md-3 order-2 order-md-3')],className = 'row')
    
    ],className = 'container-lg')


@app.callback([Output('heartstrokeprediction', 'children'),
              Output('heartstrokewaterfall', 'figure'),
              Output('heartstrokewaterfall', 'style')],              
              [Input('submit-heartstroke','n_clicks')],
              [State('hs_sex','value'),
               State('hs_age', 'value'),
               State('hs_hypertension', 'value'),
               State('hs_heartdisease', 'value'),
               State('hs_evermarried', 'value'),
               State('hs_worktype', 'value'),
               State('hs_residencetype', 'value'),
               State('hs_avgglucoselevel', 'value'),
               State('hs_bmi', 'value'),
               State('hs_smokingstatus', 'value')])
def predict_heartstroke(n_clicks,value1,value2,value3,value4,value5,value6,value7,value8,value9,value10):
    if n_clicks is None:
        raise PreventUpdate        
    col_names = ['gender', 'age', 'hypertension', 'heart_disease', 'ever_married','work_type', 'Residence_type', 'avg_glucose_level', 'bmi','smoking_status']
    
    cat_cols = ['gender','ever_married','work_type','Residence_type','smoking_status']
    
    num_cols = ['age','bmi','avg_glucose_level', 'hypertension', 'heart_disease']
    
    model = call_model('../models/strokes/stroke_model.pkl')
    one_hot = call_model('../models/strokes/one_hot_strokes.pkl')
    X_single_point = pd.DataFrame(data = np.array([[value1,value2,value3,value4,value5,value6,value7,value8,value9,value10]]),
                              columns = col_names            
                              )
    cat_data = one_hot.transform(X_single_point[cat_cols])
    cat_columns = ['gender_female','gender_male','gender_other','ever_married_no','ever_married_yes','work_type_govt_job','work_type_never_worked',
               'work_type_private','work_type_self_employed','work_type_children','resident_type_rural','resident_type_urban','smoking_status_unknown',
               'smoking_status_formerly_smoked','smoking_status_never_smoked','smoking_status_smokes']
    
    cat_data = pd.DataFrame(cat_data,columns = cat_columns)
    X = pd.concat([X_single_point[num_cols],cat_data],axis = 1)
    predicted_prob = model.predict_proba(X)[0]
    predicted_prob = list(predicted_prob)[1]
    explainer = call_model('../models/strokes/explainer_strokes.pkl')
    sv = explainer(X)
    exp = shap.Explanation(sv.values[:,:,1], 
                  sv.base_values[:,1], 
                  data=X.values, 
                  feature_names= list(X.columns))
    
    dt = pd.DataFrame({'feature': list(X.columns),'feature_value': exp[0].values})
    text = 'Probability of Having Heart Stroke is : {}'.format(round(predicted_prob,4))
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

