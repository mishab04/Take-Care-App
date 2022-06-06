# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 10:55:14 2022

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


layout_page = html.Div([html.H3('Chronic Kidney Indicator',className="display-4 text-center"),
                        html.Div([
                                html.Div([
                                        html.Header('Age'),
                                        daq.Slider(id ='kidney_age',
                                            min=0, max=100, value=25,
                                            marks={i:str(i) for i in range(0,120,20)},
                                            handleLabel={"showCurrentValue": True,"label": "AGE"},
                                            step = 1,
                                            color = "#F64C72"
                                        ),
                                        html.Br(),                                        
                                        html.Header('Blood Pressure'),
                                        daq.Slider(id ='kidney_bp',
                                            min=50, max=200, value=130,
                                            marks={50:str(50),
                                                80:str(80),
                                                110:str(110),
                                                140:str(140),
                                                170:str(170),
                                                200:str(200)},
                                            handleLabel={"showCurrentValue": True,"label": "BP"},
                                            step = 5,
                                            color = "#F64C72"
                                        ),                                            
                                        html.Br(),                                        
                                        html.Header('specific gravity'),
                                        daq.Slider(id ='kidney_sg',
                                            min=1.005, max=1.025, value=1.01,
                                            marks={1.005:str(1.005),
                                                1.01:str(1.01),
                                                1.015:str(1.015),
                                                1.02:str(1.02),
                                                1.025:str(1.025)},
                                            handleLabel={"showCurrentValue": True,"label": "SG"},
                                            step = .005,
                                            color = "#F64C72"
                                        ),
                                        html.Br(),                                        
                                        html.Header('Albumin'),
                                        daq.Slider(id ='kidney_al',
                                            min=0, max=5, value=2,
                                            marks={i:str(i) for i in range(0,6)},
                                            handleLabel={"showCurrentValue": True,"label": "AL"},
                                            step = 1,
                                            color = "#F64C72"
                                        ),
                                        html.Br(),                                        
                                        html.Header('Sugar'),
                                        daq.Slider(id ='kidney_su',
                                            min=0, max=5, value=2,
                                            marks={i:str(i) for i in range(0,6)},
                                            handleLabel={"showCurrentValue": True,"label": "SU"},
                                            step = 1,
                                            color = "#F64C72"
                                        ),
                                       html.Br(),
                                       html.Header('Red Blood Cell'),
                                       dcc.RadioItems(id= 'kidney_rbc',options=[{'label':'normal','value':'normal'}, {'label':'abnormal','value':'abnormal'}], value='abnormal', labelStyle = {'display': 'inline-block'}),           
                                       html.Br(),
                                       html.Header('Pus Cell Normal'),
                                       dcc.RadioItems(id= 'kidney_pc',options=[{'label':'normal','value':'normal'}, {'label':'abnormal','value':'abnormal'}], value='abnormal', labelStyle = {'display': 'inline-block'}),
                                       html.Br(),
                                       html.Header('Pus Cell Clumps'),
                                       dcc.RadioItems(id= 'kidney_pcc',options=[{'label':'present','value':'present'}, {'label':'notpresent','value':'notpresent'}], value='present', labelStyle = {'display': 'inline-block'}),
                                       html.Br(),
                                       html.Header('Bacteria'),
                                       dcc.RadioItems(id= 'kidney_ba',options=[{'label':'present','value':'present'}, {'label':'notpresent','value':'notpresent'}], value='present', labelStyle = {'display': 'inline-block'}),                                                   
                                       html.Br(),                                        
                                        html.Header('Blood Glucose'),
                                        daq.Slider(id ='kidney_bg',
                                            min=20, max=500, value=200,
                                            marks={i:str(i) for i in range(20,550,70)},
                                            handleLabel={"showCurrentValue": True,"label": "BG"},
                                            step = 20,
                                            color = "#F64C72"
                                        ),
                                        html.Br(),                                        
                                        html.Header('Blood Urea'),
                                        daq.Slider(id ='kidney_bu',
                                            min=0, max=400, value=150,
                                            marks={i:str(i) for i in range(0,450,50)},
                                            handleLabel={"showCurrentValue": True,"label": "BU"},
                                            step = 10,
                                            color = "#F64C72"
                                        ),
                                        html.Br(),                                        
                                        html.Header('Serum Creatinine'),
                                        daq.Slider(id ='kidney_sc',
                                            min=0, max=50, value=30,
                                            marks={i:str(i) for i in range(0,55,5)},
                                            handleLabel={"showCurrentValue": True,"label": "SC"},
                                            step = 2,
                                            color = "#F64C72"
                                        ),
                                        html.Br(),                                        
                                        html.Header('Sodium'),
                                        daq.Slider(id ='kidney_sod',
                                            min=100, max=170, value=125,
                                            marks={i:str(i) for i in range(100,175,10)},
                                            handleLabel={"showCurrentValue": True,"label": "SOD"},
                                            step = 1,
                                            color = "#F64C72"
                                        )                                                                                                                                           
                                        ],'col-sm-12 col-md-3 order-1 order-md-1'),
                            html.Div([dcc.Graph(id = 'kidneywaterfall',style = {'display':'None'}),
                                      html.Div(id = 'kidneyprediction')], className = 'col-sm-12 col-md-6 order-3 order-md-2 font-weight-bold'),
                            html.Div([
                                        html.Header('Potassium'),
                                        daq.Slider(id ='kidney_pot',
                                            min=1, max=10, value=3,
                                            marks={i:str(i) for i in range(1,11,1)},
                                            handleLabel={"showCurrentValue": True,"label": "POT"},
                                            step = 1,
                                            color = "#F64C72"
                                        ),                                         
                                        html.Br(),
                                        html.Header('Hemoglobin'),
                                        daq.Slider(id ='kidney_hemo',
                                            min=2, max=18, value=10,
                                            marks={i:str(i) for i in range(2,20,2)},
                                            handleLabel={"showCurrentValue": True,"label": "HEMO"},
                                            step = 1,
                                            color = "#F64C72"
                                        ),                                          
                                        html.Br(),
                                        html.Header('Packed Cell Volume'),
                                        daq.Slider(id ='kidney_pcv',
                                            min=10, max=55, value=20,
                                            marks={i:str(i) for i in range(10,60,5)},
                                            handleLabel={"showCurrentValue": True,"label": "PCV"},
                                            step = 1,
                                            color = "#F64C72"
                                        ),
                                        html.Br(),
                                        html.Header('White Blood Cell Count'),
                                        daq.Slider(id ='kidney_wc',
                                            min=2000, max=20000, value=10000,
                                            handleLabel={"showCurrentValue": True,"label": "WC"},
                                            step = 500,
                                            color = "#F64C72"
                                        ),
                                        html.Br(),
                                        html.Header('Red Blood Cell Count'),
                                        daq.Slider(id ='kidney_rc',
                                            min=2, max=10, value=3,
                                            marks={i:str(i) for i in range(2,11,1)},
                                            handleLabel={"showCurrentValue": True,"label": "RC"},
                                            step = 1,
                                            color = "#F64C72"
                                        ),                                                       
                                       html.Br(),
                                       html.Header('Hypertension Present'),
                                       dcc.RadioItems(id= 'kidney_htn',options=[{'label':'yes','value':'yes'}, {'label':'no','value':'no'}], value='no', labelStyle = {'display': 'inline-block'}),                                               
                                       html.Br(),
                                       html.Header('Diabetes Mellitus'),
                                       dcc.RadioItems(id= 'kidney_da',options=[{'label':'yes','value':'yes'}, {'label':'no','value':'no'}], value='no', labelStyle = {'display': 'inline-block'}),                                                   
                                       html.Br(),
                                       html.Header('Coronary Artery Disease'),
                                       dcc.RadioItems(id= 'kidney_cad',options=[{'label':'yes','value':'yes'}, {'label':'no','value':'no'}], value='no', labelStyle = {'display': 'inline-block'}),                                                  
                                       html.Br(),
                                       html.Header('Appetite Good'),
                                       dcc.RadioItems(id= 'kidney_app',options=[{'label':'good','value':'good'}, {'label':'poor','value':'poor'}], value='poor', labelStyle = {'display': 'inline-block'}),                                                
                                       html.Br(),
                                       html.Header('Pedal Edema'),
                                       dcc.RadioItems(id= 'kidney_pe',options=[{'label':'yes','value':'yes'}, {'label':'no','value':'no'}], value='no', labelStyle = {'display': 'inline-block'}),                                                  
                                       html.Br(),
                                       html.Header('Anemia'),
                                       dcc.RadioItems(id= 'kidney_ane',options=[{'label':'yes','value':'yes'}, {'label':'no','value':'no'}], value='no', labelStyle = {'display': 'inline-block'}),                                                   
                                       dbc.Button(id='submit-kidney',children='Submit',n_clicks=0,style = {'background':"#F64C72",'color':'white'}) 
                                    ],className = 'col-sm-12 col-md-3 order-2 order-md-3')                       
                                ],className = 'row')
                        ],className = 'container-lg')

@app.callback([Output('kidneyprediction', 'children'),
              Output('kidneywaterfall', 'figure'),
              Output('kidneywaterfall', 'style')],              
              [Input('submit-kidney','n_clicks')],
              [State('kidney_age', 'value'),
               State('kidney_bp', 'value'),
               State('kidney_sg', 'value'),
               State('kidney_al', 'value'),
               State('kidney_su', 'value'),
               State('kidney_rbc', 'value'),
               State('kidney_pc', 'value'),
               State('kidney_pcc', 'value'),
               State('kidney_ba', 'value'),
               State('kidney_bg', 'value'),
               State('kidney_bu', 'value'),
               State('kidney_sc', 'value'),
               State('kidney_sod', 'value'),
               State('kidney_pot', 'value'),
               State('kidney_hemo', 'value'),
               State('kidney_pcv', 'value'),
               State('kidney_wc', 'value'),
               State('kidney_rc', 'value'),
               State('kidney_htn', 'value'),
               State('kidney_da', 'value'),
               State('kidney_cad', 'value'),
               State('kidney_app', 'value'),
               State('kidney_pe', 'value'),
               State('kidney_ane', 'value')])
def predict_chronic_kidney(n_clicks,value1,value2,value3,value4,value5,value6,value7,value8,value9,
                           value10,value11,value12,value13,value14,value15,value16,value17,value18,value19,
                           value20,value21,value22,value23,value24):
    if n_clicks is None:
        raise PreventUpdate
    col_names = ['age', 'blood_pressure', 'specific_gravity', 'albumin', 'sugar', 'red_blood_cells', 'pus_cell',
              'pus_cell_clumps', 'bacteria', 'blood_glucose_random', 'blood_urea', 'serum_creatinine', 'sodium',
              'potassium', 'haemoglobin', 'packed_cell_volume', 'white_blood_cell_count', 'red_blood_cell_count',
              'hypertension', 'diabetes_mellitus', 'coronary_artery_disease', 'appetite', 'peda_edema',
              'aanemia']
    cat_cols = ['red_blood_cells','pus_cell','pus_cell_clumps','bacteria','hypertension','diabetes_mellitus','coronary_artery_disease',
                'appetite','peda_edema','aanemia']
    
    num_cols = ["age","blood_pressure","specific_gravity","albumin","sugar","blood_glucose_random","blood_urea",
                "serum_creatinine","sodium","potassium","haemoglobin","packed_cell_volume","white_blood_cell_count","red_blood_cell_count",]
    
    model = call_model('../models/kidney/kidney_model.pkl')
    one_hot = call_model('../models/kidney/one_hot_kidney.pkl')
    X_single_point = pd.DataFrame(data = np.array([[value1,value2,value3,value4,value5,value6,value7,value8,value9,
                                                    value10,value11,value12,value13,value14,value15,value16,value17,value18,value19,
                                                    value20,value21,value22,value23,value24]]),
                              columns = col_names            
                              )
    cat_data = one_hot.transform(X_single_point[cat_cols])
    cat_columns= ['red_blood_cells_abnormal','red_blood_cells_normal','pus_cell_abnormal','pus_cell_normal','pus_cell_clumps_notpresent',
             'pus_cell_clumps_present','bacteria_notpresent','bacteria_present','hypertension_no','hypertension_yes','diabetes_mellitus_no',
             'diabetes_mellitus_yes','coronary_artery_disease_no','coronary_artery_disease_yes','appetite_good','appetite_poor','peda_edema_no',
             'peda_edema_yes','aanemia_no','aanemia_yes']
    cat_data = pd.DataFrame(cat_data,columns = cat_columns)
    X = pd.concat([X_single_point[num_cols],cat_data],axis = 1)
    predicted_prob = model.predict_proba(X)[0]
    predicted_prob = list(predicted_prob)[1]
    explainer = call_model('../models/kidney/kidney_explainer.pkl')
    sv = explainer(X)
    exp = shap.Explanation(sv.values[:,:,1], 
                  sv.base_values[:,1], 
                  data=X.values, 
                  feature_names= list(X.columns))
    
    dt = pd.DataFrame({'feature': list(X.columns),'feature_value': exp[0].values})
    text = 'Probability of Having Chronic Kidney is : {}'.format(round(predicted_prob,4))
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