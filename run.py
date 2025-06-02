import streamlit as st

# -------------------------------------------------------
# Main navigation file to run a multi-page Streamlit app
# -------------------------------------------------------

# --- Page definitions (script + display title) ---

# Homepage (for data upload)
home_page = st.Page(
    page="home.py",
    title="🏠 Home"
)

# Page for creating or editing metadata
metadata_page = st.Page(
    page="metadata.py",
    title="📝 Generate or Edit Metadata"
)

# Page showing PCA and total read counts
overview_page = st.Page(
    page="overview.py",
    title="📊 Data Overview"
)

# Page for running differential gene expression analysis
dge_page = st.Page(
    page="dge.py",
    title="🧬 Differential Gene Expression"
)

# Page with visualizations: MA plot, Volcano, heatmaps
visualization_page = st.Page(
    page="visualization.py",
    title="	🖼️ Visualization"
)

# Help and usage guide page
help_page = st.Page(
    page="help.py",
    title="❓ Help"
)

# --- Register all pages into a navigation object ---
pgs = st.navigation(
    pages=[home_page, metadata_page, overview_page, dge_page, visualization_page, help_page]
)

# --- Run selected page ---
pgs.run()
