import argparse
import pandas as pd
import re
import os

def parse_gff3(gff3_file, gene_id_key="gene_id", strip_prefix=None):
    """
    Parses the GFF3 file and extracts gene-to-chromosome mappings.
    """
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
                    if strip_prefix and gene_id.startswith(strip_prefix):
                        gene_id = gene_id[len(strip_prefix):]  # Remove the custom prefix
                    gene_to_chr[gene_id] = chr_id
    return gene_to_chr

def process_anchors(anchors_file, gene_to_chr, query_gene_list=None):
    """
    Processes the anchors file, mapping target genes to their chromosomes.
    """
    results = []
    with open(anchors_file, 'r') as f:
        for line in f:
            if line.startswith("#"):
                continue
            fields = line.strip().split()
            if len(fields) < 3:
                continue
            query_gene, target_gene, score = fields[:3]
            if query_gene_list and query_gene not in query_gene_list:
                continue
            chromosome = gene_to_chr.get(target_gene, "Unknown")
            results.append([query_gene, target_gene, chromosome, score])
    return results

def get_user_input():
    """
    Prompt the user for required file paths and settings if command-line arguments are not provided.
    """
    anchors_file = input("Enter the anchors file path: ").strip()
    gff3_file = input("Enter the GFF3 file path: ").strip()
    query_gene_list_file = input("Enter the query gene list file (or press Enter to use all genes): ").strip()

    gene_id_key = input("Enter the gene identifier key (gene_id or ID, default: gene_id): ").strip()
    if gene_id_key not in ["gene_id", "ID"]:
        print("Invalid input. Using default: gene_id")
        gene_id_key = "gene_id"

    strip_prefix_input = input("Enter a prefix to strip from gene IDs (or press Enter to skip): ").strip()
    strip_prefix = strip_prefix_input if strip_prefix_input else None

    return anchors_file, gff3_file, query_gene_list_file, gene_id_key, strip_prefix

# Setup argparse with short flags
parser = argparse.ArgumentParser(description="Extract chromosome mappings from anchors and GFF3 files.")
parser.add_argument("-a", "--anchors_file", help="Path to the anchors file")
parser.add_argument("-g", "--gff3_file", help="Path to the GFF3 file")
parser.add_argument("-q", "--query_gene_list", help="Path to the query gene list file (optional)")
parser.add_argument("-k", "--gene_id_key", choices=["gene_id", "ID"], default="gene_id", help="Gene identifier key (default: gene_id)")
parser.add_argument("-s", "--strip_prefix", help="Prefix to strip from gene IDs (optional)")

args = parser.parse_args()

# Check if arguments were provided or if we should use interactive mode
if args.anchors_file and args.gff3_file:
    anchors_file = args.anchors_file
    gff3_file = args.gff3_file
    query_gene_list_file = args.query_gene_list
    gene_id_key = args.gene_id_key
    strip_prefix = args.strip_prefix
else:
    print("No command-line arguments provided. Switching to interactive mode...")
    anchors_file, gff3_file, query_gene_list_file, gene_id_key, strip_prefix = get_user_input()

# Read query gene list if provided
query_gene_list = None
if query_gene_list_file:
    with open(query_gene_list_file, 'r') as f:
        query_gene_list = set(line.strip() for line in f)

# Generate output file name
anchors_base = os.path.splitext(os.path.basename(anchors_file))[0]
gff3_base = os.path.splitext(os.path.basename(gff3_file))[0]
output_file = f"{anchors_base}_{gff3_base}_output.tsv"

# Parse GFF3
gene_to_chr = parse_gff3(gff3_file, gene_id_key, strip_prefix)

# Process Anchors
output_results = process_anchors(anchors_file, gene_to_chr, query_gene_list)

# Save results
output_df = pd.DataFrame(output_results, columns=["Query_Gene", "Target_Gene", "Chromosome", "Score"])
output_df.to_csv(output_file, sep="\t", index=False)

print(f"Results saved to {output_file}")
