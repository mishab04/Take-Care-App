# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 10:39:58 2022

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



layout_page = html.Div([html.H3('Breast Cancer Indicator',className="display-4 text-center"),
                   html.Div([
                           html.Div([
                                   html.Header('Clump Thickness'),
                                   daq.Slider(
                                           id='clump_thickness',
                                           min = 1,
                                           max = 10,
                                           step = 1,
                                           value = 3,
                                           marks = {i:str(i) for i in range(1,11)},
                                           color = "#F64C72"
                                           ),
                                    html.Br(),
                                    html.Header('Uniformity of Cell Size'),
                                    daq.Slider(
                                            id ='uniformity_of_cell_size',
                                               min = 1,
                                               max = 10,
                                               step = 1,
                                               value = 3,
                                               marks = {i:str(i) for i in range(1,11)},
                                            color = "#F64C72"
                                            ),
                                    html.Br(),
                                    html.Header('Uniformity of Cell Shape'),
                                    daq.Slider(
                                            id = 'uniformity_of_cell_shape',
                                               min = 1,
                                               max = 10,
                                               step = 1,
                                               value = 3,
                                               marks = {i:str(i) for i in range(1,11)},
                                            color = "#F64C72"
                                            ),
                                    html.Br(),
                                    html.Header('Marginal Adhesion'),
                                    daq.Slider(
                                            id ='marginal_adhesion',
                                           min = 1,
                                           max = 10,
                                           step = 1,
                                           value = 3,
                                           marks = {i:str(i) for i in range(1,11)},
                                           color = "#F64C72"
                                            ),
                                    html.Br(),
                                    html.Header('Single Epithelial Cell Size'),
                                    daq.Slider(
                                            id ='single_epithelial_cell_size',
                                           min = 1,
                                           max = 10,
                                           step = 1,
                                           value = 3,
                                           marks = {i:str(i) for i in range(1,11)},
                                           color = "#F64C72"
                                            ),                                                
                                         ],className='col-sm-12 col-md-3 order-1 order-md-1'),
                            html.Div([dcc.Graph(id = 'breastcancerwaterfall',style = {'display':'None'}),
                                      html.Div(id = 'breastcancerprediction')], className = 'col-sm-12 col-md-6 order-3 order-md-2 font-weight-bold'),
                            html.Div([
                                    html.Header('Bare Nuclei'),
                                   daq.Slider(
                                            id ='bare_nuclei',
                                           min = 1,
                                           max = 10,
                                           step = 1,
                                           value = 3,
                                           marks = {i:str(i) for i in range(1,11)},
                                           color = "#F64C72"
                                            ),                                                
                                    html.Br(),
                                    html.Header('Bland Chromatin'),
                                    daq.Slider(
                                            id ='bland_chromatin',
                                           min = 1,
                                           max = 10,
                                           step = 1,
                                           value = 3,
                                           marks = {i:str(i) for i in range(1,11)},
                                           color = "#F64C72"
                                            ),                                                
                                    html.Br(),                                        
                                    html.Header('Normal Nucleoli'),
                                    daq.Slider(
                                            id ='normal_nucleoli',
                                           min = 1,
                                           max = 10,
                                           step = 1,
                                           value = 3,
                                           marks = {i:str(i) for i in range(1,11)},
                                           color = "#F64C72"
                                            ),                                                 
                                    html.Br(),                                        
                                    html.Header('Mitoses'),
                                    daq.Slider(
                                            id ='mitoses',
                                           min = 1,
                                           max = 10,
                                           step = 1,
                                           value = 3,
                                           marks = {i:str(i) for i in range(1,11)},
                                           color = "#F64C72"
                                            ),                                          
                                    html.Br(),                                        
                                    dbc.Button(id='submit-breast_cancer',children='Submit',n_clicks=0,style = {'background':"#F64C72",'color':'white'})                                                                                 
                                    ],className = 'col-sm-12 col-md-3 order-2 order-md-3')],className = 'row')
        
        ],className = 'container-lg')

@app.callback([Output('breastcancerprediction', 'children'),
              Output('breastcancerwaterfall', 'figure'),
              Output('breastcancerwaterfall', 'style')],              
              [Input('submit-breast_cancer','n_clicks')],
              [State('clump_thickness', 'value'),
               State('uniformity_of_cell_size', 'value'),
               State('uniformity_of_cell_shape', 'value'),
               State('marginal_adhesion', 'value'),
               State('single_epithelial_cell_size', 'value'),
               State('bare_nuclei', 'value'),
               State('bland_chromatin', 'value'),
               State('normal_nucleoli', 'value'),
               State('mitoses', 'value')])
def predict_breast_cancer(n_clicks,value1,value2,value3,value4,value5,value6,value7,value8,value9):
    if n_clicks is None:
        raise PreventUpdate
    col_names = ['Clump_Thickness', 'Uniformity_of_Cell_Size','Uniformity_of_Cell_Shape', 'Marginal_Adhesion',
                 'Single_Epithelial_Cell_Size', 'Bare_Nuclei', 'Bland_Chromatin','Normal_Nucleoli', 'Mitoses']
    model = call_model('../models/breastcancer/breastcancer_model.pkl')
    X_single_point = pd.DataFrame(data = np.array([[value1,value2,value3,value4,int(value5),int(value6),value7,value8,value9]]),
                              columns = col_names            
                              )
    predicted_prob = model.predict_proba(X_single_point)[0]
    predicted_prob = list(predicted_prob)[1]
    explainer = call_model('../models/breastcancer/breastcancer_explainer.pkl')
    sv = explainer(X_single_point)
    exp = shap.Explanation(sv.values[:,:,1], 
                  sv.base_values[:,1], 
                  data=X_single_point.values, 
                  feature_names= col_names)
    
    dt = pd.DataFrame({'feature': col_names,'feature_value': exp[0].values})
    text = 'Probability of Having Breast Cancer is : {}'.format(round(predicted_prob,4))
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

