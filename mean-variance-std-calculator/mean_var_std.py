import numpy as np

def calculate(l: list):
    if (len(l) != 9):
        raise ValueError('List must contain nine numbers.')
    flattened = np.array(l)
    axis2 = np.array([l[i:i+3] for i in range(0,9,3)])
    axis1 = axis2.T

    stats = lambda f: [*[[f(l) for l in d] for d in [axis1, axis2]], f(flattened)]

    calculations = {
        'mean': stats(np.mean),
        'variance': stats(np.var),
        'standard deviation': stats(np.std),
        'max': stats(np.max),
        'min': stats(np.min),
        'sum': stats(np.sum)
    }

    return calculations