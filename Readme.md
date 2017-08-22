# Phigaro: CLI tool for predictions phages
Phigaro is a scalable command-line tool for predictions phages and
prophages from nucleid acid sequences (including metagenomes).
It is based on phage genes HMMs and a smoothing window algorithm.

## Requirements
* **Python.** Python 2.7, Python 3+ versions are supported. 
`pip` utility is also required (`sudo apt-get install python-pip` on Ubuntu).


* **MetaGeneMark.** Download it from 
[http://topaz.gatech.edu/Genemark/license_download.cgi](http://topaz.gatech.edu/Genemark/license_download.cgi) 
and follow the instructions.

* **HMMER** Download it from http://hmmer.org/

## Installation

```bash
$ sudo -H pip install phigaro
```

## Configuration

### Simplified, via `phigaro-setup` tool
In order to simplify setup process, you can run `phigaro-setup` tool.
It will locate all needed software and download data.
Example:
```bash
$ phigaro-setup
[sudo] password for user:
Found MetaGeneMark in: /home/user/software/MetaGeneMark_linux_64/mgm/gmhmmp
Found MetaGeneMark model in: /home/user/software/MetaGeneMark_linux_64/mgm/MetaGeneMark_v1.mod
Found HMMER in: /home/user/software/hmmer-3.1b2-linux-intel-x86_64/binaries/hmmsearch
HMMER model in: /home/user/.phigaro/pvog/allpvoghmms
Downloading models to /home/user/.phigaro/pvog
Downloading http://download.ripcm.com/phigaro/allpvoghmms to /home/user/.phigaro/pvog/allpvoghmms
Downloading http://download.ripcm.com/phigaro/allpvoghmms.h3f to /home/user/.phigaro/pvog/allpvoghmms.h3f
Downloading http://download.ripcm.com/phigaro/allpvoghmms.h3i to /home/user/.phigaro/pvog/allpvoghmms.h3i
Downloading http://download.ripcm.com/phigaro/allpvoghmms.h3m to /home/user/.phigaro/pvog/allpvoghmms.h3m
Downloading http://download.ripcm.com/phigaro/allpvoghmms.h3p to /home/user/.phigaro/pvog/allpvoghmms.h3p
```

### Manual
Create configuration file `~/.phigaro/config.yml` with following content:
```yaml
genemark:
  # Path to MetaGeneMark binary
  bin: /home/user/software/MetaGeneMark_linux_64/mgm/gmhmmp
  # Path to MetaGeneMark models
  mod_path: /home/user/software/MetaGeneMark_linux_64/mgm/MetaGeneMark_v1.mod
hmmer:
  # Path to HMMER hmmsearch binary
  bin: /home/user/software/hmmer-3.1b2-linux-intel-x86_64/binaries/hmmsearch
  # HMMER models, usually: ~/.phigaro/pvog/allpvoghmms
  pvog_path: /home/user/.phigaro/pvog/allpvoghmms
  e_value_threshold: 1.0e-05  # Do not change this
phigaro:
  threshold_max: 7.571429  # Do not change this
  threshold_min: 5.341108  # Do not change this
  window_len: 34  # Do not change this
```

Run `phigaro-setup` to download models data: 
```bash
$ phigaro-setup
Phigaro already configured
Downloading models to /home/user/.phigaro/pvog
Downloading http://download.ripcm.com/phigaro/allpvoghmms to /home/user/.phigaro/pvog/allpvoghmms
Downloading http://download.ripcm.com/phigaro/allpvoghmms.h3f to /home/user/.phigaro/pvog/allpvoghmms.h3f
Downloading http://download.ripcm.com/phigaro/allpvoghmms.h3i to /home/user/.phigaro/pvog/allpvoghmms.h3i
Downloading http://download.ripcm.com/phigaro/allpvoghmms.h3m to /home/user/.phigaro/pvog/allpvoghmms.h3m
Downloading http://download.ripcm.com/phigaro/allpvoghmms.h3p to /home/user/.phigaro/pvog/allpvoghmms.h3p
```
or manually download data from [http://download.ripcm.com/phigaro/](http://download.ripcm.com/phigaro/)
## Usage

```bash
$ phigaro -h                                                                                                                                                                          15:04:32
usage: phigaro [-h] [-f FASTA_FILE] [-c CONFIG] [-v] [-t THREADS]
optional arguments:
  -h, --help            show this help message and exit
  -f FASTA_FILE, --fasta-file FASTA_FILE
                        Assembly scaffolds\contigs or full genomes
  -c CONFIG, --config CONFIG
                        config file, not required
  -v, --verbose
  -t THREADS, --threads THREADS
                        num of threads (default is num of CPUs)
```

Running time depends on the size of your input data and the number of CPUs used.
The mean running time for a fasta file of 10MB is ~5 minutes.
----
(C) N.Pryanichnikov, E.Starikova, 2017