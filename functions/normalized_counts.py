import pandas as pd
from pydeseq2.dds import DeseqDataSet

def extract_normalized_counts(count_matrix, metadata, design_factor):
    """
    Runs PyDESeq2 normalization and returns normalized count matrix.
    Automatically uses the first column of metadata as the design factor.

    Args:
        count_matrix (pd.DataFrame): Raw count matrix (genes x samples)
        metadata (pd.DataFrame): Sample metadata (samples as index)

    Returns:
        pd.DataFrame: Normalized count matrix (genes x samples)
    """
    # Transpose to shape expected by PyDESeq2 (samples x genes)
    count_matrix = count_matrix.T

    # Automatically select the first column as the design factor
    metadata[design_factor] = metadata[design_factor].astype(str)

    # Create DESeq2 dataset object
    dds = DeseqDataSet(
        counts=count_matrix,
        metadata=metadata,
        design_factors=[design_factor]
    )

    # Run DESeq2 normalization
    dds.deseq2()

    # Extract normalized counts and transpose back (genes x samples)
    normalized_counts = pd.DataFrame(
        (dds.layers["normed_counts"]).T,
        index=dds.var_names,
        columns=dds.obs_names
    )

    return normalized_counts
