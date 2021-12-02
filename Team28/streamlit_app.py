import streamlit as st
import clustering as cl
from chatbot import ChatBot as cb


with st.expander("Generate WordClouds using KMeans Clustering"):
    st.header("Generate WordClouds using KMeans Clustering")
    cl.clustering_main()

with st.expander("Chatbot"):
    st.header("How can I help you?")
    bot_obj = cb()
    
    bot_obj.chatbot_main()


