import fnmatch
import os
import pickle
import tensorflow as tf
from nn import *
from Games.Games import Game
from Games.TicTacToe import *
from Games.ConnectFour import *
from nn import NN

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def find(pattern, path):
    """
    args:
        pattern (string)
        path (string)

    returns a list of all the files in the directory of a specified name
    """
    result = []
    for file in os.listdir(path):
        if fnmatch.fnmatch(file, pattern):
            result.append(file)
    return result


def load_data_for_training(game):
    """
    args:
        game (Games)
    returns 
        X (matrix) board, input for the neural network
        P (matrix) vector of values from MCTS child nodes
        V (matrix) final outcome of each game
    """

    mypath = 'saved'
    # list of files
    files = find(game.name + '*', mypath)

    # where input (board state) will be saved
    X = np.empty((0, game.num_layers, game.num_rows, game.num_cols))
    V = np.empty((0, 1))  # where the value (one of labels) will be saved
    # where the policy (one of the labels) will be saved
    P = np.empty((0, len(game.action_space)))

    for file in files:
        print(file)
        try:
            data = pickle.load(open(mypath+'\\'+file, "rb")
                               )  # load the data from file
        except:
            print("Data not found in ", file)
            continue

        X_file = np.empty((0, game.num_layers, game.num_rows, game.num_cols))
        V_file = np.empty((0, 1))
        P_file = np.empty((0, len(game.action_space)))
        for episode in data:
            X_episode = np.empty(
                (len(episode), game.num_layers, game.num_rows, game.num_cols))
            V_episode = np.empty((len(episode), 1))
            P_episode = np.empty((len(episode), len(game.action_space)))
            for i in range(len(episode)):
                game.board = episode[i][0]
                # the board is converted to its one-hot representation
                X_episode[i] = game.layers()
                P_episode[i] = episode[i][1]
                V_episode[i] = episode[i][2]

            X_file = np.append(X_file, X_episode, axis=0)
            V_file = np.append(V_file, V_episode, axis=0)
            P_file = np.append(P_file, P_episode, axis=0)

        X = np.append(X, X_file, axis=0)
        V = np.append(V, V_file, axis=0)
        P = np.append(P, P_file, axis=0)
        print("Correctly loaded: ", file)

    print("Episodes in data_set:", len(V))
    return [X, V, P]


def training_nn(game, nnet, model_path):
    """
    Args:
        game: a Game object
        nnet: a NN object
    """
    X, V, P = load_data_for_training(game)
    assert len(X) == len(V)
    perm = np.random.permutation(len(X))
    X = X[perm]
    V = V[perm]
    P = P[perm]

    nnet.fit(X, V, P, 100, 1000, model_path)


class NetTrainer():
    """
    manages the two neural networks (older and newest)
    """

    def __init__(self, game, residual_layers=5):
        """
        Args:
            game: A Game object
            residual_layers(int): number of residual layers. Default is 5
        """
        self.game = game
        input_shape = game.layers().shape
        policy_shape = len(game.action_space)

        self.nnet = NN(input_shape, residual_layers, policy_shape, True)
        self.path_1 = 'model/checkpoint/old/'
        self.path_2 = 'model/checkpoint/new/'

    def train(self, name):
        """
        Args:
            name(string): 'new' or 'old'

        trains a specified neural network
        """
        if name == 'old':
            training_nn(self.game, self.nnet, self.path_1)
        elif name == 'new':
            training_nn(self.game, self.nnet, self.path_2)
        else:
            print("invalid name.")

    def prepare(self, name):
        """
        load a specified model which was previously saved
        """
        if name == 'old':
            self.nnet.pre_run(self.path_1)
        elif name == 'new':
            self.nnet.pre_run(self.path_2)
        else:
            print("invalid name.")

    def pred(self, new_input):
        """
        Args:
            new_input: a layers representation

        returns the predtion generated by the neural network
        """
        return self.nnet.pred(new_input)


if __name__ == "__main__":
    game = TicTacToe()
    Trainer = NetTrainer(game)
    Trainer.train('old')
    Trainer.train('new')
