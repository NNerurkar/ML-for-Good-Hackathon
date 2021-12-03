import pandas as pd
import numpy as np
import os
import re
import string
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
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import textract

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..', 'Data')))


class ChatBot:
    def __init__(self):
        self.conversation = ''
        self.article_sentences = []
        self.article_words = []

    def chatbot_main(self):
        #self.train_model()
        chat_area = st.empty()
        user_message = st.text_area('', value="", key=None, on_change=None, args=None )
    
        if user_message:
            self.update_conversation('You', user_message)
            self.update_conversation('Bot', self.generate_reply(user_message))
            chat_area.text(self.conversation)
            user_message = ''
        


    def update_conversation(self, username, new_message):
        self.conversation = self.conversation + username+': '+ new_message + '\n'


    def perform_lemmatization(self, tokens):
        wnlemmatizer = nltk.stem.WordNetLemmatizer()
        return [wnlemmatizer.lemmatize(token) for token in tokens]


    def get_processed_text(self, document):
        punctuation_removal = dict((ord(punctuation), None) for punctuation in string.punctuation)
        return self.perform_lemmatization(nltk.word_tokenize(document.lower().translate(punctuation_removal)))
    

    def generate_reply(self, user_input):

        focus_group_data = ''
        for (root, dirs, files) in os.walk('FocusGroups', topdown=True):
            for file in files:
                focus_group_data = focus_group_data + str(textract.process(os.path.join(root, file)))
                    
        st.write(focus_group_data)
        article_text = re.sub(r'\[[0-9]*\]', ' ', focus_group_data)
        article_text = re.sub(r'\s+', ' ', focus_group_data)

        self.article_sentences = nltk.sent_tokenize(focus_group_data)
        self.article_words = nltk.word_tokenize(focus_group_data)

        self.article_sentences.append(user_input)

        word_vectorizer = TfidfVectorizer(tokenizer=self.get_processed_text, stop_words='english')
        all_word_vectors = word_vectorizer.fit_transform(self.article_sentences)
        similar_vector_values = cosine_similarity(all_word_vectors[-1], all_word_vectors)
        similar_sentence_number = similar_vector_values.argsort()[0][-2]

        matched_vector = similar_vector_values.flatten()
        matched_vector.sort()
        vector_matched = matched_vector[-2]

        if vector_matched == 0:
            return 'Response not found'
        else:
            return article_sentences[similar_sentence_number]
            




