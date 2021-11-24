import streamlit as st




col1, col2, col3 = st.columns(3)

with col1:
    st.header("Column1")
    st.image("https://static.streamlit.io/examples/cat.jpg")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        st.write(bytes_data)

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.write(stringio)
        # To read file as string:
        string_data = stringio.read()
        st.write(string_data)

        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)

with col2:
    st.header("Column 2")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
    st.header("Column 3")
    st.image("https://static.streamlit.io/examples/owl.jpg")

