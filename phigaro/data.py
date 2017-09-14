import csv
import re
from itertools import groupby

from phigaro.misc.ranges import first, second
INFINITY = float('inf')


def read_npn(filename, sep=None, as_dict=True):
    sep = sep or ' '
    with open(filename) as f:
        reader = csv.reader(f, delimiter=sep)
        if as_dict:
            return dict(reader)
        else:
            return reader


def read_coords(filename, sep=None):
    sep = sep or '\t'
    with open(filename) as f:
        reader = csv.reader(f, delimiter=sep)
        res = {}
        for phage, group in groupby(reader, key=lambda x: x[0]):
            res[phage] = sorted((
                (int(begin), int(end))
                for _, begin, end in group
            ), key=lambda x: x[0])
    return res


def convert_npn(phage, ph_sym):
    return [
        int(c == ph_sym)
        for c in phage
    ]


def read_hmmer_output(file_path):
    """
    :type file_path: str
    :rtype: dict[str: list[float]]

    :returns Dictionary: scaffold-> list of evalues
    """

    def parse_line(line):
        tokens = re.split(r'\s+', line)
        scaffold = '>' + line.split('>')[1]
        name = tokens[0]
        evalue = float(tokens[4])
        return scaffold, name, evalue

    with open(file_path) as f:
        lines_it = (
            parse_line(line.strip())
            for line in f
            if not line.startswith('#') and line.strip()
        )

        hmm_res = {}
        for scaffold, gene_name, evalue in lines_it:
            if scaffold not in hmm_res:
                hmm_res[scaffold] = {}
            # Take minimum of all evalues for current gene_name
            if gene_name in hmm_res[scaffold]:
                hmm_res[scaffold][gene_name] = min(evalue, hmm_res[scaffold][gene_name])
            else:
                hmm_res[scaffold][gene_name] = evalue

        return hmm_res


def read_genemark_output(file_name):
    """

    :type file_name: str
    :rtype: dict[str, list[tuple[int, int, str]]]

    :returns Dictionary scaffold -> list of tuples (begin, end, gene_name)
    """
    def extract_coords_and_name(gene_str):
        tokens = gene_str.split('|')
        return int(tokens[-2]), int(tokens[-1]), gene_str

    with open(file_name) as f:
        genes_scaffolds = (
            line.strip().split('\t')
            for line in f
            if line.startswith('>')
        )

        return {
            scaffold: [extract_coords_and_name(gene_str) for gene_str, _ in scaffold_gene_strs]
            for scaffold, scaffold_gene_strs in groupby(genes_scaffolds, key=second)
        }


def hmm_to_evalues(mgm_res, hmm_res):
    """
    :type mgm_res: dict[str, list[tuple[int, int, str]]]
    :type hmm_res: dict[str: list[float]]
    """
    for scaffold, coords_names in sorted(mgm_res.items(), key=first):
        if scaffold not in hmm_res:
            continue
        hmm_scaffold_res = hmm_res[scaffold]

        evalues_it = [
            hmm_scaffold_res.get(gene_name[1:], INFINITY)
            for begin, end, gene_name in coords_names
        ]

        yield (scaffold, evalues_it)
