import pandas as pd
import re
import os

# Function to parse the GFF3 file and extract gene to chromosome mapping
def parse_gff3(gff3_file, gene_id_key="gene_id", strip_prefix=False):
    """
    Parses the GFF3 file and extracts gene-to-chromosome mappings.
    
    Parameters:
    - gff3_file: Path to the GFF3 file.
    - gene_id_key: The key used to extract gene names (either "gene_id" or "ID").
    - strip_prefix: Whether to strip "gene:" prefixes (default: False).

    Returns:
    - A dictionary mapping gene names to chromosome IDs.
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
                chr_id = fields[0]  # Chromosome info is in the first column
                attributes = fields[8]

                # Extract gene ID based on user preference
                match = re.search(rf'{gene_id_key}=([^;]+)', attributes)

                if match:
                    gene_id = match.group(1)
                    if strip_prefix:
                        gene_id = gene_id.lstrip("gene:")  # Strip prefix if enabled
                    gene_to_chr[gene_id] = chr_id  # Store mapping

    return gene_to_chr

# Function to process the anchors file and return chromosome mappings
def process_anchors(anchors_file, gene_to_chr, query_gene_list=None):
    """
    Processes the anchors file, mapping target genes to their chromosomes.

    Parameters:
    - anchors_file: Path to the anchors file.
    - gene_to_chr: Dictionary mapping gene names to chromosome IDs.
    - query_gene_list: Optional list of query genes to filter results.

    Returns:
    - A list of [Query_Gene, Target_Gene, Chromosome, Score] entries.
    """
    results = []
    with open(anchors_file, 'r') as f:
        for line in f:
            if line.startswith("#"):  # Skip comments
                continue
            fields = line.strip().split()
            if len(fields) < 3:
                continue
            
            query_gene, target_gene, score = fields[:3]  # Extract relevant columns
            if query_gene_list and query_gene not in query_gene_list:
                continue
            chromosome = gene_to_chr.get(target_gene, "Unknown")  # Lookup chromosome
            
            results.append([query_gene, target_gene, chromosome, score])
    
    return results

# Input file paths
anchors_file = input("Enter the anchors file path: ").strip()
gff3_file = input("Enter the GFF3 file path: ").strip()
query_gene_list_file = input("Enter the query gene list file (or press Enter to use all genes): ").strip()

# Ask user for gene identifier key (default: "gene_id")
gene_id_key = input("Enter the gene identifier key (gene_id or ID, default: gene_id): ").strip()
if gene_id_key not in ["gene_id", "ID"]:
    print("Invalid input. Using default: gene_id")
    gene_id_key = "gene_id"

# Ask user if they want to strip "gene:" prefixes
strip_prefix_input = input("Do you want to strip 'gene:' prefixes? (yes/no, default: no): ").strip().lower()
strip_prefix = strip_prefix_input == "yes"

# Read query gene list if provided
query_gene_list = None
if query_gene_list_file:
    with open(query_gene_list_file, 'r') as f:
        query_gene_list = set(line.strip() for line in f)

# Generate output file name based on input file names
anchors_base = os.path.splitext(os.path.basename(anchors_file))[0]
gff3_base = os.path.splitext(os.path.basename(gff3_file))[0]
output_file = f"{anchors_base}_{gff3_base}_output.tsv"

# Parse GFF3 with user-defined settings
gene_to_chr = parse_gff3(gff3_file, gene_id_key, strip_prefix)

# Process Anchors
output_results = process_anchors(anchors_file, gene_to_chr, query_gene_list)

# Save results to a TSV file
output_df = pd.DataFrame(output_results, columns=["Query_Gene", "Target_Gene", "Chromosome", "Score"])
output_df.to_csv(output_file, sep="\t", index=False)

print(f"Results saved to {output_file}")
