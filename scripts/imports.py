# make the images consistent in Jupyter
from IPython.display import Image
def slide( what ):
    display( Image( "../images/" + what + "", width = 50, height = 50, retina = True ) )

import os
import pandas as pd
# pd.set_option( 'display.max_columns', 8 )
pd.options.mode.chained_assignment = None
from IPython.display import display_html 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import math
import sidetable
from pandas.api.types import CategoricalDtype
# pip install simple-colors
import simple_colors as sc
from sklearn import preprocessing as pp
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import statsmodels.formula.api as smf 
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import r2_score
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.tree import export_graphviz

##!{sys.executable} -m pip install graphviz

## conda install -c anaconda graphviz python-graphviz pydotplus
## Tell Python where the graphviz package is loaded; then load it.
##os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
##from sklearn.externals.six import StringIO 
from io import StringIO
import pydotplus
import graphviz

from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import dendrogram, linkage
import scipy.cluster.hierarchy as shc
from scipy.cluster.hierarchy import fcluster
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture 
from IPython.display import Image
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
import lifetimes

from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions

# sqlalchemy stuff
import pyodbc
from sqlalchemy import create_engine
import urllib

print("done running imports.py")