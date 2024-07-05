# exercise 1.3.1

import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy.spatial.distance import cdist

import numpy as np


from toolbox.similarity import similarity

def simfaces(i=1, similarity_measure = 'smc'):
    # i is the Image to use as query

    # Similarity: 'SMC', 'Jaccard', 'ExtendedJaccard', 'Cosine', 'Correlation' 


    # Load the CBCL face database
    # Load Matlab data file to python dict structure and get X
    X = loadmat("./data/wildfaces_grayscale.mat")['X']
    n, _ = X.shape


    # Search the face database for similar faces
    # Index of all other images than i
    not_i = list(range(0,i)) + list(range(i+1,n)) 
    # Compute similarity between image i and all others
    sim_function = lambda X1, X2 : similarity(X1,X2,similarity_measure)

    sim = cdist(X[i,:, np.newaxis].T, X[not_i,:], sim_function).squeeze()

    
    ordering_index = np.argsort(sim) #reverse ordering


    # Visualize query image and 5 most/least similar images
    plt.figure(figsize=(12,8))
    plt.subplot(3,1,1)
    plt.imshow(np.reshape(X[i],(40,40)).T, cmap=plt.cm.gray)
    plt.xticks([]); plt.yticks([])
    plt.title('Query image')
    plt.ylabel('image #{0}'.format(i))


    for ms in range(5):

        # 5 most similar images found
        plt.subplot(3,5,6+ms)
        im_id = ordering_index[-(ms+1)]
        im_sim = sim[im_id]
        plt.imshow(np.reshape(X[im_id],(40,40)).T, cmap=plt.cm.gray)
        plt.xlabel('sim={0:.3f}'.format(im_sim))
        plt.ylabel('image #{0}'.format(im_id))
        plt.xticks([]); plt.yticks([])
        if ms==2: plt.title('Most similar images')

        # 5 least similar images found
        plt.subplot(3,5,11+ms)
        im_id = ordering_index[ms]
        im_sim = sim[im_id]
        plt.imshow(np.reshape(X[im_id],(40,40)).T, cmap=plt.cm.gray)
        plt.xlabel('sim={0:.3f}'.format(im_sim))
        plt.ylabel('image #{0}'.format(im_id))
        plt.xticks([]); plt.yticks([])
        if ms==2: plt.title('Least similar images')
        
    plt.show()
