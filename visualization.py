import streamlit as st
from functions.maplot import ma_plot
from functions.volcano_plot import volcano_plot
from functions.clustermap import plot_heatmap
from functions.clustermap_custom import custom_heatmap
from functions.expression_trends import expression_trends
from natsort import natsorted

# Set page layout to wide and title
st.set_page_config(layout="wide")
st.title("DGE Data Visualization")

# Proceed only if DGE results exist in session state
if "results" in st.session_state:

    # Create 4 tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs([
        "MA Plot",
        "Volcano Plot",
        "Heatmap with Top Genes",
        "Heatmap with Custom Genes"
    ])

    # ---------------- TAB 1: MA PLOT ----------------
    with tab1:
        st.write("## Settings")
        # Adjusted p-value threshold input for MA plot
        pval_threshold_ma = st.number_input(
            "padj-value Threshold",
            min_value=0.000001,
            max_value=1.0,
            value=0.05,
            step=0.001,
            format="%.5g",
            key="pval_ma",
            help="Only genes with adjusted p-value (padj) below this threshold will be highlighted."
        )
        # Plot MA plot
        st.pyplot(ma_plot(st.session_state["results"], pval_threshold=pval_threshold_ma, comp_label=st.session_state["comparison_label"]))

    # ---------------- TAB 2: VOLCANO PLOT ----------------
    with tab2:
        st.write("## Settings")
        col1, col2 = st.columns(2)
        with col1:
            # Fold change threshold input
            lfc_threshold = st.slider(
                "log2 Fold Change threshold",
                0.0, 5.0, 1.0,
                step=0.1,
                key="lfc_volcano",
                help="Minimum absolute value of log2 fold change to highlight significant genes."
            )
        with col2:
            # Adjusted p-value threshold input
            pval_threshold_volcano = st.number_input(
                "padj-value Threshold",
                min_value=0.000001,
                max_value=1.0,
                value=0.05,
                step=0.001,
                format="%.5g",
                key="pval_volcano",
                help="Only genes with adjusted p-value (padj) below this threshold will be considered significant."
            )
        # Plot volcano plot
        st.pyplot(volcano_plot(
            st.session_state["results"],
            pval_threshold=pval_threshold_volcano,
            lfc_threshold=lfc_threshold,
            comp_label=st.session_state["comparison_label"]
        ))

    # ---------------- TAB 3: HEATMAP WITH TOP GENES ----------------
    with tab3:
        st.write("## Settings")
        # Select number of top genes for heatmap
        top_n = st.slider(
            "Select Top N Genes for Heatmap",
            min_value=5,
            max_value=100,
            value=20,
            help="Choose number of the most significant genes (based on padj and fold change) to be shown in the heatmap."
        )

        cluster_col, select_col = st.columns(2)
        with cluster_col:
            st.write("### Clustering")
            # Options for clustering rows and columns
            row_clustering = st.checkbox(
                "Enable row clustering",
                help="Group genes with similar expression profiles.",
                key="row"
            )
            col_clustering = st.checkbox(
                "Enable column clustering",
                help="Cluster conditions based on expression similarity.",
                key="col"
            )

        with select_col:
            st.write("### Gene Selection Method")
            # Radio selector for ranking method
            ranking = st.radio(
                "Choose how to select top genes:",
                ["log2 Fold Change", "adjusted p-value"],
                help="Select one method:\n"
                     "- log2 Fold Change: largest expression changes\n"
                     "- adjusted p-value: most statistically significant"
            )

        # Create heatmap with top N selected genes
        heatmap = plot_heatmap(
            st.session_state["results"],
            st.session_state["average_counts"],
            top_n,
            row_clustering,
            col_clustering,
            ranking,
            comp_label=st.session_state["comparison_label"]
        )

        # Plot heatmap if exists
        if heatmap is None:
            st.warning("No genes passed the default thresholds for being considered differentially expressed (adjusted p-value < 0.05 and |log2 fold change| > 1).")
        else:
            st.pyplot(heatmap)

    # ---------------- TAB 4: HEATMAP WITH CUSTOM GENES ----------------
    with tab4:
        st.write("## Settings")

        genes = []
        col1, col2 = st.columns(2)
        with col1:
            st.write("### Choose genes to create heatmap")
            # Upload a file containing selected gene names
            selected_genes_file = st.file_uploader(
                "Upload file with selected genes (TXT)",
                type=["txt"],
                help="Upload a plain text file containing a list of gene names, one per line."
            )

        with col2:
            st.write("### Clustering")
            # Clustering settings
            row_clustering_custom = st.checkbox(
                "Enable row clustering",
                help="Group genes with similar expression profiles.",
                key="custom_row"
            )
            col_clustering_custom = st.checkbox(
                "Enable column clustering",
                help="Cluster conditions based on expression similarity.",
                key="custom_col"
            )

        if selected_genes_file:
            # Read gene list from file
            genes = [g.strip() for g in selected_genes_file.read().decode("utf-8").splitlines() if g.strip()]
            st.session_state["custom_genes"] = genes

        if "custom_genes" in st.session_state:
            # Create heatmap from user-specified gene list
            fig, missing_genes = custom_heatmap(
                st.session_state["custom_genes"],
                st.session_state["average_counts"],
                row_clustering_custom,
                col_clustering_custom
            )

            # Plot heatmap if figure exists
            if fig is None:
                if not genes:
                    st.warning("No genes found in the uploaded file.")
                else:
                    st.warning("None of the selected genes are present in the count matrix.")
            else:
                if missing_genes:
                    st.warning(f"The following genes were not found and were ignored: {', '.join(missing_genes)}")
                st.pyplot(fig)

                # ----------- Expression trends section ------------
                st.write("## Expression Trends")

                # Get available condition levels from metadata
                available_conditions = st.session_state["metadata"][st.session_state["factor"]].astype(
                    str).unique().tolist()
                default_order = natsorted(available_conditions)  # Use natural sorting for default suggestion

                # User-defined condition order for trend comparison
                ordered_conditions = st.multiselect(
                    "Change order of conditions for trend table if needed:",
                    options=default_order,
                    default=default_order,
                    help="Select all conditions and arrange them in the desired order.",
                    key="custom_condition_order"
                )

                # Check if all conditions are selected (to ensure completeness)
                if set(ordered_conditions) != set(default_order):
                    st.warning("Please select all conditions in the desired order.")
                else:
                    # --- Threshold inputs ---
                    col1, col2 = st.columns(2)
                    with col1:
                        l2fc_threshold = st.slider(
                            "log2 Fold Change threshold",
                            0.0, 5.0, 1.0,
                            step=0.1,
                            key="l2fc_thr",
                            help="Minimum absolute value of log2 fold change to consider gene differentially expressed."
                        )
                    with col2:
                        padj_threshold = st.number_input(
                            "padj-value Threshold",
                            min_value=0.000001,
                            max_value=1.0,
                            value=0.05,
                            step=0.001,
                            format="%.5g",
                            key="padj_threshold",
                            help = "Only genes with adjusted p-values below this threshold will be considered statistically significant."
                        )

                    # Create and display expression trend table on button click
                    if st.button("Create trend table"):
                        table = expression_trends(
                            genes=st.session_state["custom_genes"],
                            condition_order=ordered_conditions,
                            factor=st.session_state["factor"],
                            padj_threshold=padj_threshold,
                            l2fc_threshold=l2fc_threshold,
                            dds=st.session_state["dds"]
                        )

                        # Display result as an interactive dataframe
                        st.dataframe(table)

                        # Download button for exporting the trend table
                        table_data = table.to_csv(index=True).encode("utf-8")
                        st.download_button(
                            "Download trend table",
                            data=table_data,
                            file_name="trend_table.csv",
                            mime="text/csv"
                        )


else:
    # Show warning if no DGE results were found
    st.warning("Differential gene expression analysis must be performed first.")
