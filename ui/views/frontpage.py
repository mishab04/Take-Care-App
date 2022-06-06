# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 10:35:51 2022

@author: User
"""

from dash import html



layout_page = html.Div([ html.H1('Early Detection of Dieases', style = {'text-align': 'center'}),
                        html.Br(),
                        html.Br(),
                html.Div([
                          html.Div(
                                   [html.A(html.Img(src='../static/images/breastcancer.jpg',className = 'imgclass'),href = '/breast_cancer'),
                                   html.Div('Breast Cancer')],
                                   className = 'col-4 content_img'),
                          html.Div(
                                   [html.A(html.Img(src='../static/images/diabetes.jpg',className = 'imgclass'),href = '/diabetes'),
                                   html.Div('Diabetes')],
                                   className = 'col-4 content_img'),                              
                          html.Div(
                                   [html.A(html.Img(src='../static/images/hepatitisC.jpg',className = 'imgclass'),href = '/hepatitisC'),
                                   html.Div('Hepatitis C')],
                                   className = 'col-4 content_img'),
                                  ]
                        ),
                html.Div([
                          html.Div(
                                   [html.A(html.Img(src='../static/images/heart.jpg',className = 'imgclass'),href = '/heart'),
                                   html.Div('Chronic Heart Dieases')],
                                   className = 'col-4 content_img'),
                          html.Div(
                                   [html.A(html.Img(src='../static/images/kidney.jpg',className = 'imgclass'),href = '/kidney'),
                                   html.Div('Chronic Kidney')],
                                   className = 'col-4 content_img'),
                          html.Div(
                                   [html.A(html.Img(src='../static/images/heart_stroke.jpg',className = 'imgclass'),href = '/heartstroke'),
                                   html.Div('Heart Stroke')],
                                   className = 'col-4 content_img'),
                         ]
                        )
        
        ], className = "center")
    
