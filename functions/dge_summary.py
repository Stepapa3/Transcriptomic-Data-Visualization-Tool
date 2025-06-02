import pandas as pd

def summarize_dge(results, pval_threshold=0.05, lfc_threshold=1.0):
    """
    Summarizes differential gene expression (DGE) results by counting
    upregulated, downregulated, and non-significant genes.

    Also returns separate DataFrames of upregulated and downregulated genes,
    with formatted p-values.

    Args:
        results (pd.DataFrame): DGE result table from PyDESeq2 with columns "log2FoldChange", "padj", and "pvalue".
        pval_threshold (float, optional): Maximum adjusted p-value to consider significance. Default is 0.05.
        lfc_threshold (float, optional): Minimum absolute log2 fold change for biological significance. Default is 1.0.

    Returns:
        pd.DataFrame: Summary table with counts of upregulated, downregulated, and non-significant genes.
        pd.DataFrame: Table of upregulated genes (log2FC > threshold, padj < threshold).
        pd.DataFrame: Table of downregulated genes (log2FC < -threshold, padj < threshold).
    """

    # Count significantly upregulated genes
    upregulated_count = results[
        (results["log2FoldChange"] > lfc_threshold) &
        (results["padj"] < pval_threshold)
    ].shape[0]

    # Count significantly downregulated genes
    downregulated_count = results[
        (results["log2FoldChange"] < -lfc_threshold) &
        (results["padj"] < pval_threshold)
    ].shape[0]

    # Calculate non-significant genes
    not_significant_count = results.shape[0] - upregulated_count - downregulated_count

    # Extract and format upregulated genes
    upregulated = results[
        (results["log2FoldChange"] > lfc_threshold) &
        (results["padj"] < pval_threshold)
    ].copy()
    upregulated["pvalue"] = upregulated["pvalue"].apply(lambda x: f"{x:.2e}")
    upregulated["padj"] = upregulated["padj"].apply(lambda x: f"{x:.2e}")

    # Extract and format downregulated genes
    downregulated = results[
        (results["log2FoldChange"] < -lfc_threshold) &
        (results["padj"] < pval_threshold)
    ].copy()
    downregulated["pvalue"] = downregulated["pvalue"].apply(lambda x: f"{x:.2e}")
    downregulated["padj"] = downregulated["padj"].apply(lambda x: f"{x:.2e}")

    # Create summary DataFrame
    summary_df = pd.DataFrame(
        [[upregulated_count, downregulated_count, not_significant_count]],
        columns=["Upregulated genes", "Downregulated genes", "Not significant"]
    )

    return summary_df, upregulated, downregulated
