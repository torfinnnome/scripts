#!/usr/bin/env python3

""" Reads a variant file with three values:
    Original amino acid, the position, and the replacement amino acid.
    It then reads a fasta file, replaces the amino acid, and outputs a new variant file."""

import argparse
import sys
import os
from Bio import SeqIO

def main():
    """Process input parameters, and consider doing the acual work"""
    parser = argparse.ArgumentParser(description='Flip amino acid in fasta file.')
    parser.add_argument('--seqs', required=True,
                        help='path to file with list of sequence IDs to process')
    parser.add_argument('--vardir', required=True,
                        help='path to input variation files')
    parser.add_argument('--fastadir', required=True,
                        help='path to input fasta files')
    parser.add_argument('--outvardir', required=True,
                        help='path to output variation files')
    parser.add_argument('--outfastadir', required=True,
                        help='path to output fasta files')

    args = parser.parse_args()

    sequences = get_seqs(args)
    process_fastas(sequences, args)


def get_seqs(args):
    """Read a file with all the fasta IDs to process"""
    try:
        with open(args.seqs) as f:
            sequences = f.read().splitlines()
            return(sequences)
    except:
        print("Error reading file with sequence IDs", args.seqs)
        sys.exit(1)


def process_fastas(sequences, args):
    """Flip the variants in each of the sequence files"""
    for seq in sequences:
        try:
            in_fasta = args.fastadir + '/' + seq + '.fasta'
            out_fasta = args.outfastadir + '/' + seq + '.fasta'            
            in_var = args.vardir + '/' + seq + '.var'
            out_var = args.outvardir + '/' + seq + '.var'

            if not os.path.exists(args.outfastadir):
                os.makedirs(args.outfastadir, exist_ok=True)
            if not os.path.exists(args.outvardir):
                os.makedirs(args.outvardir, exist_ok=True)

            # Process the variation files
            var = read_variation(in_var)
            write_variation(out_var, var)

            # Output fasta files
            process_fasta(in_fasta, out_fasta, var)

        except:
            print("Error processing fasta id", seq)
            sys.exit(1)


def read_variation(in_var):
    """Read the input variation file"""
    var = {}
    try:
        with open(in_var) as f:
                variation = f.readline().strip()
        var['aa_in'] = variation[0]
        var['aa_out'] = variation[-1]
        var['aa_position'] = int(variation[1:-1])
    except:
        print("Error reading input variation file")
        sys.exit(1)
    return(var)


def write_variation(out_var, var):
    """Write the flipped variation file"""
    try:
        with open(out_var, 'w') as f:
                output_string = var['aa_out'] + str(var['aa_position']) + var['aa_in']
                print(output_string, file=f)
    except:
        print("Error writing flipped variation file")
        sys.exit(1)
    return()


def process_fasta(in_fasta, out_fasta, var):
    """Read fasta file, and replace amino acid"""
    try:
        with open(in_fasta, "rU") as f:
            for record_in in SeqIO.parse(f, "fasta"):
                record_out = record_in

                aa_position = int(var['aa_position']) - 1
                aa_current = record_in.seq[aa_position]

                if aa_current == var['aa_in']:
                    record_out.seq = replace_string_pos(record_in.seq, aa_position, var['aa_out'])
                    SeqIO.write(record_out, out_fasta, "fasta")
                else:
                    print("Error: Amino acid mismatch detected: ", record_in.id)
                    sys.exit()

    except:
        print("Error occurd in process_fasta.")
        sys.exit(1)


def replace_string_pos(string, position, replace_with):
    """Replace character in string at position"""
    string = string[:position] + replace_with + string[position+1:]
    return(string)


if __name__ == "__main__":
    main()
