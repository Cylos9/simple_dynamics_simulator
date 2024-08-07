#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: model.py

Description:
    This script defines the Model class, which is an abstract class that represents the dynamical model of a system. 
    The Model class provides the basic structure for implementing a dynamical model, including the dynamics function and the step function.

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

from abc import ABC, abstractmethod
import numpy as np

class Model(ABC):
    
    def __init__(self, params):
        
        super().__init__()
        
        self._nx = params["num_states"]
        
        self._nu = params["num_inputs"]
        
        self._discrete_method = params["discrete_method"]

        self._step_size = params["step_size"]
    
    @abstractmethod
    def dynamics(self, state, input):
        pass
    
    @abstractmethod
    def graphic_model(self, state):
        pass
        
    def step(self, state, input):

        state = np.asarray(state)
        
        input = np.asarray(input)
        
        if self._discrete_method == "KR1":
            
            state_dot = self.dynamics(state, input)
                
            state += self._step_size * state_dot
        
        elif self._discrete_method == "KR4":
            
            k1 = self.dynamics(state, input)
            
            k2 = self.dynamics(state + 1/2*self._step_size*k1, input)
            
            k3 = self.dynamics(state + 1/2*self._step_size*k2, input)
            
            k4 = self.dynamics(state + self._step_size*k3, input)

            state += 1/6 * self._step_size * (k1 + 2*k2 + 2*k3 + k4)
            
        else:
            raise Exception(f"The discrete method '{self._discrete_method}' has not supported")
        
        return state