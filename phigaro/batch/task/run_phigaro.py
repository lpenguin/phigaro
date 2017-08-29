from builtins import super
import csv
from itertools import groupby

from phigaro.data import convert_npn, read_genemark_output
from phigaro.finder.v2 import V2Finder
from .base import AbstractTask
from .parse_hmmer import ParseHmmerTask
from .gene_mark import GeneMarkTask


class RunPhigaroTask(AbstractTask):
    task_name = 'run_phigaro'

    def __init__(self, parse_hmmer_task, gene_mark_task):
        """

        :type parse_hmmer_task: ParseHmmerTask
        :type gene_mark_task: GeneMarkTask
        """
        super().__init__()
        self.hmmer_task = parse_hmmer_task
        self.gene_mark_task = gene_mark_task

    def _prepare(self):
        self.finder = V2Finder(
            window_len=self.config['phigaro']['window_len'],
            threshold_min=self.config['phigaro']['threshold_min'],
            threshold_max=self.config['phigaro']['threshold_max'],
        )

    def output(self):
        return self.file('{}.tsv'.format(self.sample))

    def run(self):
        scaffold_genes_coords = read_genemark_output(self.gene_mark_task.output())

        with open(self.output(), 'w') as of:
            writer = csv.writer(of, delimiter='\t')

            with open(self.hmmer_task.output()) as f:
                reader = csv.reader(f, delimiter='\t')

                writer.writerow(('scaffold', 'begin', 'end'))
                for scaffold, npn_str in reader:
                    genes_coords = scaffold_genes_coords[scaffold]

                    npn = convert_npn(npn_str, 'P')
                    phages = self.finder.find_phages(npn)
                    for phage in phages:
                        begin = genes_coords[phage.begin][0]
                        end = genes_coords[phage.end][1]
                        writer.writerow((scaffold, begin, end))

