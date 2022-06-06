# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 11:46:33 2022

@author: User
"""

import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from views import breast_cancer,diabetes,frontpage,heart_dieases,heart_stroke,hepatitis,kidney,login

from app import app, server
from flask_login import logout_user, current_user

logo = dbc.Navbar(id = 'navBar',

    children = [],
    color="#F64C72",
    dark=True,
    #className="mb-5",
    sticky = "top"
)

app.layout = html.Div([dcc.Location(id="url",refresh=False),logo,html.Br(),html.Div(id='page-content')])



@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/":
        if current_user.is_authenticated:
            return frontpage.layout_page
        else:
            return login.layout_page    
    elif pathname == "/breast_cancer":
        if current_user.is_authenticated:
            return breast_cancer.layout_page
        else:
            return login.layout_page
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return login.layout_page
        else:
            return login.layout_page       
    elif pathname == "/diabetes":
        if current_user.is_authenticated:
            return diabetes.layout_page
        else:
            return login.layout_page
    elif pathname == "/hepatitisC":
        if current_user.is_authenticated:
            return hepatitis.layout_page
        else:
            return login.layout_page
    elif pathname == "/heart":
        if current_user.is_authenticated:
            return heart_dieases.layout_page
        else:
            return login.layout_page
    elif pathname == "/kidney":
        if current_user.is_authenticated:
            return kidney.layout_page
        else:
            return login.layout_page
    elif pathname == "/heartstroke":
        if current_user.is_authenticated:
            return heart_stroke.layout_page
        else:
            return login.layout_page
    elif pathname == "/login":
        if current_user.is_authenticated:
            return frontpage.layout_page
        else:
            return login.layout_page
    else:
        return login.layout_page

@app.callback(Output('navBar', 'children'),
              [Input('page-content', 'children')])
def update(children):
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        children = html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                           html.Img(src='/static/images/Takecare.png', height="45px",width = "120px"),
                           
                            dbc.NavLink("Home",href="/",style = {'color':'white'}),
                            dbc.NavLink("About",href="/about",style = {'color':'white'}),
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                )
    
        return children
    else:
        children = html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                           html.Img(src='/static/images/Takecare.png', height="45px",width = "120px"),
                                                   ],
                        align="center",
                        no_gutters=True,
                    ),
                )
        return children

if __name__ == "__main__":
    app.run_server(debug=False)