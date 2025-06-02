import numpy as np
import matplotlib.pyplot as plt

def ma_plot(results, pval_threshold, comp_label):
    """
    Creates an MA plot to visualize differential gene expression results.

    Genes are colored by significance and fold change direction:
    - Red: upregulated
    - Blue: downregulated
    - Gray: not significant

    Args:
        results (pd.DataFrame): PyDeSeq2 result table with columns "baseMean", "log2FoldChange", and "padj".
        pval_threshold (float): Adjusted p-value threshold to define significance

    Returns:
        matplotlib.figure.Figure: MA plot figure.
    """

    # Classify genes based on direction and statistical significance
    colors = np.where(
        (results["log2FoldChange"] > 0) & (results["padj"] < pval_threshold), "red",
        np.where(
            (results["log2FoldChange"] < 0) & (results["padj"] < pval_threshold), "blue",
            "gray"
        )
    )

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(8, 6))

    # Scatter plot: log baseMean on X, log2FC on Y
    ax.scatter(
        np.log1p(results["baseMean"]),
        results["log2FoldChange"],
        c=colors,
        alpha=0.6
    )

    # Label axes and title
    ax.set_xlabel("Log Base Mean")
    ax.set_ylabel("log2 Fold Change")
    ax.set_title(f"MA Plot ({comp_label.replace('_', ' ')})")

    # Add reference line at y=0
    ax.axhline(y=0, color="black", linestyle="dashed")

    # Add legend manually
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Upregulated'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=8, label='Downregulated'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=8, label='Not significant')
    ]
    ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))

    return fig
