# AlphaZero
ECS 171 Machine Learning project

## Setup

Everyone should have installed

    pip install tensorflow
    pip install numpy
    pip install autopep8

If you have a Nvidia gpu, you should try to install the gpu version of tensorflow

    pip install tensorflow-gpu
and all the related requirements, such as Cuda and CuDnn.

## Submission

Before submitting a file, format the file by running

    autopep8 --in-place filename.py
## Monte Carlo Tree Search
The class MCT should be able to do the following
1. save the current node
2. from the current node, select the best action
3. update a node
4. save the Monte Carlo tree
5. load the Monte Carlo tree
6. be game-agnostic, so it gets the information from a generic Game object

## Game implementation
There are currently two games available
1. TicTacToe()
2. ConnectFour()

The following methods need to be implemented for each game:

    restart()
    is_valid(action)
        # returns a boolean
    invert_board()
    step(action)
        # returns reward
    render()
The games should also have variables such as

    action_space
    observation_space
    num_rows
    num_cols
    num_layers
