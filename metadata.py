import streamlit as st
import pandas as pd
from functions.validate_metadata import validate_metadata

st.set_page_config(layout="wide")

st.title("Generate or Edit Metadata")

# Proceed only if the count matrix has been uploaded
if "count_matrix" in st.session_state:
    sample_names = st.session_state["count_matrix"].columns.tolist()

    tab1, tab2 = st.tabs(["Create New Metadata", "Edit Existing Metadata"])

    # === TAB 1: Create New Metadata ===
    with tab1:
        st.subheader("Create Metadata from Scratch")

        default_metadata = pd.DataFrame({
            "SampleID": sample_names,
            "Condition": ["" for _ in sample_names]
        })

        if "new_metadata" not in st.session_state:
            st.session_state["new_metadata"] = default_metadata

        st.write("Fill in all fields. You can add or remove columns as needed.")

        col1, col2 = st.columns(2)

        with col1:
            new_col_name = st.text_input(
                "New column name",
                key="new_col_create",
                help="Enter the name of a new metadata column."
            )
            if st.button("Add Column", key="add_col_create"):
                if new_col_name and new_col_name not in st.session_state["new_metadata"].columns:
                    st.session_state["new_metadata"][new_col_name] = ""

        with col2:
            cols_to_remove = [col for col in st.session_state["new_metadata"].columns if col != "SampleID"]
            if cols_to_remove:
                col_to_remove = st.selectbox(
                    "Select column to remove",
                    cols_to_remove,
                    key="remove_col_create",
                    help="Choose a metadata column to remove. At least one annotation column must remain."
                )
                if st.button("Remove Column", key="remove_button_create"):
                    if len(st.session_state["new_metadata"].columns) > 2:
                        st.session_state["new_metadata"].drop(columns=[col_to_remove], inplace=True)
                    else:
                        st.warning("At least one annotation column must remain.")

        edited = st.data_editor(
            st.session_state["new_metadata"],
            num_rows="fixed",
            use_container_width=True,
            column_config={"SampleID": st.column_config.TextColumn(disabled=True, help="Sample IDs from the count matrix. Cannot be edited.")}
        )

        if st.button("Save Metadata", key="save_create"):
            metadata = edited.set_index("SampleID")
            if not validate_metadata(st.session_state["count_matrix"], metadata):
                st.stop()
            st.session_state["metadata"] = metadata
            st.session_state["metadata_ready"] = True
            st.success("Metadata saved successfully.")
            st.session_state["new_metadata"] = default_metadata.copy()
            csv = metadata.reset_index().to_csv(index=False).encode("utf-8")
            st.download_button("Download Metadata CSV", data=csv, file_name="metadata.csv", mime="text/csv")

    # === TAB 2: Edit Existing Metadata ===
    with tab2:
        if "metadata" in st.session_state:
            st.subheader("Edit Existing Metadata")

            if "metadata_ready" in st.session_state and not st.session_state["metadata_ready"]:
                base_metadata = st.session_state["metadata_to_edit"]
            else:
                base_metadata = st.session_state["metadata"]

            if not base_metadata.empty:
                editable = base_metadata.reset_index()
                st.session_state["edited_metadata"] = editable

                col1, col2 = st.columns(2)

                with col1:
                    new_col_name = st.text_input(
                        "New column name",
                        key="new_col_edit",
                        help="Add a new column to your existing metadata table."
                    )
                    if st.button("Add Column", key="add_col_edit"):
                        if new_col_name and new_col_name not in st.session_state["edited_metadata"].columns:
                            st.session_state["edited_metadata"][new_col_name] = ""

                with col2:
                    cols_to_remove = st.session_state["edited_metadata"].columns.tolist()
                    if len(cols_to_remove) > 1:
                        col_to_remove = st.selectbox(
                            "Select column to remove",
                            cols_to_remove[1:],
                            key="remove_col_edit",
                            help="Select a column to remove from metadata."
                        )
                        if st.button("Remove Column", key="remove_button_edit"):
                            if len(st.session_state["edited_metadata"].columns) > 2:
                                st.session_state["edited_metadata"].drop(columns=[col_to_remove], inplace=True)
                            else:
                                st.warning("At least one annotation column must remain.")

                edited = st.data_editor(
                    st.session_state["edited_metadata"],
                    num_rows="fixed",
                    use_container_width=True
                )

                if st.button("Save Changes", key="save_edit"):
                    metadata = edited.set_index(edited.columns[0])
                    if not validate_metadata(st.session_state["count_matrix"], metadata):
                        st.stop()
                    st.session_state["metadata"] = metadata
                    st.session_state["metadata_ready"] = True
                    st.success("Metadata updated successfully.")
                    csv = metadata.reset_index().to_csv(index=False).encode("utf-8")
                    st.download_button("Download Metadata CSV", data=csv, file_name="edited_metadata.csv", mime="text/csv")
        else:
            st.warning("No metadata available. Please upload or create metadata first.")
else:
    st.warning("Please upload a count matrix on the Home page first.")
