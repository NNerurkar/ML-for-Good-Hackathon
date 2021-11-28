import pandas as pd
import numpy as np
import os
import pandas_profiling as pp
import streamlit as st
from streamlit_pandas_profiling import st_profile_report
from sklearn.cluster import KMeans
import pickle
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates
from sklearn.preprocessing import StandardScaler
import nltk
import sys
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score


def clustering_main():
    uploaded_file = st.file_uploader("Choose a file", key='1234')
    number = int(st.number_input('Number of clusters', format='%d'))
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        #dataframe = pd.read_csv(uploaded_file)
        crisis_data = pd.read_csv(uploaded_file, low_memory=False) 
    res = st.button('Generate clusters')
    if res:
        get_cluster_word_cloud(_dataframe=crisis_data, _clusters=number) 


def get_cluster_word_cloud(_dataframe, _clusters=5):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(_dataframe["transcriptions"])

    
    model = KMeans(n_clusters=_clusters, init='k-means++', max_iter=1000, n_init=1)
    model.fit(X)


    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()

    for i in range(_clusters):
        print("Cluster %d:" % i)
        mystr = ""
        for ind in order_centroids[i, :30]:
            mystr = mystr+ ' ' +terms[ind]
        #print(' %s' % terms[ind]),
        wordcloud = WordCloud().generate(mystr)
        print(wordcloud)
        
    # Display the generated image:
        st.set_option('deprecation.showPyplotGlobalUse', False)
        plt.imshow(wordcloud, interpolation='bilinear')
        
        plt.axis("off")
        plt.show()
        st.pyplot()


