import streamlit as st
from functions.dge_analysis import run_dge_analysis  # Custom function to run DGE using PyDESeq2
from functions.average_counts import average_counts  # Function to compute average normalized counts
from functions.dge_summary import summarize_dge      # Function to summarize DGE results
from functions.normalized_counts import extract_normalized_counts # Function to calculcate normalized counts

st.set_page_config(layout="wide")

st.title("Differential Gene Expression Analysis")

if "dge_done" not in st.session_state:
    st.markdown("*To run the analysis, please select the inputs in the sidebar and click the 'Run DGE Analysis' button.*")

# Check if count matrix and metadata are loaded in session state
if "count_matrix" in st.session_state and "metadata" in st.session_state:
    count_matrix = st.session_state["count_matrix"]
    metadata = st.session_state["metadata"]

    st.sidebar.header("DGE Analysis Parameters")

    # User selects condition factor and reference vs experimental groups
    available_factors = metadata.columns.tolist()
    selected_factor = st.sidebar.selectbox(
        "Select condition column:",
        available_factors,
        help="This column will be used to divide samples into comparison groups (e.g. treatment vs control)."
    )
    unique_levels = metadata[selected_factor].unique().tolist()
    reference = st.sidebar.selectbox(
        "Select reference condition",
        unique_levels,
        help="The reference condition serves as the baseline group for differential expression comparison."
    )
    experimental = st.sidebar.selectbox(
        "Select experimental condition",
        unique_levels,
        help="The experimental condition will be compared against the reference group."
    )
    st.session_state["factor"] = selected_factor

    # Run DGE analysis on button click
    if st.sidebar.button("Run DGE Analysis"):
        with st.spinner("Running DGE Analysis..."):

            comparison_label = f"{experimental}_vs_{reference}".replace(" ", "_")
            filename = f"dge_{comparison_label}.csv"
            st.session_state["comparison_label"] = comparison_label

            results, dds = run_dge_analysis(
                count_matrix,
                [selected_factor, str(experimental), str(reference)],
                metadata,
                selected_factor,
                "dge_results.csv"
            )
            st.session_state["dds"] = dds
            st.session_state["results"] = results

            normalized_counts = extract_normalized_counts(
                st.session_state["count_matrix"],
                st.session_state["metadata"],
                selected_factor
            )

            # Compute average normalized counts
            averaged_counts = average_counts(normalized_counts, metadata, selected_factor)
            st.session_state["average_counts"] = averaged_counts

            st.success("DGE Analysis Completed!")
            st.session_state["dge_done"] = True

    # Display results if analysis has been run
    if st.session_state.get("dge_done"):
        st.write(f"### DGE Results ({st.session_state['comparison_label'].replace('_', ' ')})")

        # Download button for full DGE results as CSV
        st.download_button(
            "Download DGE Results",
            data=st.session_state["results"].to_csv().encode("utf-8"),
            file_name=f"dge_results_{st.session_state['comparison_label']}.csv",
            mime="text/csv"
        )

        # Format p-values for display
        data = st.session_state["results"].copy()
        data["pvalue"] = data["pvalue"].apply(lambda x: f"{x:.2e}")
        data["padj"] = data["padj"].apply(lambda x: f"{x:.2e}")

        # Expandable table of raw DGE results
        with st.expander("Show/hide results", expanded=False):
            st.dataframe(data, height=400)

        st.write(f"### DGE Summary ({st.session_state['comparison_label'].replace('_', ' ')})")

        # User-defined thresholds for filtering significant genes
        col1, col2 = st.columns(2)
        with col1:
            pval_threshold = st.number_input(
                "padj-value Threshold",
                min_value=0.000001,
                max_value=1.0,
                value=0.05,
                step=0.001,
                format="%.5g",
                help="Only genes with adjusted p-values below this threshold will be considered statistically significant."
            )
        with col2:
            lfc_threshold = st.slider(
                "log2 Fold Change Threshold",
                min_value=0.0,
                max_value=5.0,
                value=1.0,
                step=0.1,
                help="Minimum absolute value of log2 fold change to consider gene differentially expressed."
            )

        # Generate and display summary of significant genes
        summary, upregulated, downregulated = summarize_dge(
            st.session_state["results"],
            pval_threshold,
            lfc_threshold
        )
        st.dataframe(summary, hide_index=True)

        with st.expander("Show/hide upregulated genes", expanded=False):
            st.dataframe(upregulated, use_container_width=True)

        with st.expander("Show/hide downregulated genes", expanded=False):
            st.dataframe(downregulated, use_container_width=True)

else:
    st.warning("No data uploaded yet. Please upload count matrix and metadata on the Home page.")
