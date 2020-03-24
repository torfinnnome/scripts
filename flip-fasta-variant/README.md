# What

Reads a variant file with three values: Original amino acid, the position, and the replacement amino acid. It then reads a fasta file, replaces the amino acid, and outputs a new variant file.

# Requirements

[Python 3](https://www.python.org/) and [Biopython](https://biopython.org/).

# Example

## Input

```
test/proteins.txt:
protein1
```

```
test/protein1.fa:
>protein1
XXXXYXXXX

test/protein1.var:
Y5X
```

## Execute script

```
$ python flip-fasta-variant.py --seqs test/proteins.txt --vardir test --fastadir test --outvardir testout --outfastadir testout
```


## Output

```
testout/protein1.fa:
>protein1
XXXXXXXXX

testout/protein1.var:
X5Y

```
