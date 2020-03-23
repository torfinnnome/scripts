# What

Reads a variant file with three values: Original amino acid, the position, and the replacement amino acid. It then reads a fasta file, replaces the amino acid, and outputs a new variant file.

# Example

## Input

```
fasta/protein1.fa:
>protein1
XXXXYXXXX

var/protein1.var:
Y5X
```

## Output

```
fasta_mod/protein1.fa:
>protein1
XXXXXXXXX

var_mod/protein1.var:
X5Y

```
