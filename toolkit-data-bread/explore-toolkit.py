
import re
import time
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model, preprocessing
import matplotlib
import matplotlib.pyplot as plt
#%matplotlib inline
#matplotlib.use('Qt5Agg')     #  use this to make plots NOT in-line



def lm(dataframe, model, plot = False):

    lin_model = linear_model.LinearRegression()
    model=model.split('~')
    
    y_variable = model[0].strip()
    x_variables = model[1]
    x_variables = [x.strip() for x in x_variables.split('+')]

    X = dataframe[x_variables]
    Y = dataframe[y_variable]

    lin_model.fit(X, Y)
    lin_slope = lin_model.coef_
    lin_intercept = lin_model.intercept_

    Z = lin_model.predict(X)
    
    clean_eq = f"{y_variable} = {lin_model.intercept_.round(decimals=3)}"

    for idx, x in enumerate(x_variables):  
        clean_eq = str(clean_eq) + f" + {lin_model.coef_[idx].round(decimals=2)}*{x_variables[idx]}"

    if len(x_variables) > 2:
        print('4D+ not plottable')

    elif len(x_variables) == 2:
     
        fig1 = plt.figure(figsize=(5,5))
        ax = fig1.add_subplot(111, projection='3d')
        ax.scatter3D(X.iloc[:,0], X.iloc[:,1], Y)
        ax.set_xlabel(x_variables[0], fontweight ='bold') 
        ax.set_ylabel(x_variables[1], fontweight ='bold') 
        ax.set_zlabel(y_variable, fontweight ='bold', rotation=90)
        ax.zaxis.labelpad=-0.5
    
        x_plane, y_plane = np.meshgrid([X.iloc[:,0].min(), X.iloc[:,0].max()], [X.iloc[:,1].min(), X.iloc[:,1].max()])
        z_plane = lin_slope[0] * x_plane + lin_slope[1] * y_plane + lin_intercept
        ax.plot_surface(x_plane, y_plane, z_plane, alpha=0.7, color='grey')
        ax.set_title(clean_eq)
        
    else:

        fig1 = plt.figure()
        plt.scatter(X.iloc[:,0], Y, color="black")
        plt.plot(X, lin_intercept+lin_slope*X, c='red')  # plot equation of line
        plt.xlabel(x_variables[0])
        plt.ylabel(y_variable)
        plt.title(clean_eq)

    print(clean_eq)

    
    if plot==False:
        plt.close()

