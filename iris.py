import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_iris

X, Y = load_iris(return_X_y=True)

iris = pd.DataFrame(data=X, columns=["sepal length", "sepal width", "petal length", "petal width"])
iris["species"] = Y
iris["species"] = pd.cut(iris["species"], bins=3, labels=range(3))

st.header("Exploring the Iris dataset")

col_1, col_2, col_3 = st.columns(3)

options = ["sepal length", "sepal width", "petal length", "petal width","species"]

# X variable selection
with col_1:
    x_value = st.selectbox("X variable",options=options)

# Y variable selection
with col_2:
    y_value = st.selectbox("Y variable",options=options)

# Color variable selection
with col_3:
    color_value = st.selectbox("Color variable",options=options)

# Create scatterplot
# Using Streamlit's built-in scatter plot visualization
chart_data = iris[[x_value, y_value, color_value]]
st.scatter_chart(chart_data, x=x_value, y=y_value, color=color_value)