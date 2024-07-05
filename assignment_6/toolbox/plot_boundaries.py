# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 10:05:21 2018

@author: Roel bouman, Lisa Tostrams

Simple decision boundary plotter for scikit-learn Classifiers

from toolbox.plot_boundaries import plot_boundaries

clf = sklearn.___.(...)
clf.fit(X,y)

plot_boundaries((X,y,clf))

"""

import numpy as np
import matplotlib.pyplot as plt

        
def plot_boundaries(X,y,model):
	y_hat = model.predict(X)
	x0 = np.arange(min(X[:,0])-0.5, max(X[:,0])+0.5, 0.01)
	x1 = np.arange(min(X[:,1])-0.5, max(X[:,1])+0.5, 0.01)
	xx, yy = np.meshgrid(x0, x1, sparse=False)
	space = np.asarray([xx.flatten(),yy.flatten()]).T
	z = model.predict(space)

	plt.scatter(X[(y_hat==1),0],X[(y_hat==1),1],label='Predicted 1', c="r", marker="o", s=50)
	plt.scatter(X[(y_hat==0),0],X[(y_hat==0),1],label='Predicted 0', c="b", marker="o", s=50)
	plt.scatter(X[(y==1),0],X[(y==1),1],label='True 1', c="r", marker=".", s=70, zorder=3)
	plt.scatter(X[(y==0),0],X[(y==0),1],label='True 0', c="b", marker=".", s=70, zorder=3)
	h = plt.contourf(x0,x1,np.reshape(z,[len(x1),len(x0)]), levels=[0,0.5,1],colors=('b','r'),alpha=0.1)
	plt.legend(numpoints=1, markerscale=.75, prop={'size': 12}, bbox_to_anchor=(1, 0.5))
