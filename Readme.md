# Phigaro: CLI tool for phage prediction
Phigaro is a scalable command-line tool for predictions phages and
prophages from nucleid acid sequences (including metagenomes).
It is based on phage genes HMMs and a smoothing window algorithm.

## Requirements
* **Python**: Python 2.7, Python 3+ versions are supported. 
`pip` utility is also required (`sudo apt-get install python-pip` on Ubuntu).


* **MetaGeneMark**: Download it from 
[http://topaz.gatech.edu/Genemark/license_download.cgi](http://topaz.gatech.edu/Genemark/license_download.cgi) 
and follow the instructions.

* **HMMER**: Download it from http://hmmer.org/

* **locate**: In order to install Phigaro, you need `locate`. 
It is present in the latest Ubuntu distributions, 
but in case you don't have it, install it with `sudo apt-get install locate` 

## Installation

```bash
$ sudo -H pip install phigaro
```
If you have other pip versions installed, use `pip2` or `pip3` instead of `pip`
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
  e_value_threshold: 0.00445  # Do not change this
phigaro:
  threshold_max: 8.827586  # Do not change this
  threshold_min: 7.058859  # Do not change this
  window_len: 32  # Do not change this
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
Getting help
```bash
$ phigaro -h  
usage: phigaro [-h] -f FASTA_FILE [-c CONFIG] [-o OUTPUT] [-t THREADS]
Phigaro is a scalable command-line tool for predictions phages and prophages                                                                                                                                                                        
from nucleid acid sequences

optional arguments:
  -h, --help            show this help message and exit
  -f FASTA_FILE, --fasta-file FASTA_FILE
                        Assembly scaffolds/contigs or full genomes, required
  -c CONFIG, --config CONFIG
                        Config file, not required
  -o OUTPUT, --output OUTPUT
                        Output file, not required, default is stdout
  -t THREADS, --threads THREADS
                        Num of threads (default is num of CPUs)
```
Searching prophages
```bash
$ phigaro -f Escherichia_coli_O157:H7_str._Sakai.fna
scaffold	begin	end 
>Escherichia_coli_O157:H7_str._Sakai	291589	317255
>Escherichia_coli_O157:H7_str._Sakai	881486	929292
>Escherichia_coli_O157:H7_str._Sakai	1042294	1075143
>Escherichia_coli_O157:H7_str._Sakai	1161297	1214167
>Escherichia_coli_O157:H7_str._Sakai	1242390	1312585
>Escherichia_coli_O157:H7_str._Sakai	1533217	1663713
>Escherichia_coli_O157:H7_str._Sakai	1755765	1806239
>Escherichia_coli_O157:H7_str._Sakai	1916035	1972127
>Escherichia_coli_O157:H7_str._Sakai	2154248	2251085
>Escherichia_coli_O157:H7_str._Sakai	2597642	2618313
>Escherichia_coli_O157:H7_str._Sakai	2666906	2713016
>Escherichia_coli_O157:H7_str._Sakai	2891705	2950968
>Escherichia_coli_O157:H7_str._Sakai	3476233	3498946
>Escherichia_coli_O157:H7_str._Sakai	5046510	5082381
```
Running time depends on the size of your input data and the number of CPUs used.
The mean running time for a fasta file with Escherichia coli O157:H7 (str. Sakai) genome is 207 seconds (with 1 thread used).

## Modus operandi
ORFs and corresponging proteins are predicted from the input .fasta file using MetaGeneMark. 
Phage genes are predicted with pVOG Hidden Markov Models 
that can be downloaded stand-alone from http://dmk-brain.ecn.uiowa.edu/pVOGs/. 
Each contig is represented as a sequence of phage and non-phage genes. 
A smoothing window algorithm determines regions with high density of phage genes 
and prophage boundaries.

In case of any questions regarding installing and running Phigaro 
please address [estarikova@rcpcm.org](mailto:estarikova@rcpcm.org)
or leave feedback on [Github issues page](https://github.com/lpenguin/phigaro/issues).

----
(C) E.Starikova, N.Pryanichnikov, 2017
