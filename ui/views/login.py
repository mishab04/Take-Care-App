# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 19:00:37 2022

@author: User
"""

from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app, User
from flask_login import login_user
from werkzeug.security import check_password_hash


layout_page = dbc.Container([
    html.Br(),
    dbc.Container([
        dcc.Location(id='urlLogin', refresh=True),
        html.Div([
            dbc.Container(id='loginType', children=[
                dcc.Input(
                    placeholder='Enter your username',
                    type='text',
                    id='usernameBox',
                    className='form-control',
                    n_submit=0,
                ),
                html.Br(),
                dcc.Input(
                    placeholder='Enter your password',
                    type='password',
                    id='passwordBox',
                    className='form-control',
                    n_submit=0,
                ),
                html.Br(),
                dbc.Button(id='loginButton',children='Login',n_clicks=0,style = {'background':"#2F2FA2",'color':'white'}),     
                html.Br(),
            ], className='form-group'),
        ]),
    ], className='jumbotron',style = {'background':"#F64C72"})
])



################################################################################
# LOGIN BUTTON CLICKED / ENTER PRESSED - REDIRECT TO PAGE1 IF LOGIN DETAILS ARE CORRECT
################################################################################
@app.callback(Output('urlLogin', 'pathname'),
              [Input('loginButton', 'n_clicks'),
              Input('usernameBox', 'n_submit'),
              Input('passwordBox', 'n_submit')],
              [State('usernameBox', 'value'),
               State('passwordBox', 'value')])
def sucess(n_clicks, usernameSubmit, passwordSubmit, username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            return '/login'
        else:
            pass
    else:
        pass


################################################################################
# LOGIN BUTTON CLICKED / ENTER PRESSED - RETURN RED BOXES IF LOGIN DETAILS INCORRECT
################################################################################
@app.callback(Output('usernameBox', 'className'),
              [Input('loginButton', 'n_clicks'),
              Input('usernameBox', 'n_submit'),
              Input('passwordBox', 'n_submit')],
              [State('usernameBox', 'value'),
               State('passwordBox', 'value')])
def update_output(n_clicks, usernameSubmit, passwordSubmit, username, password):
    if (n_clicks > 0) or (usernameSubmit > 0) or (passwordSubmit) > 0:
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                return 'form-control'
            else:
                return 'form-control is-invalid'
        else:
            return 'form-control is-invalid'
    else:
        return 'form-control'

