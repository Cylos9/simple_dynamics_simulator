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

import sys
import os 
import math
from copy import deepcopy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import casadi.casadi as cs
import numpy as np
from simple_dynamics_simulator.model import Model
from simple_dynamics_simulator.graphic.graphic_object import Rectangle, Circle


class TractorTrailerModel(Model):
        
    def __init__(self, params):
        
        super().__init__(params["standard_params"])
        
        self._graphic_model_params = params["graphic_model_params"]
        
        additional_params = params["additional_params"]
        
        self._lb = additional_params["length_back"]
        
        self._lf = additional_params["length_front"]
        
        
    def dynamics(self, state, input):
        
        if len(state) != self._nx or len(input) != self._nu:
            raise Exception("Failed to compute dynamics. The size of input arguments is not matched with the size of state or control input")
        
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
            
        return  np.asarray(state_dot)

    def graphic_model(self, state):

        trailer_pose  = state[0:3]
        
        tractor_pose = self._compute_tractor_pose(state)
        
        graphic_model = []
 
        # Tractor       
        tractor = self._graphic_model_params["tractor"]
        
        translation = [tractor["width"] / 4 * cs.cos(tractor_pose[2]), 
                       tractor["width"] / 4 * cs.sin(tractor_pose[2])]
        
        pose = self._transform_pose(tractor_pose, translation, 0.)
        
        graphic_model.append(Rectangle("tractor", pose, tractor["width"], tractor["height"]))
        
        # Trailer
        trailer = self._graphic_model_params["trailer"]

        translation = [trailer["width"] / 4 * cs.cos(trailer_pose[2]), 
                       trailer["width"] / 4 * cs.sin(trailer_pose[2])]
        
        pose = self._transform_pose(trailer_pose, translation, 0.)  
          
        graphic_model.append(Rectangle("trailer", pose, trailer["width"], trailer["height"]))
        
        # hitch_joint
        hitch_joint  = self._graphic_model_params["hitch_joint"]
        
        translation = [self._lf  * cs.cos(trailer_pose[2]),  
                       self._lf  * cs.sin(trailer_pose[2])]
        
        pose = self._transform_pose(trailer_pose, translation, 0.) 
                  
        graphic_model.append(Circle("hitch_joint", pose, hitch_joint["radius"]))

        #front_wheels
        front_wheel = self._graphic_model_params["front_wheels"]
        
        rw_translation = [(tractor["height"]/2 + front_wheel["height"]/2 + 0.05) * cs.sin(tractor_pose[2]),  
                          - (tractor["height"]/2 + front_wheel["height"]/2 + 0.05) * cs.cos(tractor_pose[2])]
        
        lw_translation = [-(tractor["height"]/2 + front_wheel["height"]/2 + 0.05) * cs.sin(tractor_pose[2]),  
                           (tractor["height"]/2 + front_wheel["height"]/2 + 0.05) * cs.cos(tractor_pose[2])]
        
        rw_pose = self._transform_pose(tractor_pose, rw_translation, 0.) 
        
        lw_pose = self._transform_pose(tractor_pose, lw_translation, 0.) 
                 
        graphic_model.append(Rectangle("front_right_wheel", rw_pose, front_wheel["width"], front_wheel["height"]))
        
        graphic_model.append(Rectangle("front_left_wheel", lw_pose, front_wheel["width"], front_wheel["height"]))


        #back_wheels
        back_wheel = self._graphic_model_params["back_wheels"]
        
        rw_translation = [(trailer["height"]/2 + back_wheel["height"]/2 + 0.05) * cs.sin(trailer_pose[2]),  
                          - (trailer["height"]/2 + back_wheel["height"]/2 + 0.05) * cs.cos(trailer_pose[2])]
        
        lw_translation = [-(trailer["height"]/2 + back_wheel["height"]/2 + 0.05) * cs.sin(trailer_pose[2]),  
                           (trailer["height"]/2 + back_wheel["height"]/2 + 0.05) * cs.cos(trailer_pose[2])]
        
        rw_pose = self._transform_pose(trailer_pose, rw_translation, 0.) 
        
        lw_pose = self._transform_pose(trailer_pose, lw_translation, 0.) 
                 
        graphic_model.append(Rectangle("front_right_wheel", rw_pose, back_wheel["width"], back_wheel["height"]))
        
        graphic_model.append(Rectangle("front_left_wheel", lw_pose, back_wheel["width"], back_wheel["height"]))
        
        return graphic_model   

    def _compute_tractor_pose(self, state):
        
        if len(state) != 4:
            raise Exception("Failed to compute tractor pose. The size of state is expected to be equal to 4")
        
        x2, y2, theta2, gamma = state
        
        theta1 = theta2 - gamma
        
        x1 = x2 + self._lf * cs.cos(theta2) + self._lb * cs.cos(theta1)
        
        y1 = y2 + self._lf * cs.sin(theta2) + self._lb * cs.sin(theta1)

        return np.asarray([x1, y1, theta1])
    

    def _transform_pose(self, pose, translation, rotate_angle, degree=False):
        
        transformed_pose = deepcopy(pose)
        
        transformed_pose[0] += translation[0]
        
        transformed_pose[1] += translation[1]
        
        if degree:
            rotate_angle = rotate_angle * math.pi / 180
            
        transformed_pose[2] += rotate_angle
        
        return transformed_pose