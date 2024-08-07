#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: simulator.py

Description:
    This script defines the Simulator class, which is used to simulate the dynamics of a system using a dynamical model.

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


class Simulator:
    
    def __init__(self, model):
        
        self._model = model
        
        self._result = None
        
    def run(self, intial_state, inputs):

        intial_state = np.asarray(intial_state)
        
        intial_state.reshape(self._model._nx, 1)
        
        if inputs.shape[0] != self._model._nu:
            
            inputs.tranpose()
        
        steps = inputs.shape[1]
        
        states = np.zeros((self._model._nx, steps + 1))
        
        states[:, 0] = intial_state
        
        time_axis = np.linspace(0, steps * self._model._step_size, num=steps+1)
        
        for i in range(steps):
            states[:, i+1] = self._model.step(states[:, i], 
                                               inputs[:, i])
            
        inputs = np.hstack((inputs, np.zeros((self._model._nu, 1))))
        
        self._result = np.vstack((time_axis, states, inputs))
        
        return time_axis, states, inputs