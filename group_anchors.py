import pandas as pd
import argparse
import os
import math

def process_groupby(input_file, output_file=None, query_gene_file=None):
    """ Groups by Query_Gene and aggregates anchor/lifted anchor target genes into lists of tuples. """

    # Load data
    df = pd.read_csv(input_file, sep="\t")

    # Convert "NA" values to None (so they can be filtered)
    df.replace("NA", None, inplace=True)

    # Load Query_Gene subset if provided
    query_gene_subset = None
    if query_gene_file:
        with open(query_gene_file, 'r') as f:
            query_gene_subset = set(line.strip() for line in f)

    # Filter if a subset is provided
    if query_gene_subset:
        df = df[df["Query_Gene"].isin(query_gene_subset)]

    # Function to create a list of tuples while skipping None and NaN values
    def make_tuple_list(target_genes, chromosomes):
        return [(gene, chr_) for gene, chr_ in zip(target_genes, chromosomes) 
                if gene and chr_ and not (isinstance(gene, float) and math.isnan(gene)) 
                and not (isinstance(chr_, float) and math.isnan(chr_))]

    # Group by Query_Gene and aggregate into lists of tuples
    grouped_df = df.groupby("Query_Gene").agg({
        "Target_Gene-Anchor": list,
        "Chromosome-Anchor": list,
        "Target_Gene-LiftedAnchor": list,
        "Chromosome-LiftedAnchor": list
    }).reset_index()

    # Apply function to generate tuple lists and remove empty lists
    grouped_df["Target_Gene-Anchor"] = grouped_df.apply(lambda x: make_tuple_list(x["Target_Gene-Anchor"], x["Chromosome-Anchor"]), axis=1)
    grouped_df["Target_Gene-LiftedAnchor"] = grouped_df.apply(lambda x: make_tuple_list(x["Target_Gene-LiftedAnchor"], x["Chromosome-LiftedAnchor"]), axis=1)

    # Drop unused chromosome columns
    grouped_df.drop(columns=["Chromosome-Anchor", "Chromosome-LiftedAnchor"], inplace=True)

    # Set automatic output file name if not provided
    input_base = os.path.splitext(os.path.basename(input_file))[0]  # Get base name without extension
    if not output_file:
        if query_gene_file:
            output_file = f"grouped_filtered_{input_base}.tsv"
        else:
            output_file = f"grouped_{input_base}.tsv"

    # Save to file
    grouped_df.to_csv(output_file, sep="\t", index=False)

    print(f"Grouped results saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Group anchor data by Query_Gene and aggregate Target_Gene lists.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input TSV file")
    parser.add_argument("-o", "--output", required=False, help="Path to the output TSV file (optional, will be auto-generated if not provided)")
    parser.add_argument("-q", "--query_genes", required=False, help="Path to a file containing a subset of Query_Genes (one per line)")

    args = parser.parse_args()
    process_groupby(args.input, args.output, args.query_genes)

if __name__ == "__main__":
    main()
