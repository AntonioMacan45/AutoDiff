import numpy as np
import matplotlib.pyplot as plt
import data
from auto_diff import *
from computational_nodes import *
from source.model import LogisticRegression


def logreg_train(X, Y_):
    N, D = X.shape
    C = np.max(Y_) + 1
    Y = data.class_to_onehot(Y_)

    # Parameter initialization
    W = Parameter(shape=(C, D))
    W.initialize_with_random()

    b = Parameter(shape=(C, 1))
    b.initialize_with_zeros()

    x = Variable(X, name="x")
    y = Variable(Y, name="y")

    model = LogisticRegression(W, b)

    # Mode: affine transformation + softmax
    affine = AffineTransform(x, model.W, model.b, name="affine")
    scores = Softmax(affine, name="softmax")

    # Loss function: cross entropy
    loss = SoftmaxCrossEntropyWithLogits(scores, y, name="loss")

    model.train(X, Y_, loss, verbose=True, param_delta=0.1, param_niter=50000)

    return model


def logreg_decfun(model: LogisticRegression):
    def classify(X):
        return np.argmax(model.classify(X), axis=1)

    return classify


if __name__ == "__main__":
    np.random.seed(100)

    # get the training dataset
    X, Y_ = data.sample_gauss_2d(3, 100)

    model = logreg_train(X, Y_)

    # evaluate the model on the training dataset
    probs = model.classify(X)
    Y = np.argmax(probs, axis=1)

    # report performance
    accuracy, recall, precision = data.eval_perf_multi(Y, Y_)
    # AP = data.eval_AP(Y_[np.max(probs, axis=1).argsort()])
    # print(accuracy, recall, precision, AP)
    print(accuracy, recall, precision, sep='\n')
    # breakpoint()

    # graph the decision surface
    decfun = logreg_decfun(model)
    bbox = (np.min(X, axis=0), np.max(X, axis=0))
    data.graph_surface(decfun, bbox, offset=0.5)

    # graph the data points
    data.graph_data(X, Y_, Y, special=[])

    # show the plot
    plt.show()
