# Extract Target Chromosomes and Process Anchors

## Overview
This repository contains scripts for extracting chromosome information from a GFF3 file for target genes,  
combining **anchor** and **lifted anchor** files from **MCScan outputs**, and grouping data for further analysis.

✅ The **anchor** and **lifted anchor** files should come from **MCScan** output.  
✅ These scripts have been tested with **MCScan for Python (jcvi)**.  
✅ They **should** work with **MCScanX** outputs as well, but this has not been tested.

---

## **Scripts Included**
1. **`extract_target_chromosomes.py`** → Extracts chromosome information from a GFF3 file.
2. **`combine_anchors.py`** → Merges **anchor** and **lifted anchor** files, linking `Query_Gene` to both.
3. **`group_anchors.py`** → Groups data by `Query_Gene`, removing `"NA"` values and producing lists of tuples.

---

## **1. Extract Target Chromosomes**
This script extracts chromosome information from a **GFF3 file** for target genes listed in an **MCScanX/JCVI anchors file**.

### **Features**
✅ Skips comments in the anchors file (`#`-prefixed lines)  
✅ Parses the GFF3 file to map genes to chromosomes  
✅ Supports **user-defined gene identifiers** (`gene_id=` or `ID=`)  
✅ Optionally **removes** `"gene:"` prefixes from gene names  
✅ Can **filter results** based on a user-provided list of query genes  
✅ Saves results as a **TSV file**  

### **Usage**
Run interactively:
```bash
python extract_target_chromosomes.py
```
OR specify files using arguments:
```bash
python extract_target_chromosomes.py -a anchors.txt -g genome.gff3
```

#### **Output Format**
```
Query_Gene    Target_Gene    Chromosome    Score
qA            tA1           C5            150
qA            tA2           B5            120
qB            tB1           A1            200
```

---

## **2. Combine Anchor and Lifted Anchor Files**
This script **merges** **MCScan (JCVI or MCScanX)** **anchor and lifted anchor files**, linking `Query_Gene` to both.

### **Features**
✅ Reads **both anchor and lifted anchor files**  
✅ Looks up **chromosome mappings** from a GFF3 file  
✅ Outputs a TSV file combining information from both sources  
✅ Supports **command-line arguments and interactive input**  

### **Usage**
```bash
python combine_anchors.py -a anchor.txt -l lifted_anchor.txt -g genome.gff3
```
OR run interactively:
```bash
python combine_anchors.py
```

### **Output Format**
```
Query_Gene	Target_Gene-Anchor	Chromosome-Anchor	Score-Anchor	Target_Gene-LiftedAnchor	Chromosome-LiftedAnchor	Score-LiftedAnchor
LOC107275246	OMIW190G07916	C1	506	OMIW190G02023	B1	144L
LOC107275246	NA	NA	NA	OMIW190G02022	B1	109L
LOC107275248	OMIW190G014393	B2	452	OMIW190G019179	C2	226L
```
🔹 **NA values are preserved** if no corresponding match exists.

---

## **3. Group Anchors by Query Gene**
This script **groups anchor data by `Query_Gene`**, aggregating **target genes and chromosomes** into lists of tuples. The input file here is the output of the **step 2 (the combined anchor-lifted anchor output from combine_anchors.py)**.

### **Features**
✅ Groups **all entries by `Query_Gene`**  
✅ Aggregates **target genes & chromosomes** into **lists of tuples**  
✅ **Removes `"NA"` values**  
✅ **Filters by a subset of query genes** if specified  
✅ **Automatically names output files** unless a custom name is given  

### **Usage**
#### **1. Process All Genes (Auto-Named Output)**
```bash
python group_anchors.py -i combined_output.tsv
```
✅ Saves to:  
```
grouped_combined_output.tsv
```

#### **2. Process a Subset of Genes**
```bash
python group_anchors.py -i combined_output.tsv -q query_genes.txt
```
✅ Saves to:  
```
grouped_filtered_combined_output.tsv
```

#### **3. Specify a Custom Output File**
```bash
python group_anchors.py -i combined_output.tsv -o my_output.tsv -q query_genes.txt
```
✅ Saves to `my_output.tsv`.

### **Output Format**
```
Query_Gene	Target_Gene-Anchor	Target_Gene-LiftedAnchor
LOC107275246	[('OMIW190G07916', 'C1')]	[('OMIW190G02023', 'B1'), ('OMIW190G02022', 'B1'), ('OMIW190G07916', 'C1')]
LOC107275248	[('OMIW190G014393', 'B2')]	[('OMIW190G014393', 'B2'), ('OMIW190G019179', 'C2')]
```

---

## **Installation**
Requires **Python 3.x** and `pandas`. Install dependencies with:
```bash
pip install pandas
```

---

## **Notes**
🔹 **Anchor and lifted anchor files should come from MCScan (JCVI or MCScanX).**  
🔹 If a **query gene** is missing from the provided list, it will be skipped.  
🔹 **"NA" values are automatically removed** when grouping anchor data.  
🔹 The script **automatically adapts** to different input formats.  

---

## **License**
MIT License.
