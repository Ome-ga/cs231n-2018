import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  scores = np.dot(X, W)
  num_train = X.shape[0]
  num_class = W.shape[1]
  for i in range(num_train):
    loss -= scores[i, y[i]]
    sum_score = np.sum((np.exp(scores[i])))
    loss += np.log(sum_score)
    dW[:, y[i]] -= X[i]
    for j in range(num_class):
      dW[:, j] += X[i] * np.exp(scores[i, j]) / sum_score

  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################
  loss /= num_train
  dW /= num_train
  loss += reg * np.sum(W * W)
  dW += 2 * reg * W
  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train, dim = X.shape
  dim, num_class = W.shape
  scores = np.dot(X, W)
  max_scores = np.max(scores, axis=1, keepdims=True)
  scores -= max_scores
  exp_scores = np.exp(scores)
  sum_rows = np.sum(exp_scores, axis=1, keepdims=True)
  exp_scores_reg = exp_scores / sum_rows
  true_class = np.zeros((num_train, num_class))
  true_class[range(num_train), y] = 1
  w_true_class = np.dot(true_class, W.T) # N by D
  loss -= np.trace(np.dot(scores, true_class.T))
  loss += np.sum(np.log(np.sum(exp_scores, axis=1, keepdims=True)))
  loss /= num_train
  loss += reg * np.sum(np.multiply(W, W))
  dW += np.dot(X.T, exp_scores_reg - true_class) / num_train
  dW += 2 * reg * W

  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

