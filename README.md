# IMU Pre-integrated Examples

## Pre-Reqs:

Python environment that should work (see the environment.yaml, and you can create your python environment with this yaml: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

 - gtbook
 - matplotlib
 - ipympl
 - numpy (1.21.6, make sure it is less than 2.0)
 - graphviz
 - pybind11-stubgen
 - pyparsing 
 - double check any other packages that the instructions from gtsam form the link below specify, and make sure you have your python environment activated when you try to build gtsam from source (see building from source)


Follow the instructions below. 

### Building From Source

Python 3.7 or above seemed to work. And do not skip the step to just run "make" before you run "make python-install," at least that is what worked when setting up these. You need to build gtsam from source for the FixedLagSmoother gtsam functions.
"pip install gtsam" will not have some of those functions exposed on the python side.


Go here: https://github.com/borglab/gtsam/tree/develop/python

Make sure you specifiy correct python version, etc. while runing your "cmake .." command


## File/Directory Descriptions

### lm.ipynb

Batch optimizer. Taken directly from https://gtbook.github.io/gtsam-examples/ImuFactorExample101.html.

### isam.ipynb

Adapted the lm.ipynb example to be incremental. Used this example (https://github.com/borglab/gtsam/blob/develop/python/gtsam/examples/ImuFactorISAM2Examplepy), which is included also.

### isam_imu_predict.ipynb

Main difference between this file and the isam.ipynb is the way that we are setting an initial estimate for X and V for each pose and velocity node. I am using the pre-integration to predict X and V here (dead reckoning) rather than just adding noise to the true pose and velocity.

### isam_imu_predict_with_unaries.ipynb

Same as directly above except with added unary constraints.


### fixed_lag_smoother.ipynb

This is an implementation of an incremental fixed lag smoother using pre-integrated imu factors. Based on the previous scripts. And used the python example of Batch fixed lag smoother in python from gtsam (https://github.com/borglab/gtsam/blob/develop/python/gtsam/examples/FixedLagSmootherExample.py) as well as the incremental example they have in C++ () -- using fixed lag smoother functions gtsam has recreated required building gtsam from source

### ifls_with_unary.ipynb

Incremental fixed lag smoother with added unaries. This is what we are going for. A sliding window factor graph that also adds unary constraints.

### factor_graph.sh

Just a script to launch a useful tmux configuration to test the factor graph using ros2 bags. You can "ros2 bag play" in one terminal, while another terminal sends init empty messages to the factor graph node, and you can use another termianl to go into the docker container and run the factor graph.







