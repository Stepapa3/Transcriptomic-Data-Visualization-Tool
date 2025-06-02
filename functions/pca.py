from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from adjustText import adjust_text
from sklearn.preprocessing import StandardScaler
import pandas as pd

def pca(normalized_counts, metadata, color_by):
    """
    Performs Principal Component Analysis (PCA) on normalized gene expression data
    and returns a 2D PCA scatter plot with points colored by chosen metadata condition.

    Args:
        normalized_counts (pd.DataFrame): Normalized expression matrix (genes x samples).
        metadata (pd.DataFrame): Sample metadata with grouping information.
        color_by (str): Column name in metadata used for coloring points.

    Returns:
        matplotlib.figure.Figure: A figure containing the PCA scatter plot.
    """

    # Transpose to shape: samples x genes
    normalized_counts = normalized_counts.T

    # Standardize data
    scaler = StandardScaler()
    scaled = scaler.fit_transform(normalized_counts)

    # Perform PCA to reduce to 2 principal components
    pca = PCA(n_components=2)
    components = pca.fit_transform(scaled)

    # Build PCA result DataFrame with sample names and group info
    pca_df = pd.DataFrame(components, columns=["PC1", "PC2"], index=normalized_counts.index)
    pca_df[color_by] = metadata.loc[normalized_counts.index, color_by]

    # Plotting
    fig, ax = plt.subplots(figsize=(8, 6))

    unique_groups = pca_df[color_by].unique()
    colors = plt.cm.tab20.colors  # Use a color palette with up to 20 distinct colors

    texts = []

    # Scatter each group with label
    for i, group in enumerate(unique_groups):
        group_df = pca_df[pca_df[color_by] == group]
        ax.scatter(
            group_df["PC1"],
            group_df["PC2"],
            label=str(group),
            color=colors[i % len(colors)],
            s=80
        )

        # Add sample labels to each point
        for j in range(len(group_df)):
            texts.append(
                ax.text(
                    group_df["PC1"].iloc[j],
                    group_df["PC2"].iloc[j],
                    group_df.index[j],
                    fontsize=9
                )
            )

    # Automatically adjust text to reduce overlaps
    adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray'))

    # Axis labels and title
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_title("PCA of Gene Expression")

    # Legend positioned outside the plot
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title=color_by)
    fig.tight_layout()

    return fig
