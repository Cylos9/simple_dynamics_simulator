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
import yaml
import csv
import numpy as np

package_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(os.path.abspath(package_path))

from models.tractor_trailer_model import TractorTrailerModel
from simple_dynamics_simulator.simulator import Simulator
from simple_dynamics_simulator.graphic.animator import Animator

def get_params(file_name, config_path=None):
    
    if config_path == None: 
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

def write_csv(data, file_path):
    
    headers = data.keys()
    
    rows = zip(*output_data.values())
    
    with open(file_path, 'w', newline='') as csvfile:
        
        csvwriter = csv.writer(csvfile)
        
        csvwriter.writerow(headers)
        
        csvwriter.writerows(rows)

if __name__ == "__main__":
    
    params = get_params("params.yaml")
    
    common_params = params["common_params"]
    
    # Data table is expeted to have "v" and "w" column header, represents for the control input
    control_input_data = read_csv(os.path.join(package_path, "data", common_params["system_input_filename"]))
    
    reference_path_data = read_csv(os.path.join(package_path, "data", common_params["reference_path_filename"]))
    
    model = TractorTrailerModel(params["model_params"])

    simulator = Simulator(model)
    
    animator = Animator(params["animator_params"], model)
    
    intial_state = np.array(common_params["initial_state"])
    
    inputs =  np.vstack((np.array(control_input_data["v"]), np.array(control_input_data["w"])))
    
    time_axis, states, _ = simulator.run(intial_state, inputs)
    
    animator.run(
        states,
        reference_path= np.array([reference_path_data["x_ref"], reference_path_data["y_ref"]]),
        environment=None
        )
    
    output_data = {
        "t": time_axis.tolist(),
        "v": control_input_data["v"],
        "w": control_input_data["w"],
        "x2": states[0],
        "y2": states[1],
        "theta2": states[2],
        "gamma": states[3],
        "x_ref": reference_path_data["x_ref"],
        "y_ref": reference_path_data["y_ref"]
    }
    
    file_path = os.path.join(package_path, "data", common_params["output_filename"])
    
    write_csv(output_data, file_path)