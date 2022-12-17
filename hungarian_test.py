from hungarian import Hungarian
import numpy as np
from app import paint_clip
import streamlit as st

# sample visualization of Munkres

matrix = np.array([
    [2, 3, 2, 4],
    [4, 1, 5, 1],
    [1, 3, 6, 2],
    [5, 6, 7, 8]
])
hungarian = Hungarian(matrix=matrix)
hungarian.calculate()
sequence = hungarian.get_seq()
x = st.slider('x', max_value=len(sequence) - 1)  # 👈 this is a widget
paint_clip(sequence[x])
