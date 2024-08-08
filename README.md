
# Simple Dynamic Model Simulator

This package offers a simple framework for defining dynamic models, simulating them with control inputs using the Fourth-order Runge Kutta method, and visualizing the simulation results through graphs and animations. It is designed to be user-friendly and is ideal for educational purposes.

> An example of a tractor trailer model is provided.

![hardware configuration](images/tractor_trailer_navigation_demo.gif)

## Enviroments
This module was tested with Python 3.9.

Install dependencies

```bash
pip install -r requirements.txt

```
## How to use this modules
1. Define dynamic models uses Model as base class
2. Using Animator, Simulator with the target model to simulate and animate the dynamics.

> I have written a tractor trailer model as an example, inside `models` folder.

## Simple run with TractorTrailerModel

```bash
python ./examples/main.py
```

