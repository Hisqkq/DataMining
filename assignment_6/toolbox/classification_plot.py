# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt


def classification_plot(X_test, y_test, y_test_pred, X_train = None, y_train = None):
    '''
    classification_plot plots a clustering of a data set as well as the true class
    labels. If data is more than 2-dimensional it should be first projected
    onto the first two principal components. Data objects are plotted as a dot
    with a circle around. The color of the dot indicates the true class,
    and the cicle indicates the predicted class.

    Usage:
    classification_plot(X_test, y_test, y_test_pred)
    classification_plot(X_test, y_test, y_test_pred, X_train, y_train)

    Input:
    X_test           N-by-2 test data matrix (N data objects with 2 attributes)
    y_test           N-by-1 vector of true class labels of the test data
    y_test_pred      N-by-1 vector of predicted class labels of the test data
    X_train          N-by-2 train data matrix (N data objects with 2 attributes)
    y_train          N-by-1 vector of true class labels of the train data    
    
    '''
    
    X_test = np.asarray(X_test)
    cls = np.asarray(y_test_pred)

    y_test = np.asarray(y_test)

    K = np.size(np.unique(cls))
    C = np.size(np.unique(y_test))
    
    ncolors = np.max([C, K])

    # plot data points color-coded by class, cluster markers and centroids

    colors = [0]*ncolors
    for color in range(ncolors):
        colors[color] = plt.cm.jet.__call__((color*255)//(ncolors-1))[:3]
    for i, cs in enumerate(np.unique(y_test)):
        plt.plot(X_test[(y_test == cs).ravel(), 0], X_test[(y_test == cs).ravel(), 1], 'o',
                 markeredgecolor='k', markerfacecolor=colors[i], markersize=6,
                 zorder=2, label = 'Test Class:' + str(i))
    for i, cr in enumerate(np.unique(cls)):
        plt.plot(X_test[(cls == cr).ravel(), 0], X_test[(cls == cr).ravel(), 1], 'o',
                 markersize=12, markeredgecolor=colors[i],
                 markerfacecolor='None', markeredgewidth=3, zorder=1, label = 'Test Predicted:' + str(i))

    if X_train is not None and X_test is not None:
        X_train = np.asarray(X_train)
        y_train - np.asarray(y_train).ravel()
        T = np.size(np.unique(y_train))
        
        for i, cr in enumerate(np.unique(y_train)):
            plt.plot(X_train[y_train == cr, 0].ravel(), X_train[y_train == cr, 1].ravel(), '*',
                     markersize=4, markeredgecolor=colors[i],
                     markerfacecolor='None', zorder=3, label = 'Train Class:' + str(i))

    else:
        T = 0

    # create legend
    legend_items = (np.unique(y_test).tolist() + np.unique(cls).tolist() +
                    np.unique(y_train).tolist())
    for i in range(len(legend_items)):
        if i < C:
            legend_items.append('Test Class: {0}'.format(legend_items[i]))
        elif i < C + K:
            legend_items.append('Test Predicted: {0}'.format(legend_items[i]))
        elif i < C + K + T:
            legend_items.append('Train: {0}'.format(legend_items[i]))    
    #plt.legend(legend_items, numpoints=1, markerscale=.75, prop={'size': 9}, bbox_to_anchor=(1, 0.5))
    plt.legend(numpoints=1, markerscale=.75, prop={'size': 12}, bbox_to_anchor=(1, 0.5))