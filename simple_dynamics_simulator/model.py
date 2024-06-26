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

from abc import ABC, abstractmethod

class Model(ABC):
    
    def __init__(self, model_params, discrete_method, step_size):
        
        super().__init__()
        
        self._model_params = model_params
        
        self._discrete_method = discrete_method

        self._step_size = step_size
    
    @abstractmethod
    def dynamics(self, state, input):
        pass
    
    @abstractmethod
    def graphic_model(self, state):
        pass
        
    def step(self, state, input):
            
        state_dot = self.dynamics(state, input)

        if self._discrete_method == "KR1":
            
            for i in range(len(state)):
                
                state[i] += self._step_size * state_dot[i]
        
        elif self._discrete_method == "KR4":
            
            pass
        
        return state