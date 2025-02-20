import pandas as pd
import re
import os
import argparse

def parse_gff3(gff3_file, gene_id_key="gene_id", strip_prefix=False):
    """ Parses the GFF3 file and extracts gene-to-chromosome mappings. """
    gene_to_chr = {}
    with open(gff3_file, 'r') as f:
        for line in f:
            if line.startswith("#"):
                continue
            fields = line.strip().split("\t")
            if len(fields) < 9:
                continue
            
            feature_type = fields[2]
            if feature_type == "gene":
                chr_id = fields[0]
                attributes = fields[8]

                match = re.search(rf'{gene_id_key}=([^;]+)', attributes)
                if match:
                    gene_id = match.group(1)
                    if strip_prefix:
                        gene_id = gene_id.lstrip("gene:")
                    gene_to_chr[gene_id] = chr_id

    return gene_to_chr

def process_anchors(anchors_file, gene_to_chr):
    """ Processes the anchors file, mapping target genes to their chromosomes. """
    results = {}
    with open(anchors_file, 'r') as f:
        for line in f:
            if line.startswith("#"):
                continue
            fields = line.strip().split()
            if len(fields) < 3:
                continue
            
            query_gene, target_gene, score = fields[:3]
            chromosome = gene_to_chr.get(target_gene, "Unknown")

            if query_gene not in results:
                results[query_gene] = []
            results[query_gene].append((target_gene, chromosome, score))
    
    return results

def merge_results(anchor_data, lifted_data):
    """ Merges anchor and lifted anchor results. """
    merged = []
    all_queries = set(anchor_data.keys()).union(set(lifted_data.keys()))

    for query_gene in sorted(all_queries):
        anchor_entries = anchor_data.get(query_gene, [("NA", "NA", "NA")])
        lifted_entries = lifted_data.get(query_gene, [("NA", "NA", "NA")])

        max_entries = max(len(anchor_entries), len(lifted_entries))

        for i in range(max_entries):
            anchor_values = anchor_entries[i] if i < len(anchor_entries) else ("NA", "NA", "NA")
            lifted_values = lifted_entries[i] if i < len(lifted_entries) else ("NA", "NA", "NA")

            merged.append([query_gene] + list(anchor_values) + list(lifted_values))

    return merged

def main():
    parser = argparse.ArgumentParser(description="Combine anchor and lifted anchor files.")
    parser.add_argument("-a", "--anchor", help="Path to the anchor file")
    parser.add_argument("-l", "--lifted", help="Path to the lifted anchor file")
    parser.add_argument("-g", "--gff3", help="Path to the GFF3 file")
    
    args = parser.parse_args()

    # Interactive input if arguments are missing
    anchor_file = args.anchor if args.anchor else input("Enter the anchor file path: ").strip()
    lifted_file = args.lifted if args.lifted else input("Enter the lifted anchor file path: ").strip()
    gff3_file = args.gff3 if args.gff3 else input("Enter the GFF3 file path: ").strip()

    # Ask user for gene identifier key
    gene_id_key = input("Enter the gene identifier key (gene_id or ID, default: gene_id): ").strip()
    if gene_id_key not in ["gene_id", "ID"]:
        print("Invalid input. Using default: gene_id")
        gene_id_key = "gene_id"

    # Ask user if they want to strip "gene:" prefixes
    strip_prefix_input = input("Do you want to strip 'gene:' prefixes? (yes/no, default: no): ").strip().lower()
    strip_prefix = strip_prefix_input == "yes"

    # Parse GFF3 file
    gene_to_chr = parse_gff3(gff3_file, gene_id_key, strip_prefix)

    # Process anchor and lifted anchor files
    anchor_data = process_anchors(anchor_file, gene_to_chr)
    lifted_data = process_anchors(lifted_file, gene_to_chr)

    # Merge results
    merged_results = merge_results(anchor_data, lifted_data)

    # Generate output file name
    output_file = f"combined_{os.path.basename(anchor_file)}_{os.path.basename(lifted_file)}.tsv"

    # Save results
    output_df = pd.DataFrame(merged_results, columns=[
        "Query_Gene", 
        "Target_Gene-Anchor", "Chromosome-Anchor", "Score-Anchor", 
        "Target_Gene-LiftedAnchor", "Chromosome-LiftedAnchor", "Score-LiftedAnchor"
    ])
    output_df.to_csv(output_file, sep="\t", index=False)

    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
