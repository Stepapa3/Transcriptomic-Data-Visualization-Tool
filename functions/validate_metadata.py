import streamlit as st

def validate_metadata(count_matrix, metadata):
    """
    Validates the structure and contents of the uploaded metadata.

    Checks:
    1. Sample names in count matrix columns must exactly match metadata index.
    2. Metadata must contain at least one annotation column.
    3. Metadata must not contain any missing values (NaN or empty strings).

    Parameters:
        count_matrix (pd.DataFrame): The count matrix with samples as columns.
        metadata (pd.DataFrame): The metadata with sample names as index.

    Returns:
        bool: True if metadata is valid, False otherwise (Streamlit error is shown).
    """


    # 1. Check for missing values (NaN or empty strings)
    if metadata.isnull().values.any() or (metadata == "").any().any():
        st.error("Metadata contains missing values. Please fill in all cells before proceeding.")
        return False

    # 2. Check sample name match (index vs. count matrix columns)
    if not all(metadata.index == count_matrix.columns):
        print(metadata.index)
        st.error("Mismatch between sample names in count matrix and metadata! "
                 "Ensure that column names in the count matrix match the index in metadata (first column).")
        return False

    # 3. Check that there is at least one annotation column
    if metadata.shape[1] < 1:
        st.error("No condition colum detected. Metadata must contain at least one column with experimental conditions.")
        return False

    return True
