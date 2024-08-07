#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: main.py

Description:
    This script demonstrates how to use the tractor-trailer model to simulate the motion of a tractor-trailer system.

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
import yaml
import csv
import numpy as np

PACKAGE_PATH = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(os.path.abspath(PACKAGE_PATH))

from models.tractor_trailer_model import TractorTrailerModel
from simple_dynamics_simulator.simulator import Simulator
from simple_dynamics_simulator.graphic.animator import Animator

def load_params(file_name, config_path=None):
    
    if config_path == None: 
        config_path = os.path.join(PACKAGE_PATH, "config")
    
    with open(os.path.join( config_path, file_name), "r") as file:
        params = yaml.safe_load(file)
    
    common_params = params["common_params"]
        
    model_params = params["model_params"]

    animator_params = params["animator_params"]
    
    print("Successfully loaded parameters")
    
    return common_params, model_params, animator_params

def read_csv(file_path):

    with open(file_path, newline='') as csvfile:
            
        csvreader = csv.reader(csvfile)
        
        headers = next(csvreader)
        
        data = {header: [] for header in headers}
        
        for row in csvreader:
            
            for header, value in zip(headers, row):
                
                data[header].append(float(value))
    
    return data

def write_csv(data, file_path):
    
    headers = data.keys()
    
    rows = zip(*output_data.values())
    
    with open(file_path, 'w', newline='') as csvfile:
        
        csvwriter = csv.writer(csvfile)
        
        csvwriter.writerow(headers)
        
        csvwriter.writerows(rows)

def load_reference_path(common_params):
    
    reference_path_data = read_csv(os.path.join(PACKAGE_PATH, common_params["data_folder"], common_params["reference_path_filename"]))
    
    reference_path = np.zeros((len(common_params["reference_path_names"]), len(reference_path_data[common_params["reference_path_names"][0]])))

    for i, state_name in enumerate(common_params["reference_path_names"]):
        reference_path[i] = np.array(reference_path_data[state_name])
    
    print("Successfully loaded reference path")

    return reference_path

def load_system_input(common_params):
    system_input_data = read_csv(os.path.join(PACKAGE_PATH, common_params["data_folder"], common_params["system_input_filename"]))
    
    system_input = np.zeros((len(common_params["system_input_names"]), len(system_input_data[common_params["system_input_names"][0]])))

    for i, input_name in enumerate(common_params["system_input_names"]):
        system_input[i] = np.array(system_input_data[input_name])
    
    print("Successfully loaded system input")
        
    return system_input

def compute_tractor_state(states):
    tractor_state = np.zeros((3, states.shape[1]))
    
    for  index in range(states.shape[1]):
        tractor_state[:, index] =  model._compute_tractor_pose(states[:, index])
    
    return tractor_state

if __name__ == "__main__":
    # Read params and data
    common_params, model_params, animator_params = load_params("params.yaml")
    
    reference_path = load_reference_path(common_params)
    
    control_input = load_system_input(common_params)
    
    # Initialize
    model = TractorTrailerModel(model_params)

    simulator = Simulator(model)
    
    animator = Animator(animator_params, model)
    
    # Simulation
    intial_state = np.array(common_params["initial_state"])
    
    time_axis, states, _ = simulator.run(intial_state, control_input)
    
    # Animation
    static_paths = {"Reference path": reference_path}
    
    tractor_state = compute_tractor_state(states)
    
    dynamic_paths = {"Trailer trajectory": np.array([states[0], states[1]]),
                    "Tractor trajectory": np.array([tractor_state[0], tractor_state[1]]),
                    }
    
    animator.run(
        states,
        static_paths=static_paths,
        dynamic_paths=dynamic_paths,
        environment=None
        )
    
    # Export data
    output_data = {
        "t": time_axis,
        "x1": tractor_state[0],
        "y1": tractor_state[1],
        "theta1": tractor_state[2],
        "x2": states[0],
        "y2": states[1],
        "theta2": states[2],
        "gamma": states[3],
        "v": control_input[0],
        "w": control_input[1],
        "x_ref": reference_path[0],
        "y_ref": reference_path[1],
    }
    
    file_path = os.path.join(PACKAGE_PATH, common_params["data_folder"], common_params["output_filename"])
    
    write_csv(output_data, file_path)