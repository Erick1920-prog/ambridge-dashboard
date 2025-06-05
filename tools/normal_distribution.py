import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def run():  # ✅ This must be defined at the top level
    st.subheader("Normal Distribution Curve Viewer")

    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])
    if uploaded_file:
        sheet_names = pd.ExcelFile(uploaded_file).sheet_names
        sheet = st.selectbox("Select a sheet", sheet_names)
        df = pd.read_excel(uploaded_file, sheet_name=sheet)
        df.columns = df.columns.str.strip()
        column = st.selectbox("Select a column", df.columns)
        data = df[column].dropna()

        mean, std = data.mean(), data.std()
        min_val, max_val = data.min(), data.max()
        counts, bin_edges = np.histogram(data, bins='auto')
        bin_width = bin_edges[1] - bin_edges[0]
        x = np.linspace(mean - 4 * std, mean + 4 * std, 400)
        pdf = norm.pdf(x, mean, std) * len(data) * bin_width

        add_limits = st.checkbox("Add Min/Max OD Limits")
        if add_limits:
            min_limit = st.number_input("Enter Min OD limit", value=float(min_val))
            max_limit = st.number_input("Enter Max OD limit", value=float(max_val))

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(data, bins=bin_edges, alpha=0.6, color='green', edgecolor='black', label='Data Histogram')
        ax.plot(x, pdf, 'r-', linewidth=2, label='Normal Fit')

        if add_limits:
            ax.axvline(min_limit, color='black', linestyle='--', linewidth=1.5, label=f'Min Limit = {min_limit}')
            ax.axvline(max_limit, color='black', linestyle='--', linewidth=1.5, label=f'Max Limit = {max_limit}')
            ax.axvspan(min_val, min_limit, color='gray', alpha=0.15)
            ax.axvspan(max_limit, max_val, color='gray', alpha=0.15)

        ax.set_title(f"Histogram & Bell Curve for \"{column}\"")
        ax.set_xlabel("Value")
        ax.set_ylabel("Count")
        ax.grid(True, linestyle=':')
        ax.legend(loc='upper left')
        st.pyplot(fig)

        st.subheader("Summary Statistics")
        st.table(pd.DataFrame({
            "Metric": ["Mean", "Min", "Max", "Std Dev"],
            "Value": [f"{mean:.4f}", f"{min_val:.4f}", f"{max_val:.4f}", f"{std:.4f}"]
        }))