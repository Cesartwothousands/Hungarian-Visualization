import streamlit as st
import numpy as np
import pandas as pd


# Some helper function to visualize Munkres algorithm

def highlight_row(data, list_covered_row):
    '''
    highlight the maximum in a Series yellow.
    '''
    output = []
    for i in range(len(data)):
        if i in list_covered_row:
            output.append("background-color: yellow")
        else:
            output.append("")
    return output


def highlight_column(data):
    return ['background-color: yellow' for v in data]


def paint_clip(clip):
    matrix = clip["matrix"]
    covered_row = clip["covered rows"]
    covered_column = clip["covered colums"]
    starred_point = clip["starred_point"]
    primed_point = clip["primed_point"]
    df = pd.DataFrame(matrix)
    list_covered_column = []
    for i in covered_column:
        list_covered_column.append(i)
    list_covered_row = []
    for i in covered_row:
        list_covered_row.append(i)
    if len(list_covered_column) == 0:
        df1 = df.style
    else:
        df1 = df.style.apply(highlight_column, subset=list_covered_column, axis=1)
    # st.dataframe(df1)
    st.dataframe(df1.apply(highlight_row, list_covered_row=list_covered_row))
    st.write("starred zeros are")
    st.write(starred_point)
    st.write("primed zeros are")
    st.write(primed_point)


matrix = np.array([
    [2, 3, 2, 4],
    [4, 1, 5, 1],
    [1, 3, 6, 2],
    [5, 6, 7, 8]
])
clip = {
    "matrix": matrix,
    "covered rows": {1},
    "covered colums": {0},
    "starred_point": [(0, 0), (1, 1)],
    "primed_point": [(0, 2)],
}
paint_clip(clip)
"""
hungarian=Hungarian(matrix=matrix)
hungarian.calculate()
sequence=hungarian.get_seq()
x = st.slider('x',max_value=len(sequence))  # 👈 this is a widget
show_clips(sequence[x])
"""
