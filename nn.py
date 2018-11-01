# python 3.5

import tensorflow as tf
import numpy as np

class NN():
	""" 
	Args:
		lr (float): learning rate
		board_dim (int np_arr of size 2): length and width of board
		input_layers (int): number of input layers
		hidden_layers (int): number of hidden residual layers
	
	"""
	def __init__(self, lr, board_dim, input_layers, hidden_layers):
		self.lr = lr
		self.board_dim = board_dim
		self.input_layers = input_layers
		self.hidden_layers = hidden_layers

	def batch_norm(inputs, training, BATCH_MOMENTUM = 0.997, BATCH_EPSILON = 1e-5):
		return tf.layers.batch_normalization(
			inputs=inputs, axis=-1, momentum=_BATCH_NORM_DECAY, 
			epsilon=_BATCH_NORM_EPSILON, center=True, 
			scale=True, training=training, fused=True)

	def conv2d():
		# WILL DO NEXT
		return None

	def resBlock(inputs, filter, kernelsize, training, strides=1, padding="same"):
		"""
		Args:
			inputs (tensor): Tensor input
			filter (int): Number of channels in the output
			kernelsize (int,tuple): Size of convolution window
			strides (int): Stride of convolution
			padding (int): "valid" or "same"
			training (bool): True if training
		"""
		shortcut = tf.identity(input)
		conv1 = tf.layers.Conv2D(
			inputs = inputs,
			filters = filter, 
			kernel_size = kernelsize, 
			strides = strides, 
			padding = padding, 
			activation = None
		)
		conv1_bn = batch_norm(conv1, training)
		conv1_bn_relu = tf.nn.relu(conv1_bn)
		conv2 = tf.layers.Conv2D(
			inputs = conv1_bn_relu,
			filters = filter, 
			kernel_size = kernelsize, 
			strides = strides, 
			padding = padding, 
			activation = None
		)
		conv2_bn = batch_norm(conv2, training)
		y = conv2_bn + shortcut
		y_relu = tf.nn.relu(y)
		return y