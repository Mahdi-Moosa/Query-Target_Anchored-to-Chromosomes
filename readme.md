# Extract Target Chromosomes

## Overview
This script extracts chromosome information from a GFF3 file for target genes listed in an MCScanX anchors file. It outputs a TSV file that includes:
- Query gene
- Target gene
- Chromosome number of the target gene
- Alignment score from the anchors file

## Features
- Skips comments in the anchors file (`#`-prefixed lines)
- Parses the GFF3 file to map genes to chromosomes
- Optionally filters results based on a user-provided list of query genes
- Saves results as a TSV file

## Requirements
- Python 3.x
- pandas

Install dependencies with:
```bash
pip install pandas
```

## Usage
Run the script and provide file paths when prompted:
```bash
python extract_target_chromosomes.py
```

### Input Files
1. **Anchors file** (e.g., `anchors.txt`)
    - Format: `query_gene target_gene score`
    - Example:
      ```
      qA tA1 150
      qA tA2 120
      qB tB1 200
      ```
    
2. **GFF3 file** (e.g., `target_genome.gff3`)
    - Contains genomic feature annotations, including genes and their chromosome locations.
    
3. **(Optional) Query Gene List** (e.g., `query_genes.txt`)
    - A text file with one gene per line.
    - If not provided, all query genes will be included.

### Output
A TSV file named `{anchors_base}_{gff3_base}_output.tsv` will be created, containing:
```
Query_Gene    Target_Gene    Chromosome    Score
qA            tA1           C5            150
qA            tA2           B5            120
qB            tB1           A1            200
```

## Notes
- If a query gene is missing from the provided list, it will be skipped.
- If a target gene has no chromosome mapping, "Unknown" will be recorded.

## License
MIT License.

