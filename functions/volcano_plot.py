import numpy as np
import matplotlib.pyplot as plt

def volcano_plot(results, pval_threshold, lfc_threshold, comp_label):
    """
    Creates a volcano plot to visualize differential gene expression.

    Points are colored by direction and statistical significance:
    - Red: significantly upregulated (log2FC > threshold, padj < threshold)
    - Blue: significantly downregulated (log2FC < -threshold, padj < threshold)
    - Gray: not significant

    Args:
        results (pd.DataFrame): PyDeSeq2 result table with columns "log2FoldChange" and "padj".
        pval_threshold (float): Adjusted p-value threshold.
        lfc_threshold (float): Log2 fold change threshold.

    Returns:
        matplotlib.figure.Figure: The volcano plot figure.
    """

    # Classify each gene based on thresholds
    colors = np.where(
        (results["log2FoldChange"] > lfc_threshold) & (results["padj"] < pval_threshold), "red",
        np.where(
            (results["log2FoldChange"] < -lfc_threshold) & (results["padj"] < pval_threshold), "blue",
            "gray"
        )
    )

    # Replace padj = 0 with a very small value to avoid -log10(0)
    padj_safe = results["padj"].clip(lower=1e-300)

    # Create plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Scatter: log2FC on X-axis, -log10(padj) on Y-axis
    ax.scatter(
        results["log2FoldChange"],
        -np.log10(padj_safe),
        c=colors,
        alpha=0.6
    )

    # Axis labels and title
    ax.set_xlabel("log2 Fold Change")
    ax.set_ylabel("-log10 Adjusted p-value")
    ax.set_title(f"Volcano Plot ({comp_label.replace('_', ' ')})")

    # Draw thresholds
    ax.axhline(
        y=-np.log10(pval_threshold),
        color='black',
        linestyle='dashed',
        label=f"padj = {pval_threshold}"
    )
    ax.axvline(
        x=-lfc_threshold,
        color='black',
        linestyle='dashed',
        label=f"log2FC = ±{lfc_threshold}"
    )
    ax.axvline(
        x=lfc_threshold,
        color='black',
        linestyle='dashed'
    )

    # Custom legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Upregulated'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=8, label='Downregulated'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=8, label='Not significant')
    ]
    ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))

    return fig
