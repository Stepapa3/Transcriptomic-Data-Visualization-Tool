import seaborn as sns
import pandas as pd


def custom_heatmap(selected_genes, average_counts, row_cluster, col_cluster):
    """
    Generates a heatmap of selected genes.

    Args:
        selected_genes (list of str): List of gene names to include in the heatmap.
        average_counts (pd.DataFrame): DataFrame of average expression values (genes x conditions).
        row_cluster (bool): Whether to cluster rows (genes).
        col_cluster (bool): Whether to cluster columns (samples/conditions).

    Returns:
        matplotlib.figure.Figure: The generated heatmap figure, or None if no valid genes are found.
    """

    # Identify genes provided by the user that are not present in the expression matrix (due to typos or missing entries)
    missing_genes = list(set(selected_genes) - set(average_counts.index))

    # Check if any genes are provided
    if not selected_genes:
        return None, missing_genes


    # Subset the data to include only genes found in the DataFrame index
    data = average_counts.loc[average_counts.index.intersection(selected_genes)]

    # Return None if no matching genes are found in the dataset
    if data.empty:
        return None, missing_genes

    # Determine font size for gene labels based on the number of selected genes
    n_genes = data.shape[0]
    fontsize = max(4, 12 - n_genes // 10)

    # Create the clustered heatmap with z-score normalization across genes (rows)
    g = sns.clustermap(
        data,
        z_score=0,
        cmap="coolwarm",
        xticklabels=True,
        yticklabels=True,
        row_cluster=row_cluster,
        col_cluster=col_cluster,
        cbar_kws={"label": "Z-score"}
    )

    # Set axis labels and the title of the plot
    g.ax_heatmap.set_xlabel("Condition")
    g.ax_heatmap.set_ylabel("Gene")
    g.fig.suptitle("Heatmap of Selected Genes", y=1.02)
    # Apply dynamically calculated font size to gene labels
    g.ax_heatmap.set_yticklabels(g.ax_heatmap.get_yticklabels(), fontsize=fontsize)

    return g.fig, missing_genes
