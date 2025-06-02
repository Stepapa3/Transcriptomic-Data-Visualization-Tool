def average_counts(normalized_counts, metadata, factor):
    """
    Computes the average normalized gene expression for each condition group.

    Args:
        normalized_counts (pd.DataFrame): DataFrame of normalized counts
        metadata (pd.DataFrame): Sample metadata
        factor (string): Chooses metadata column used to average counts

    Returns:
        pd.DataFrame: A DataFrame with average expression values per condition
    """
    # Group samples by condition and compute the mean expression for each gene
    average_counts = normalized_counts.groupby(metadata[factor].astype(str), axis=1).mean()

    return average_counts
