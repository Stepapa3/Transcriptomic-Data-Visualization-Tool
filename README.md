# Transcriptomic Data Visualization Tool

An interactive web-based tool for analyzing **differential gene expression (DGE)** and visualizing transcriptomic data. Built using Python and Streamlit, this application is designed for biologists and bioinformaticians who need an easy-to-use interface for interpreting RNA-seq count data.

## Features

- Upload and validate input files (count matrix and metadata)
- Differential gene expression analysis using [PyDESeq2](https://github.com/owkin/PyDESeq2)
- Summary statistics of differential gene expression
- Principal Component Analysis (PCA) for exploring sample variability
- Volcano and MA plots
- Heatmaps of selected or top differentially expressed genes
- Built-in metadata editor to create or modify sample annotations
- Export of results as CSV or saving plots via right-click
- Integrated help and usage guide within the application

> The user guide is included directly within the application under the "Help" section.

> Note: The application uses **wide mode** by default to improve visibility. If preferred, users can disable wide mode using the three-dot menu in the top right corner of the app.

---

## Run the App Online

This application is deployed via **Streamlit Community Cloud**:

[Launch App](https://transcriptomic-data-visualization-tool-qbssmewxmp37z3pkyq8yjq.streamlit.app/)

---

## Local Installation

If you wish to run the application locally:

### 1. Clone this repository:
```bash
git clone https://github.com/Stepapa3/Transcriptomic-Data-Visualization-Tool.git
cd Transcriptomic-Data-Visualization-Tool
```

### 2. Create a virtual environment (recommended):
```bash
python -m venv .venv
.venv\Scripts\activate # For Windows
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Run the application:
```bash
streamlit run run.py
```

This will start the app in your browser.

---

## Input Requirements

- **Count matrix**: CSV file with genes as rows and sample names as columns (first column must contain gene identifiers)
- **Metadata**: CSV file with sample names in the first column and at least one condition/grouping column

More details and examples are available directly in the app under the **Help** section.

> Example input files are provided in the `test_files` folder within this repository. You can use them to try the tool without preparing your own data.
---

## Requirements

This application requires **Python 3.11.1** and the following Python libraries:

- [adjustText 1.3.0](https://github.com/Phlya/adjustText)
- [matplotlib 3.7.1](https://github.com/matplotlib/matplotlib)
- [natsort 8.4.0](https://github.com/SethMMorton/natsort)
- [numpy 1.24.2](https://github.com/numpy/numpy)
- [pandas 2.2.3](https://github.com/pandas-dev/pandas)
- [pydeseq2 0.5.0](https://github.com/owkin/PyDESeq2)
- [scikit-learn 1.6.1](https://github.com/scikit-learn/scikit-learn)
- [seaborn 0.13.2](https://github.com/mwaskom/seaborn)
- [streamlit 1.43.2](https://github.com/streamlit/streamlit)

---

