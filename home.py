import streamlit as st
import pandas as pd
from functions.validate_metadata import validate_metadata
from functions.detect_delimiter import detect_delimiter

st.set_page_config(layout="wide")

# Page title
st.title("Home")

st.write("### Upload your files here to start.")

# Layout: two columns for uploading files
col1, col2 = st.columns(2)

# -------- Upload count matrix --------
with col1:
    count_matrix_file = st.file_uploader(
        "Upload Count Matrix (CSV)",
        type=["csv"],
        help="Upload a CSV file with raw gene expression counts. Rows should represent genes, and columns should represent samples. The first column must contain gene names."
    )

# If count matrix is uploaded, load and store it
if count_matrix_file:
    delimiter = detect_delimiter(count_matrix_file)
    count_matrix = pd.read_csv(count_matrix_file, index_col=0, delimiter=delimiter)
    st.session_state["count_matrix"] = count_matrix

# -------- Upload metadata --------
if "count_matrix" in st.session_state and "metadata" not in st.session_state:
    st.success("Count matrix successfully uploaded. Now upload metadata or create it on the Generate Metadata page.")

    with col2:
        metadata_file = st.file_uploader(
            "Upload Metadata (CSV)",
            type=["csv"],
            help="Upload a CSV file containing sample metadata. The first column must match the sample names (columns) in the count matrix. Other columns define conditions or groups."
        )

    # Uploading metadata file
    if metadata_file:
        delimiter = detect_delimiter(metadata_file)
        st.session_state["metadata_ready"] = False
        with st.spinner("Processing data..."):
            # Load metadata and set first column as index
            metadata = pd.read_csv(metadata_file, index_col=0, delimiter=delimiter)

            # Metadata validation
            if not validate_metadata(st.session_state["count_matrix"], metadata):
                st.session_state["metadata_to_edit"] = metadata
                st.stop()

            # Save to session state
            st.session_state["metadata"] = metadata
            st.session_state["metadata_ready"] = True
            st.session_state["dge_done"] = False

            st.success("Files successfully uploaded.")

elif "count_matrix" in st.session_state and "metadata" in st.session_state:
    st.success("Files successfully uploaded.")
