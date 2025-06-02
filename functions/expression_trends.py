from pydeseq2.ds import DeseqStats
import pandas as pd

def expression_trends(genes, condition_order, factor, padj_threshold, l2fc_threshold, dds):
    """
    Computes expression trends for selected genes across user-defined consecutive conditions.

    For each consecutive condition pair (e.g., t2 vs t1, t3 vs t2), the function performs a pairwise
    differential expression analysis using PyDESeq2 results and evaluates the regulation status of each gene.
    Genes are categorized as upregulated ("1"), downregulated ("-1"), unchanged ("0"), or not available ("NA")
    based on log2 fold change and adjusted p-value thresholds.

    Args:
        genes (list of str): List of gene identifiers to evaluate.
        condition_order (list of str): Ordered list of condition labels
        factor (str): Metadata column representing the condition factor used for contrasts.
        padj_threshold (float): Maximum adjusted p-value to consider a gene statistically significant.
        l2fc_threshold (float): Minimum absolute log2 fold change for a gene to be biologically relevant.
        dds (DeseqDataSet): Pre-fitted PyDESeq2 object containing all samples.

    Returns:
        pd.DataFrame: A table showing the regulation trend of each gene across condition pairs.
                      Cell values: "1" (upregulated), "-1" (downregulated), "0" (no significant change), "NA" (gene not found).
    """

    # Initialize result DataFrame with genes as rows
    trends = pd.DataFrame(index=genes)

    # Loop over consecutive condition pairs
    for i in range(1, len(condition_order)):
        cond1, cond2 = condition_order[i - 1], condition_order[i]
        pair_label = f"{cond2} vs {cond1}"  # e.g., t2 vs t1

        # Compute differential expression for the given condition pair
        stat_res = DeseqStats(dds, contrast=[factor, str(cond2), str(cond1)])
        stat_res.summary()
        results = stat_res.results_df

        gene_trends = []
        for gene in genes:
            # If gene is not present in result table, label as "NA"
            if gene not in results.index:
                gene_trends.append("NA")
                continue

            row = results.loc[gene]

            # Determine regulation status based on statistical thresholds
            if row["padj"] < padj_threshold:
                if row["log2FoldChange"] > l2fc_threshold:
                    gene_trends.append("1")   # Upregulated
                elif row["log2FoldChange"] < -l2fc_threshold:
                    gene_trends.append("-1")  # Downregulated
                else:
                    gene_trends.append("0")   # Statistically significant but small effect
            else:
                gene_trends.append("0")       # Not statistically significant

        # Add current condition pair as a new column
        trends[pair_label] = gene_trends

    return trends
