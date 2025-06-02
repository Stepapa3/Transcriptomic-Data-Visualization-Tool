import seaborn as sns


def plot_heatmap(results, average_counts, top_n, row_cl, col_cl, ranking, comp_label):
    """
    Generates a heatmap of the top N most differentially expressed genes,
    selected by either log2 fold change or adjusted p-value.

    Args:
        results (pd.DataFrame): PyDESeq2 results with columns "padj" and "log2FoldChange".
        average_counts (pd.DataFrame): Averaged normalized expression values (genes x conditions).
        top_n (int): Number of top genes to include.
        row_cl (bool): Whether to apply row clustering (genes).
        col_cl (bool): Whether to apply column clustering (conditions).
        ranking (str): Criterion for gene selection - "log2 Fold Change" or "adjusted p-value".

    Returns:
        matplotlib.figure.Figure or None:
            Heatmap figure if significant genes are found, otherwise None.
    """

    # Filter genes that are considered statistically significant
    significant_genes = results[
        (results["padj"] < 0.05) & (abs(results["log2FoldChange"]) > 1)
    ]

    # If no significant genes are found, return None
    if significant_genes.empty:
        return None

    # Select top N genes by the chosen ranking method
    if ranking == "log2 Fold Change":
        # Select genes with the highest absolute log2 fold change
        top_genes = significant_genes.reindex(
            significant_genes["log2FoldChange"].abs().nlargest(top_n).index
        ).index
    elif ranking == "adjusted p-value":
        # Select genes with the lowest adjusted p-values
        top_genes = significant_genes.nsmallest(top_n, "padj").index

    # Retrieve the expression values for the selected genes
    heatmap_data = average_counts.loc[top_genes]

    # Create heatmap
    g = sns.clustermap(
        heatmap_data,
        z_score=0,
        cmap="coolwarm",
        xticklabels=True,
        yticklabels=True,
        row_cluster=row_cl,
        col_cluster=col_cl,
        cbar_kws={"label": "Z-score"}
    )

    # Adjust the font size of gene labels based on number of genes
    n_genes = heatmap_data.shape[0]
    fontsize = max(4, 12 - n_genes // 10)

    # Set axis labels and the plot title
    g.ax_heatmap.set_xlabel("Condition")
    g.ax_heatmap.set_ylabel("Gene")
    g.fig.suptitle(f"Heatmap of Top Differentially Expressed Genes ({comp_label.replace('_', ' ')})", y=1.02)
    # Apply dynamically calculated font size to gene labels
    g.ax_heatmap.set_yticklabels(g.ax_heatmap.get_yticklabels(), fontsize=fontsize)

    return g.fig
