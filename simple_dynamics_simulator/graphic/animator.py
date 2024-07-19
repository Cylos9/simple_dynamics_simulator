import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, pi
from matplotlib.patches import Circle, Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.animation as animation

class Animator:
    
    def __init__(self, param, model):
        self._param = param
        self._model = model
        self._frame_rate = param["desired_frame_rate"]
        self._figure, self._axes = plt.subplots()
            
    def run(self, states, static_path={}, dynamic_path={}, environment=None):
        
        states, extraction_ratio = self._extract_state_for_animate(states)

        for path_name, path_value in dynamic_path.items():
            dynamic_path[path_name] = path_value[:, 0::extraction_ratio]

        dynamic_artists = self._generate_dynamic_artists(states, dynamic_path)
        
        self._animate(dynamic_artists, static_path, environment)
    
    def _generate_dynamic_artists(self, states, dynamic_path):
    
        dynamic_artists = []
        
        for i in  range(states.shape[1]):
            
            if len(dynamic_path) != 0:
                pass
            
            state = states[:,i]
            
            graphic_model = self._model.graphic_model(state)

            dynamic_artists.append(self._get_patch_collection(graphic_model))

        return dynamic_artists
        
    def _animate(self, dynamic_artists, static_path, environment):
        
        # Static plot
        if len(static_path) != 0:
            for path_name, path_value in static_path.items():
                self._axes.plot(path_value[0, :], path_value[1, :], linestyle='dotted', color='grey', label=path_name)
        
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
        
        # Plot setting
        self._axes.set(xlim=[self._param["xlim_lb"], self._param["xlim_ub"]], 
                            ylim=[self._param["ylim_lb"], self._param["ylim_ub"]], 
                            xlabel='X', ylabel='Y',
                            title='Simulation in 2D space')
                
        self._axes.set_aspect("equal", adjustable="box")
        
        self._axes.legend()
        
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
        x_c, y_c, theta = graphic_object.pose
        
        x = x_c - graphic_object.width / 2 
        
        y = y_c - graphic_object.height / 2
        
        theta_in_deg = theta * 180 / pi 
        
        patch = Rectangle((x, y), graphic_object.width, graphic_object.height, 
                  angle=theta_in_deg, rotation_point='center')
         
        return self._axes.add_patch(patch)
        
    def _generate_circle_patch(self, graphic_object):

        x_c, y_c, _ = graphic_object.pose
         
        patch = Circle((x_c, y_c), radius = graphic_object.radius)
        
        return self._axes.add_patch(patch)
    
    def _extract_state_for_animate(self, states):
        
        num_states_in_second = 1/self._model._step_size
        
        if num_states_in_second < self._param["desired_frame_rate"]:
            print(f"[Warn] The frame rate was reduced from {self._param['desired_frame_rate']} to {num_states_in_second},",
                f"since the number of simulated states ({num_states_in_second}) within a second is lower than required frames ({self._param['desired_frame_rate']})")
            
            extraction_ratio = 1
            
            self._frame_rate =  1/self._model._step_size

        else:
            extraction_ratio = int(num_states_in_second / self._param["desired_frame_rate"])
            
            self._frame_rate = 1 / (self._model._step_size * extraction_ratio)
        
        states = states[:, 0::extraction_ratio]
        
        return states, extraction_ratio