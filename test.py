import streamlit as st
import pandas as pd
import numpy as np

from sklearn.datasets import load_iris


X, Y = load_iris(return_X_y=True)

iris = pd.DataFrame(data=X, columns=["sepal length", "sepal width", "petal length", "petal width"])

import streamlit as st


st.header("Example app")

st.markdown(
    """
    This is a text example showing how you can use **markdown** in order to format
    the *text* in your streamlit application.

    You can use all sorts of things

    - in order
    - to avoid
    - actual Front-end development
    """
)

col_1, col_2 = st.columns(2)


with col_1:
    slider_value = st.slider("Select a value", 0, 10, 4, 1)



with col_2:
    selectbox_value = st.selectbox("Select an option", ("option 1", "option 2", "option 3",))

button = st.button("This is a button!")

st.divider()

st.write(f"Using {selectbox_value} anf value {slider_value}!")

if button:
    st.write("When you press the button, things happen!")
