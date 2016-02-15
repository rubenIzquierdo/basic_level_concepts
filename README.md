#Basic Level Concepts#
Basic Level Concepts (BLC) are those concepts that are frequent and salient; they are neither overly general nor too specific.
BLC are a compromise between two conflicting principles of characterization:

+ to represent as many concepts as possible (abstract concepts)
+ to represent as many distinctive features as possible (concrete concepts).

We have developed a method for the automatic selection of BLC from WordNet.  We use a very simple method for deriving a small set
of appropriate meanings using basic structural properties of WordNet. The program considers:

+ The total number of relations of every synset or just the hyponymy relations.
+ Discard those BLCs that do not represent at least a number of synsets.

For more information about the BLCs and the extraction process, please check out the papers cited at the end of this documentation.

In this repository you can find both the sofware to extract BLC from the database files of WordNet, and the BLC already extracted
from WordNet 3.0.

##Extracting BLC##

To extract BLC you need to run the script `extract_blc_from_wordnet.py`, which has several parameters:
```shell
usage: extract_blc_from_wordnet.py [-h] -i FD_WN_DATA_FILE -o FD_OUTPUT -t
                                   {all,hypo} -m MIN_FREQUENCY [-log] -pos
                                   {n,v} [-start-at-synset]

Extract BLC concepts from WordNet

optional arguments:
  -h, --help          show this help message and exit
  -i FD_WN_DATA_FILE  Wordnet data file (path to data.noun or data.verb)
  -o FD_OUTPUT        Output file
  -t {all,hypo}       Type of relations to consider
  -m MIN_FREQUENCY    Minimum number of synsets subsumed per BLC
  -log                Show log
  -pos {n,v}          POS tag
  -start-at-synset    Start the iteration process at the synset itself
```

The `-start-at-synset` parameter sets whether to start the iteration process at the synset itself on at the first hyperonym. If we provide
this parameter, the process will start at the synset itself, and in some cases (if the criteria are satisfied) the synset could be selected
as its own BLC. If we do not provide this parameter, the iteration process will start at the first hyperonym.

For instance a valid call would be:
```shell
python extract_blc_from_wordnet.py -i wordnet3.0/dict/data.noun -o blc_wn30.txt -t all -m 20 -pos n
```

The format of the generated file `blc_wn30.txt` would be like:
```shell
### START PARAMETERS
### fd_output => blc_wn30.noun
### fd_wn_data_file => /home/izquierdo/wordnets/wordnet-3.0/dict/data.noun
### log => True
### min_frequency => 20
### pos => n
### start_at_synset => False
### type_relations => all
### END PARAMETERS
04958634 04916342 property.n#2 584
13253423 13252973 transferred_possession.n#1 32
02935387 03094503 container.n#1 603 
10725893 00007846 person.n#1 3783
12149144 12147226 bamboo.n#2 7
```

The lines at the beginning starting with `#` store the particular parameters that were used to generate the BLC in the file. There are four fields per line. The first field is the synset identifier, the second field is the synset identifier of the BLC assigned.
The third is a more friendly format for the BLC synset in field 2, and finally the last field is the number of synsets subsumed by this BLC.
For instance, the synset 10725893 which corresponds to fishpole_bamboo.n#1 or phyllostachys_aurea.n#1 is assigned with the BLC synset 12147226
which corresponds to bamboo.n#2 (the second sense of the lemma bamboo). This BLC subsumes 7 synsets.

You can also modify the script `create_BLC.sh` with the proper version of WordNet to generate automatically the BLC for other versions.

##BLC extracted##

BLC from WordNet 3.0, 2.1, 1.7.1 and 1.6 have been already generated and can be found in the folder `BLC/WordNet-VERSION`. In each case, there are two subfolders for the two types of
relations considered (all, hypo), and three subfolders for different values of the minimumn frequency (0,20,50).

##Related papers##

If you are interested in further information about the BLC you can read these publications. Please cite us if you make use of our BLCs.

+ Izquierdo R., Suarez A. and Rigau G. Exploring the Automatic Selection of Basic Level Concepts. Proceedings of the International Conference on Recent Advances on Natural Language Processing (RANLP'07), Borovetz, Bulgaria. September, 2007. [URL](http://hdl.handle.net/10045/2522) 
+ Izquierdo R., Suarez A. and Rigau G. An Empirical Study on Class-based Word Sense Disambiguation. Proceedings of the 12th Conference of the European Chapter of the Association for Computational Linguistics (EACL-09). Athens, Greece. 2009. [URL](http://dl.acm.org/citation.cfm?id=1609110)
+ Izquierdo R., Suaez A. and Rigau G. Word vs. Class-Based Word Sense Disambiguation. Journal of Artificial Intelligence Research. Volume 54, pages 83-122. 2015. [URL](http://jair.org/papers/paper4727.html)

##Contact##
* Ruben Izquierdo
* Vrije University of Amsterdam
* ruben.izquierdobevia@vu.nl  rubensanvi@gmail.com
* http://rubenizquierdobevia.com/
