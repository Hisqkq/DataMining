import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr
from sklearn.metrics import jaccard_score


def similarity(X, Y, method):
    '''
    SIMILARITY Computes similarity matrices

    Usage:
        sim = similarity(X, Y, method)

    Input:
    X   n(n, ), (n, 1), or (1, n) vector
    Y   n(n, ), (n, 1), or (1, n) vector
    method   string defining one of the following similarity measure
           'SMC', 'smc'             : Simple Matching Coefficient
           'Jaccard', 'jac'         : Jaccard coefficient 
           'ExtendedJaccard', 'ext' : The Extended Jaccard coefficient
           'Cosine', 'cos'          : Cosine Similarity
           'Correlation', 'cor'     : Correlation coefficient

    Output:
    sim Estimated similarity matrix between X and Y
        If input is not binary, SMC and Jaccard will make each
        attribute binary according to x>median(x)

    Copyright, Morten Morup and Mikkel N. Schmidt
    Rewritten entirely in 2021 by Roel Bouman (Radboud University)
    Technical University of Denmark '''
    X, Y = X.squeeze(), Y.squeeze()
    n = X.shape[0]
    n2 = X.shape[0]
    
    if not n == n2:
        raise ValueError("X and Y are not the same size")
    
    method = method[:3].lower()
    if method=='smc': # SMC
        if not np.sum(X==0) + np.sum(X==1) == len(X):
            X = binarize(X)
        if not np.sum(Y==0) + np.sum(Y==1) == len(Y):
            Y = binarize(Y)
        sim = np.mean(X==Y)
    elif method=='jac': # Jaccard
        if not np.sum(X==0) + np.sum(X==1) == len(X):
            X = binarize(X)
        if not np.sum(Y==0) + np.sum(Y==1) == len(Y):
            Y = binarize(Y)
        sim = jaccard_score(X,Y)
    elif method=='ext': # Extended Jaccard
        XYt = X.dot(Y)
        sim = XYt / (np.linalg.norm(X)**2 + np.linalg.norm(Y)**2 - XYt)
    elif method=='cos': # Cosine
        sim = cosine_similarity(X.reshape(1, -1),Y.reshape(1, -1))[0][0]
    elif method=='cor': # Correlation
        sim = pearsonr(X,Y)[0]
    return sim
    
def binarize(X):
    med_X = np.median(X)
    return (X > med_X).astype(np.float64)