import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation
from matplotlib.patches import Circle, Polygon


# def update(frame):
    
#     global vertices
    
#     vertices += 0.1
    
#     polygon.set_xy(vertices)
    
#     return (polygon)  


# if __name__ == "__main__":
    
#     fig, ax = plt.subplots()
    
#     graphic_model = []
    
        
#     vertices = np.array([[0., 0.], [0., 2.] , [2., 2.], [2., 0.]])

#     t = np.linspace(0, 10, 100)

#     # graphic_model.append(Polygon(vertices, facecolor=(0.,0.,1.)))

#     polygon = Polygon(vertices, facecolor=(0.,0.,1.))
    
#     ax.add_patch(polygon)
    
#     ax.set(xlim=[-2, 20], ylim=[-2, 20], xlabel='X', ylabel='Y')

#     anim = animation.FuncAnimation(fig=fig, func=update, frames=100, interval=0.1)

# plt.show()

class Animator:
    
    def __init__(self, model):
        self._model = model
        
        self._figure, self._axes = plt.subplots()
        
    def run(self, states):
        for i in  range(states.shape[1]):
            state = states[:,i]
            graphic_model = self._model.graphic_model(state)
        
        for graphic_object in graphic_model:
            print(graphic_object.pose)

    # def convert_
        