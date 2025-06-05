import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def run():
    st.subheader("🔥 Heat Element Comparison Dashboard")

    uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])
    if uploaded_file:
        # --- Load File ---
        try:
            if uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"❌ Error loading file: {e}")
            return

        # --- Clean and Validate Data ---
        if df.empty or len(df.columns) < 2:
            st.error("The file must contain at least one heat column and one element column.")
            return

        df.columns = df.columns.str.strip()
        heat_column = df.columns[0]
        element_columns = df.columns[1:]
        df[heat_column] = df[heat_column].astype(str).str.strip()

        # --- Sidebar Inputs ---
        col1, col2 = st.columns(2)
        with col1:
            selected_elements = st.multiselect("📌 Select Elements", element_columns)
        with col2:
            selected_heats = st.multiselect("🔥 Select Heat Numbers", df[heat_column].unique())

        # --- Chart Section ---
        if selected_elements and selected_heats:
            st.subheader("📈 Comparison Charts")
            filtered_df = df[df[heat_column].isin(selected_heats)][[heat_column] + selected_elements]
            melted_df = pd.melt(filtered_df, id_vars=heat_column, var_name='Element', value_name='Value')

            for element in selected_elements:
                with st.expander(f"📊 {element} Chart", expanded=True):
                    subset = melted_df[melted_df["Element"] == element]

                    if subset.empty:
                        st.warning(f"No data available for {element}.")
                        continue

                    fig, ax = plt.subplots(figsize=(8, 4))
                    bars = ax.bar(subset[heat_column], subset["Value"], color='seagreen')
                    for bar in bars:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2, height / 2,
                                f"{height:.3f}", ha='center', va='center',
                                color='white', fontsize=9, fontweight='bold')

                    ax.set_xlabel("Heat Number")
                    ax.set_ylabel(f"{element} Value")
                    ax.set_title(f"{element} Comparison Across Heats")
                    ax.grid(True, linestyle='--', alpha=0.7)
                    st.pyplot(fig)
        else:
            st.info("🔍 Please select at least one heat and one variable to display charts.")
