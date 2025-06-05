import streamlit as st
from tools import normal_distribution, boxplot_viewer, heat_comparison
import tools.normal_distribution
print("Imported from:", tools.normal_distribution.__file__)

st.set_page_config(page_title="Steel Analysis Toolbox", layout="wide")

st.title("🧪 Steel Statistical Tools")

tool = st.sidebar.selectbox("Choose a Tool", (
    "Normal Distribution Viewer",
    "Boxplot Element Viewer",
    "Heat Comparison Dashboard"
))

if tool == "Normal Distribution Viewer":
    normal_distribution.run()
elif tool == "Boxplot Element Viewer":
    boxplot_viewer.run()
elif tool == "Heat Comparison Dashboard":
    heat_comparison.run()