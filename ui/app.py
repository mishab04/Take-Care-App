# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 11:47:12 2022

@author: User
"""

import dash
import dash_bootstrap_components as dbc
from flask_login import LoginManager, UserMixin
import os
from user_mgt import db, User as base

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config.suppress_callback_exceptions = True

server = app.server


server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI="postgresql://postgres:Abhinav@90@localhost:5432/users",
    SQLALCHEMY_TRACK_MODIFICATIONS=False
        )

db.init_app(server)

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

# Create User class with UserMixin
class User(UserMixin, base):
    pass

# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))