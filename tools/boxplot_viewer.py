# tools/boxplot_viewer.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def run():
    st.subheader("📊 Boxplot Element Viewer")

    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()
        df[df.columns[0]] = df[df.columns[0]].astype(str).str.strip()
        df.set_index(df.columns[0], inplace=True)

        df_numeric = df.select_dtypes(include='number')

        if df_numeric.empty:
            st.error("No numeric data found in the file.")
            return

        heat_input = st.text_input("Enter Heat Number")
        element_input = st.selectbox("Select Element", df_numeric.columns)

        if heat_input in df.index:
            value = df_numeric.at[heat_input, element_input]
            fig, ax = plt.subplots(figsize=(6, 6))
            df_numeric[element_input].plot.box(ax=ax)
            ax.scatter(1, value, color='red', zorder=5, label=f"Heat {heat_input}: {value:.4f}")
            ax.set_title(f"Boxplot for {element_input}")
            ax.set_ylabel("Content (%)")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
        elif heat_input:
            st.warning("Heat number not found.")
