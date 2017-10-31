import csv
import logging
import re
from builtins import super

from phigaro.data import read_hmmer_output, read_genemark_output
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

        hmm_evalues = hmm_to_evalues(mgm_res, hmm_res)

        with open(self.output(), 'w') as of:
            writer = csv.writer(of, delimiter='\t')

            for scaffold, evalues in hmm_evalues:
                npn_it = (
                    'P' if e < max_evalue else 'P'
                    for e in evalues
                )
                writer.writerow((scaffold, ''.join(npn_it)))

