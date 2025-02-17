# Extract Target Chromosomes

## Overview
This script extracts chromosome information from a GFF3 file for target genes listed in an MCScanX anchors file.  
It outputs a TSV file that includes:
- Query gene
- Target gene
- Chromosome number of the target gene
- Alignment score from the anchors file

## Features
- Skips comments in the anchors file (`#`-prefixed lines)
- Parses the GFF3 file to map genes to chromosomes
- **User-defined gene identifier** (supports both `gene_id=` and `ID=`)
- **Optional stripping of "gene:"** prefixes in gene names
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

### **User Inputs**
When running the script, you will be prompted to:
1. **Enter the Anchors File** (e.g., `anchors.txt`)
2. **Enter the GFF3 File** (e.g., `target_genome.gff3`)
3. **(Optional) Enter the Query Gene List** (or press Enter to include all query genes)
4. **Choose the Gene Identifier Key** (`gene_id` or `ID`, default: `gene_id`)
5. **Enable or Disable "gene:" Stripping** (`yes` to remove it, `no` to keep it)

---

### **Input Files**
#### **1. Anchors File (e.g., `anchors.txt`)**
- Format: `query_gene target_gene score`
- Example:
  ```
  qA tA1 150
  qA tA2 120
  qB tB1 200
  ```

#### **2. GFF3 File (e.g., `target_genome.gff3`)**
- Contains genomic feature annotations, including genes and their chromosome locations.
- Example:
  ```
  1    oge    gene    1816    9281    .    +    .    ID=gene:OPUNC01G00010;gene_id=OPUNC01G00010;biotype=protein_coding
  ```

#### **3. (Optional) Query Gene List (e.g., `query_genes.txt`)**
- A text file with one gene per line.
- If not provided, all query genes will be included.

---

### **Output**
A TSV file named `{anchors_base}_{gff3_base}_output.tsv` will be created, containing:
```
Query_Gene    Target_Gene    Chromosome    Score
qA            tA1           C5            150
qA            tA2           B5            120
qB            tB1           A1            200
```

### **How Unknown Chromosomes Are Handled**
- If a **target gene** is missing in the GFF3 file, `"Unknown"` is recorded in the Chromosome column.
- If **gene ID formats differ** (e.g., `gene:OPUNC01G00010` vs. `OPUNC01G00010`), use the `"strip gene:"` option.

---

## **Example Run**
```
Enter the anchors file path: anchors.txt
Enter the GFF3 file path: target_genome.gff3
Enter the query gene list file (or press Enter to use all genes): (press Enter)
Enter the gene identifier key (gene_id or ID, default: gene_id): ID
Do you want to strip 'gene:' prefixes? (yes/no, default: no): yes
```
**Example Output File (`anchors_target_genome_output.tsv`)**
```
Query_Gene    Target_Gene    Chromosome    Score
LOC4326813    OPUNC01G00010    1            3100
LOC4326455    OPUNC01G00020    1            2650
LOC112163591  OPUNC01G00030    Unknown      2360
```

---

## **Notes**
- If a **query gene** is missing from the provided list, it will be skipped.
- If a **target gene has no chromosome mapping**, `"Unknown"` will be recorded.
- The script **automatically adapts** to different GFF3 formats by allowing user choices.

---

## **License**
MIT License.

