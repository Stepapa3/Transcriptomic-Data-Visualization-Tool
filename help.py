import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Help – User Guide")

st.markdown("""
This application is designed for analyzing differential gene expression (DGE) and visualizing its results.
Below you will find a guide to each page, required input formats, examples, and common issues.
""")

# Recommended Workflow
with st.expander("🧭 Recommended Workflow"):
    st.markdown("""
    1. Upload the **count matrix** and **metadata** files on the **Home** page.
    2. Review or create metadata on the **Generate or Edit Metadata** page.
    3. Visualize sample distribution using **PCA** and see a table with total counts per sample on the **Data Overview** page.
    4. Run differential gene expression analysis on the **Differential Gene Expression** page.
    5. Explore and customize result visualizations in the **Visualization** section.
    """)

# Input Formats
with st.expander("📁 Input File Formats"):
    st.markdown("### 🔸 Count Matrix (.csv)")
    st.markdown("A CSV file where the first column contains gene identifiers and the first row contains sample names. Values represent raw read counts:")

    # Use real example from uploaded file
    example_counts = pd.DataFrame({
        "GeneID": ["gene-X276_00010", "gene-X276_00015", "gene-X276_00020", "gene-X276_00025", "gene-X276_00030"],
        "countsB01": ["1753", "747", "6061", "7298", "1332"],
        "countsB02": ["948", "490", "3744", "3786", "1609"],
        "countsB03": ["1501", "723", "5510", "5992", "1432"],
        "countsB04": ["2689", "1155", "8620", "9944", "1085"],
        "countsB05": ["1400", "645", "5084", "5645", "919"],
        "countsB06": ["610", "294", "2158", "2352", "560"],
    })
    st.table(example_counts.set_index("GeneID"))

    st.markdown("### 🔸 Metadata (.csv)")
    st.markdown("A CSV file where the first column contains sample names matching the count matrix and the other columns define experimental conditions. Example:")

    example_meta = pd.DataFrame({
        "SampleID": ["countsB01", "countsB02", "countsB03", "countsB04", "countsB05", "countsB06"],
        "TimePoint": ["T1", "T2", "T3", "T4", "T5", "T6"],
    })
    st.table(example_meta.set_index("SampleID"))

    st.markdown("### 🔸 Gene List (.txt)")
    st.markdown("A plain text file with one gene ID per line. Must match the format used in the count matrix. "
                "It is used for creating heatmap with selected genes on the **Visualization** page.")

    st.code("gene-X276_00010\ngene-X276_00020\ngene-X276_00030\ngene-X276_00025", language="text")

st.markdown("## 📄 Application Pages Guide")

with st.expander("🏠 Home"):
    st.markdown("""
    This is the main page of the application, where users upload input files:

    - **Count matrix** (`.CSV`)
    - **Metadata** (`.CSV`)  
      The required format of these files and example tables are shown in the Input File Format section above.

    Once the **count matrix** is uploaded, the interface will allow you to upload the **metadata file** or allow you to proceed to the Generate Metadata page.

    Upon uploading metadata, automatic validation is triggered with the following rules:

    1. **Sample name match**  
       → Sample names in the metadata (first column, used as index) must exactly match the column names in the count matrix, and be in the same order.

    2. **Missing values**  
       → The metadata must not contain any missing values.

    3. **Annotation requirement**  
       → The metadata must include at least **one column** with experimental annotations (e.g., time point, treatment), in addition to the sample names.

    If validation fails, an error message is displayed and the metadata is **not stored** and cannot be used for analysis..  
    In that case, you can fix the metadata either on the **Generate or Edit Metadata** page or by uploading a corrected file again.

    If both files are uploaded and valid, a success message confirms that you can proceed to the next steps.
    """)


with st.expander("📝 Generate or Edit Metadata"):
    st.markdown("""
    This page enables users to either **create new metadata** if none has been uploaded or **edit the uploaded metadata**.

    **Two tabs are available:**
    - `Create New Metadata`: Automatically generates a metadata table containing sample names from the uploaded count matrix. Users can add any number of condition columns and fill in their values manually.
    - `Edit Existing Metadata`: Allows users to modify any previously uploaded or created metadata.

    **Main features:**
    - Add or delete columns (at least one condition column must remain)
    - Edit values directly in the interactive table
    - Save the metadata to session state
    - Download the current metadata as a CSV file

    **Validation is automatically performed upon saving** according to the rules mentioned in previous section.

    If validation fails, an error message is shown and the metadata is not saved. The table remains editable, so users can fix and revalidate it immediately.

    ---
    **🔧 Common issues & troubleshooting:**
    - *“Metadata contains missing values”* → Fill in all empty cells.
    - *“Mismatch between sample names”* → Ensure the order and names of samples in metadata match the count matrix exactly.
    - *“No condition column detected”* → Add at least one valid condition column.
    - *“Cannot remove column”* → At least one annotation column must remain besides the sample ID.
    """)


with st.expander("📊 Data Overview"):
    st.markdown("""
    This page provides a basic summary of the dataset and helps to assess sample quality and variability.

    ### 🔹 Total Reads per Sample
    Table summarizing the total number of raw reads per sample.  
    This can help detect:
    - **Uneven library sizes**
    - **Outliers or problematic samples**

    ### 🔹 PCA (Principal Component Analysis)
    This allows you to generate a 2D PCA plot from normalized expression data.  
    PCA is used to assess **sample similarity**, detect **batch effects**, or reveal **biological structure**.

    **Before creating the PCA plot:**
    - You must select a **factor** (column from metadata) that will be used for normalization via PyDESeq2 (median-of-ratios normalization).
      This does not affect differential analysis later.
    - You also choose a **coloring factor** which determines which factor is used for coloring of the dots in the PCA plot.
    These inputs are selected in the sidebar on the left of the screen. The PCA plot will show after clicking the button below in the sidebar.

    Each sample is shown as a dot labeled with its name and colored by the selected factor. A legend appears beside the plot for reference.
    """)


with st.expander("🧬 Differential Gene Expression"):
    st.markdown("""
    This page performs the core statistical analysis of the application — differential gene expression (DGE) using PyDESeq2.

    ### 🔹 Settings (in the sidebar)
    Before running the analysis, you must select the following:
    - A **condition column** from metadata used as an experimental factor
    - Two **categories** from that column:
        - One is selected as the **reference condition**
        - The other as the **experimental condition**

    Once selected, press the **Run DGE Analysis** button to start the analysis.

    ### 🔹 Output includes:
    - Full DGE result table with:
        - `baseMean`: average normalized expression of the gene across all samples.
        - `log2FoldChange`: log base 2 of the fold change between the compared conditions; indicates the direction and magnitude of differential expression.
        - `lfcSE`: standard error of the log2 fold change estimate; reflects the uncertainty of the l2FC value.
        - `stat`: test statistic value used for hypothesis testing (Wald test).
        - `p-value`: raw (unadjusted) p-value testing the null hypothesis that there is no difference in expression.
        - `adjusted p-value (padj)`: p-value adjusted for multiple testing using the Benjamini-Hochberg method; used to identify statistically significant differentially expressed genes.
    - An interactive data table with options to:
        - Search by gene
        - Sort by any column
        - Expand to fullscreen
    - A downloadable CSV with all results

    ### 🔹 Summary statistics:
    Below the results, a summary table is shown with the number of:
    - **Upregulated genes**
    - **Downregulated genes**
    - **Not significant genes**

    You can **adjust thresholds** for:
    - `padj` (adjusted p-value) — statistical significance
    - `log2FC` — magnitude of expression change

    The summary and filtered gene tables (up/down) update automatically according to chosen thresholds.

    """)


with st.expander("🖼️ Visualization"):
    st.markdown("""
    This section provides graphical outputs to visualize the results of differential gene expression analysis.

    ### 🔍 Available Plot Types:

    - **MA Plot**  
      Displays the relationship between mean expression (log-transformed) and fold change (log2FC).  
      Genes are colored based on statistical significance and direction of regulation:
        - 🔴 Upregulated (log2FC > 0, padj < threshold)
        - 🔵 Downregulated (log2FC < 0, padj < threshold)
        - ⚫ Not significant  

    - **Volcano Plot**  
      Combines log2FC (X-axis) and –log10 adjusted p-value (Y-axis) to highlight both change in expression and statistical significance.  
      Threshold lines are shown for both log2FC and padj. Genes are categorized similarly as in the MA plot.

    - **Heatmap**  
      Two options are available:
        1. **Top N genes:** Genes with the strongest expression change or statistical significance (selected by `padj` or `log2FC`). The number of shown genes can be changed.
        2. **Custom list:** User uploads a `.txt` file with one gene per line. The example of such file is in **Input File Formats** section.

      Heatmaps are generated using normalized and averaged (by condition) read counts. Data are standardized using Z-score.  
      Optional clustering (UPGMA method using Euclidean distance) can be toggled for both rows and columns.

    ### 📈 Expression Trend Table

    When using a custom gene list, an additional trend table is available. It is useful especially for analyzing expression between more time points.
    It summarizes whether each gene was:
    - Upregulated (`1`)
    - Downregulated (`–1`)
    - Unchanged (`0`)  
    between each pair of **consecutive experimental conditions** (e.g., T2 vs T1, T3 vs T2, ...).

    The condition order is automatically determined based on metadata values, but can be **manually adjusted** before creating the table.
    
    💡 Tip
    All plots can be downloaded by right-clicking on the figure and selecting “Save image as…” from the context menu. 
    This allows users to store figures directly from the interface.
    ---
    **🛠 Issues & troubleshooting:**
    - *“None of the selected genes are present in the count matrix.”* → Ensure gene names in TXT file match exactly with the count matrix gene names.
    """)

st.success("You can return to this page at any time for guidance.")
