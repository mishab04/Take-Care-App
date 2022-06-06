# -*- coding: utf-8 -*-
"""
Created on Sat May 28 21:54:53 2022

@author: User
"""

import pickle

def call_model(pickle_path): 
    # Load from file
    with open(pickle_path, 'rb') as file:
        pickle_model = pickle.load(file)
    
    return pickle_model