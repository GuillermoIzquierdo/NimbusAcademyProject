import streamlit as st
import pandas as pd
import numpy as np

from sklearn.datasets import load_iris d


X, Y = load_iris(return_X_y=True)

iris = pd.DataFrame(data=X, columns=["sepal length", "sepal width", "petal length", "petal width"])

iris["species"] = Y
iris["species"] = pd.cut(iris["species"], bins=3, labels=range(3))


import streamlit as st


st.header("Exploring the Iris dataset")


col_1, col_2, col_3 = st.columns(3)

with col_1:
    selectbox_value = st.selectbox("X variable",sepal length,sepal width,petal length,petal width)


with col_2:
    selectbox_value = st.selectbox("Y variable", )

with col_2:
    selectbox_value = st.selectbox("Color variable", )

st.divider()

st.write(f"Using {selectbox_value} anf value {slider_value}!")

if button:
    st.write("When you press the button, things happen!")
