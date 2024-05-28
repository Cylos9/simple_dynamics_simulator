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
import yaml
import csv
import numpy as np

from model.tractor_trailer_model import TractorTrailerModel
from simulator.simulator import Simulator
from graphic.animator import Animator

def get_params(file_name, config_path=None):
    
    if config_path == None: 
        
        package_path = str(Path(__file__).resolve().parent.parent)
        
        config_path = os.path.join(package_path, "config")
    
    with open(os.path.join( config_path, file_name), "r") as file:
        params = yaml.safe_load(file)
        
    return params

def read_csv(file_path):

    with open(file_path, newline='') as csvfile:
            
        csvreader = csv.reader(csvfile)
        
        headers = next(csvreader)
        
        data = {header: [] for header in headers}
        
        for row in csvreader:
            
            for header, value in zip(headers, row):
                
                data[header].append(float(value))
    
    return data

if __name__ == "__main__":
    
    params = get_params("params.yaml")
    
    data = read_csv("/home/cylos/tutlab/dynamics_simulator/data/system_input.csv")
    
    step_size = 0.2
    
    model = TractorTrailerModel(params, 'KR1', step_size)
    
    simulator = Simulator(model)
    
    animator = Animator(model)
    
    intial_state = np.array([0., 0., 0., 0.])
    
    inputs =  np.vstack((np.array(data["v"]), np.array(data["w"])))
    
    time_axis, states, _ = simulator.run(intial_state, inputs)
    
    animator.run(states)