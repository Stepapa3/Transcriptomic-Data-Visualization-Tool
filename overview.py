import streamlit as st
from functions.pca import pca  # Custom function to compute and plot PCA
from functions.normalized_counts import extract_normalized_counts  # Custom function for normalization

# Set Streamlit page layout to wide
st.set_page_config(layout="wide")

# Set the main page title
st.title("Data Overview")

# Check if both count matrix and metadata are available in session state
if "count_matrix" in st.session_state and "metadata" in st.session_state:

    # --- Sidebar options for PCA ---
    st.sidebar.write("## PCA Settings")

    # Select design factor for normalization (used only for visualization)
    factor = st.sidebar.selectbox(
        "Design factor for normalization",
        options=st.session_state["metadata"].columns,
        help="This factor will only be used for normalization and PCA visualization. "
             "You will choose the design factor for differential expression analysis separately."
    )

    # Select metadata column to color the PCA samples by
    selected_factor = st.sidebar.selectbox(
        "Color samples by",
        options=st.session_state["metadata"].columns,
        help="This will determine the sample coloring in the PCA plot."
    )

    # Generate PCA plot on button click
    if st.sidebar.button("Create PCA plot"):
        with st.spinner("Creating PCA..."):
            # Normalize counts using the selected design factor
            normalized_counts = extract_normalized_counts(
                st.session_state["count_matrix"],
                st.session_state["metadata"],
                factor
            )

            # --- PCA Section ---
            st.write("### Principal Component Analysis (PCA)")
            st.pyplot(pca(
                normalized_counts,
                st.session_state["metadata"],
                selected_factor
            ))

    # --- Total Reads Section ---
    st.write("### Total Reads per Sample")

    # Calculate total raw reads for each sample from the count matrix
    total_counts = st.session_state["count_matrix"].sum(axis=0).reset_index()
    total_counts.columns = ["Sample", "Total reads"]

    # Format numbers with spaces (e.g. 1 234 567)
    total_counts["Total reads"] = total_counts["Total reads"].apply(lambda x: f'{x:,}'.replace(',', ' '))

    # Display formatted total reads as a table
    st.table(total_counts.set_index("Sample"))

else:
    # Show a warning if data is not yet uploaded
    st.warning("No data uploaded yet. Please upload your files on the **Home** page.")
