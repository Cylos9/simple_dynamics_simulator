#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: main.py

Description:
    This script performs data analysis on a given dataset. It includes functions to load the data,
    preprocess it, and generate various statistical summaries and visualizations.

Usage:
    To run this script, use the following command:
        python example.py <input_file>
    where <input_file> is the path to the dataset you want to analyze.

Author:
    Loc Dang 

Contact:
    bobdbl99@gmail.com
    
Date:
    May 24, 2024

License:
    BSD 3-Clause License

    Redistribution and use in source and binary forms, with or without modification,
    are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this
       list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice, this
       list of conditions and the following disclaimer in the documentation and/or
       other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its contributors
       may be used to endorse or promote products derived from this software without
       specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
    IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
    INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
    NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
    WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
    OF SUCH DAMAGE.
"""
import os
from pathlib import Path
import sys

package_path = str(Path(__file__).resolve().parent.parent)
sys.path.append(os.path.join(package_path, "simple_dynamics_simulator"))

import casadi.casadi as cs

from simple_dynamics_simulator.model import Model
from simple_dynamics_simulator.graphic.graphic_object import Rectangle, Circle


class TractorTrailerModel(Model):
        
    def __init__(self, model_params, discrete_method = "KR1", step_size = 0.1):
        
        super().__init__(model_params, discrete_method, step_size)
        
        self._nx = model_params["num_states"]
        
        self._nu = model_params["num_inputs"]
        
        self._lb = model_params["length_back"]
        
        self._lf = model_params["length_front"]
        
    def dynamics(self, state, input):
        
        if len(state) != self._nx or len(input) != self._nu:
            print("[WARN] Number of states or inputs is not matched.")
            return
        
        v1, w1 = input
        
        state_dot = []
        
        if self._nx == 6:
            
            x1 , y1 , theta1, x2 , y2 , theta2 =  state
            
            gamma = theta2 - theta1
            
            x1_dot = v1 * cs.cos(theta1)
            
            y1_dot = v1 * cs.sin(theta1)
            
            theta1_dot = w1 
            
            x2_dot = v1 * cs.cos(theta2) * cs.cos(gamma) - w1 * self._lb * cs.cos(theta2) * cs.sin(gamma)
            
            y2_dot = v1 * cs.sin(theta2) * cs.cos(gamma) - w1 * self._lb * cs.sin(theta2) * cs.sin(gamma)
            
            theta2_dot = - v1 * (1 / self._lf) * cs.sin(gamma) - w1 * (self._lb / self._lf) * cs.cos(gamma)      
            
            state_dot = [x1_dot, y1_dot, theta1_dot, x2_dot, y2_dot, theta2_dot]         
            
        elif self._nx == 4:
            
            x2 , y2 , theta2, gamma =  state
            
            x2_dot = v1 * cs.cos(theta2) * cs.cos(gamma) - w1 * self._lb * cs.cos(theta2) * cs.sin(gamma)
            
            y2_dot = v1 * cs.sin(theta2) * cs.cos(gamma) - w1 * self._lb * cs.sin(theta2) * cs.sin(gamma)
            
            theta2_dot = - v1 * (1 / self._lf) * cs.sin(gamma) - w1 * (self._lb / self._lf) * cs.cos(gamma)
            
            gamma_dot = - v1 * (1 / self._lf) * cs.sin(gamma) - w1 * ((self._lb / self._lf) * cs.cos(gamma) + 1)
            
            state_dot = [x2_dot, y2_dot, theta2_dot, gamma_dot]
            
        return  state_dot

    def graphic_model(self, state):
        
        x2, y2, theta2, gamma = state
        
        x1, y1, theta1 = self._compute_tractor_state(state)
        
        graphic_model = []
        
        graphic_model_params = self._model_params["graphic_model_params"]
 
        # Tractor       
        tractor = graphic_model_params["tractor"]

        pose = [x1 + tractor["length"] / 2 * cs.cos(theta1), 
                y1 + tractor["length"] / 2 * cs.sin(theta1), 
                theta1]
        
        graphic_model.append(Rectangle("tractor", pose, tractor["length"], tractor["width"]))
        
        # Trailer
        trailer = graphic_model_params["trailer"]
        
        pose = [x2 + trailer["length"] / 2 * cs.cos(theta1), 
                y2 + trailer["length"] / 2 * cs.sin(theta1), 
                theta1]
        
        graphic_model.append(Rectangle("trailer", pose, trailer["length"], trailer["width"]))
        
        # Connected Joint
        connected_joint  = graphic_model_params["connected_joint"]
        
        pose = [x2 + self._lf  * cs.cos(theta1), 
                y2 + self._lf  * cs.sin(theta1), 
                theta1]
                
        graphic_model.append(Circle("connected_joint", pose, connected_joint["radius"]))
        
        return graphic_model   

    def _compute_tractor_state(self, state):
        
        if len(state) != 4:
            return
        
        x2, y2, theta2, gamma = state
        
        theta1 = theta2 - gamma
        
        x1 = x2 + self._lf * cs.cos(theta2) + self._lb * cs.cos(theta1)
        
        y1 = y2 + self._lf * cs.sin(theta2) + self._lb * cs.sin(theta1)

        return [x1, y1, theta1]
    
