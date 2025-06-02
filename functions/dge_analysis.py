from pydeseq2.ds import DeseqStats
from pydeseq2.dds import DeseqDataSet
import pandas as pd

def run_dge_analysis(count_matrix, contrast, metadata, factor, output_path):
    """
    Runs differential gene expression (DGE) analysis using PyDESeq2.

    Args:
        count_matrix (pd.DataFrame): Raw count matrix (genes x samples).
        contrast (list of str): Contrast to evaluate, e.g. ["condition", "treated", "control"].
        metadata (pd.DataFrame): Metadata table with experimental conditions.
        factor (str): Column in metadata to use as the design factor.
        output_path (str): File path where DGE results will be saved as CSV.

    Returns:
        pd.DataFrame: DGE results including log2FoldChange, p-values, etc.
        DeseqDataSet: Fitted DESeq2 dataset object.
    """

    # Transpose to match PyDESeq2 expectations (samples as rows)
    count_matrix = count_matrix.T

    # Ensure categorical factor is string-type
    metadata[factor] = metadata[factor].astype(str)

    # Create and run DESeq2 analysis
    dds = DeseqDataSet(
        counts=count_matrix,
        metadata=metadata,
        design_factors=[factor]
    )
    dds.deseq2()

    # Extract statistics for selected contrast
    stat_res = DeseqStats(dds, contrast=contrast)
    stat_res.summary()
    results = stat_res.results_df

    # Save results to file
    results.to_csv(output_path)
    print(f"DGE results saved to: {output_path}")

    return results, dds