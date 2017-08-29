import csv
import logging
import re
from builtins import super
from itertools import groupby

from phigaro.data import read_hmmer_output, read_genemark_output
from phigaro.misc.ranges import first
from .base import AbstractTask
from .gene_mark import GeneMarkTask
from .hmmer import HmmerTask

logger = logging.getLogger(__name__)

INFINITY = float('inf')


class ParseHmmerTask(AbstractTask):
    task_name = 'parse_hmmer'

    def __init__(self, hmmer_task, gene_mark_task):
        """

        :type hmmer_task: HmmerTask
        :type gene_mark_task: GeneMarkTask
        """
        super().__init__()
        self.hmmer_task = hmmer_task
        self.genemark_task = gene_mark_task

    def output(self):
        return self.file('{}.npn'.format(self.sample))

    def run(self):
        self._parse_hmmer_output()

    @staticmethod
    def parse_line(line):
        tokens = re.split(r'\s+', line)
        scaffold = '>' + line.split('>')[1]
        name = tokens[0]
        evalue = float(tokens[4])
        return scaffold, name, evalue

    def _parse_hmmer_output(self):
        max_evalue = self.config['hmmer']['e_value_threshold']

        hmm_res = read_hmmer_output(self.hmmer_task.output())
        mgm_res = read_genemark_output(self.genemark_task.output())

        with open(self.output(), 'w') as of:
            writer = csv.writer(of, delimiter='\t')

            for scaffold, coords_names in sorted(mgm_res.items(), key=first):
                if scaffold not in hmm_res:
                    continue
                scaffold_res = hmm_res[scaffold]

                is_phage_it = (
                    scaffold_res.get(gene_name[1:], INFINITY) <= max_evalue
                    for begin, end, gene_name in coords_names
                )

                is_phage_it = (
                    'P' if is_phage else 'N'
                    for is_phage in is_phage_it
                )
                writer.writerow((scaffold, ''.join(is_phage_it)))

