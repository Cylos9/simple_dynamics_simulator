#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: animator.py

Description:
    This script defines the Animator class, which is used to animate the simulation of a dynamical system.
    
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

import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, pi
from matplotlib.collections import PatchCollection
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.animation as animation

class Animator:
    
    def __init__(self, param, model):
        
        self._param = param
        
        self._model = model
        
        self._frame_rate = param["desired_frame_rate"]
        
        self._figure, self._axes = plt.subplots()
            
    def run(self, states, static_paths={}, dynamic_paths={}, environment=None):
        
        states, extraction_ratio = self._truncate_state_for_animate(states)

        dynamic_paths = self._truncate_dynamic_path_for_animate(dynamic_paths, extraction_ratio)
                                   
        dynamic_artists = self._generate_dynamic_artists(states, dynamic_paths)
                        
        self._configure_plot_setting(static_paths.keys(), dynamic_paths.keys())
                          
        self._animate(dynamic_artists, static_paths, environment)

    def _generate_dynamic_artists(self, states, dynamic_paths):
            
        dynamic_artists = []
        
        for i in  range(states.shape[1]):
            
            artist_collection = []
            
            # Dynamic path
            for index, (path_name, path_value) in enumerate(dynamic_paths.items()):
                
                artist_collection += self._axes.plot(path_value[0, :i], path_value[1, :i], linestyle='-', color=self._param['dynamic_path_color'][index], label=path_name, animated=True)
  
            # Robot path collection
            state = states[:,i]
            
            graphic_model = self._model.graphic_model(state)

            artist_collection += self._get_patch_collection(graphic_model)

            dynamic_artists.append(artist_collection)
            
        return dynamic_artists
        
    def _animate(self, dynamic_artists, static_paths, environment):
        
        # Static plot
        for index, (path_name, path_value) in enumerate(static_paths.items()):
            
            self._axes.plot(path_value[0, :], path_value[1, :], linestyle='dotted', color=self._param['static_path_color'][index], label=path_name)
            
        if type(environment) != type(None):
            pass
        
        # Dynamic plot
        time_interval_between_frames = 1000 / self._frame_rate / self._param["speed_factor"] #in milisecond
        
        print(f"[Animator][Info] frame_rate: {self._frame_rate:.2f} fps , speed_factor: {self._param['speed_factor']}")
        
        anim = animation.ArtistAnimation(fig=self._figure, 
                                        artists=dynamic_artists, 
                                        interval=time_interval_between_frames, 
                                        repeat=self._param["repeat"],
                                        blit=True)

        plt.show() 
           
    def _get_patch_collection(self, graphic_model):
        
        patches = []

        for graphic_object in graphic_model:
            
            if graphic_object.type == "rectangle":
                
                patches.append(self._generate_rectangle_patch(graphic_object))

            elif graphic_object.type == "circle":
                
                patches.append(self._generate_circle_patch(graphic_object))

            else:
                print("[animator][Warning] '{graphic_object.type}' is not defined")
                
        return patches
    
    
    def _generate_rectangle_patch(self, graphic_object):
        
        #compute anchor point
        x_c, y_c = graphic_object.center
        
        theta = graphic_object.rotate_angle
        
        x = x_c - graphic_object.width / 2 
        
        y = y_c - graphic_object.height / 2
        
        theta_in_deg = theta * 180 / pi 
        
        patch = mpatches.Rectangle((x, y), graphic_object.width, graphic_object.height, 
                  angle=theta_in_deg, rotation_point='center', color=self._param["robot_color"], animated=True)
         
        return self._axes.add_patch(patch)
        
    def _generate_circle_patch(self, graphic_object):

        x_c, y_c = graphic_object.center
         
        patch = mpatches.Circle((x_c, y_c), radius = graphic_object.radius,  color=self._param["robot_color"], animated=True)
        
        return self._axes.add_patch(patch)
    
    def _configure_plot_setting(self, static_pathnames, dynamic_pathnames):
                
        # Plot setting
        self._axes.set(xlim=[self._param["xlim_lb"], self._param["xlim_ub"]], 
                            ylim=[self._param["ylim_lb"], self._param["ylim_ub"]], 
                            xlabel='X', ylabel='Y',
                            title='Simulation in 2D space')
                
        self._axes.set_aspect("equal", adjustable="box")

        # Configure legend
        legend_handles = []
        
        legend_handles.append(mpatches.Patch(color=self._param["robot_color"], label='Robot'))
        
        for index, path_name in enumerate(static_pathnames):
            legend_handles.append(mlines.Line2D([], [], linestyle='--', color=self._param['static_path_color'][index], label=path_name))

        for index, path_name in enumerate(dynamic_pathnames):
            legend_handles.append(mlines.Line2D([], [], linestyle='-', color=self._param['dynamic_path_color'][index], label=path_name))

        self._axes.legend(handles=legend_handles, loc="upper right")
    
    def _truncate_state_for_animate(self, states):
        
        num_states_in_second = 1 / self._model._step_size
        
        if num_states_in_second < self._param["desired_frame_rate"]:
            print(f"[Warn] The frame rate was reduced from {self._param['desired_frame_rate']} to {num_states_in_second},",
                f"since the number of simulated states ({num_states_in_second}) within a second is lower than required frames ({self._param['desired_frame_rate']})")
            
            extraction_ratio = 1
            
            self._frame_rate =  1 / self._model._step_size

        else:
            extraction_ratio = int(num_states_in_second / self._param["desired_frame_rate"])
            
            self._frame_rate = 1 / (self._model._step_size * extraction_ratio)
        
        states = states[:, 0::extraction_ratio]
        
        return states, extraction_ratio
    
    @staticmethod
    def _truncate_dynamic_path_for_animate(dynamic_paths, extraction_ratio):
        
        for path_name, path_value in dynamic_paths.items():
            
            dynamic_paths[path_name] = path_value[:, 0::extraction_ratio]
            
        return dynamic_paths
                        