import seaborn as sns
import matplotlib.pyplot as plt


def plot_heatmap(results, normalized_counts, top_n=20):

    # Select significant genes
    significant_genes = results[(results["padj"] < 0.05) & (abs(results["log2FoldChange"]) > 1)]

    if significant_genes.empty:
        return None  # Return None if no significant genes are found

    top_genes = significant_genes.reindex(significant_genes["log2FoldChange"].abs().nlargest(top_n).index).index

    # Extract data from the normalized count matrix
    heatmap_data = normalized_counts.loc[top_genes]

    # Create the heatmap figure
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.clustermap(heatmap_data, z_score = 0, cmap="coolwarm", xticklabels=True, yticklabels=True) #, ax=ax)

    ax.set_title("Heatmap of Top Differentially Expressed Genes")
    ax.set_xlabel("Samples")
    ax.set_ylabel("Genes")

    return fig
