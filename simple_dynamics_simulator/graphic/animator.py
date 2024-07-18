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
        self._figure, self._axes = plt.subplots()
            
    def run(self, states):
        
        artists = []
        
        for i in  range(states.shape[1]):
            
            state = states[:,i]
            
            graphic_model = self._model.graphic_model(state)

            artists.append(self._get_patch_collection(graphic_model))
        
        self._axes.set(xlim=[self._param["xlim_lb"], self._param["xlim_ub"]], 
                       ylim=[self._param["ylim_lb"], self._param["ylim_ub"]], 
                       xlabel='X', ylabel='Y')
        
        self._axes.set_aspect("equal",adjustable="box")
        
        anim = animation.ArtistAnimation(fig=self._figure, 
                                         artists=artists, 
                                         interval=self._param["interval_time"], 
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