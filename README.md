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
                                   {n,v}

Extract BLC concepts from WordNet

optional arguments:
  -h, --help          show this help message and exit
  -i FD_WN_DATA_FILE  Wordnet data file
  -o FD_OUTPUT        Output file
  -t {all,hypo}       Type of relations to consider
  -m MIN_FREQUENCY    Minimum number of synsets subsumed per BLC
  -log                Show log
  -pos {n,v}          POS tag
```

For instance a valid call would be:
```shell
python extract_blc_from_wordnet.py -i wordnet3.0/dict/data.noun -o blc_wn30.txt -t all -m 20 -pos n
```

The format of the generated file `blc_wn30.txt` would be like:
```shell
04958634 04916342 property.n#2 584
13253423 13252973 transferred_possession.n#1 32
02935387 03094503 container.n#1 603 
10725893 00007846 person.n#1 3783
12149144 12147226 bamboo.n#2 7
```

There are four fields per line. The first field is the synset identifier, the second field is the synset identifier of the BLC assigned.
The third is a more friendly format for the BLC synset in field 2, and finally the last field is the number of synsets subsumed by this BLC.
For instance, the synset 10725893 which corresponds to fishpole_bamboo.n#1 or phyllostachys_aurea.n#1 is assigned with the BLC synset 12147226
which corresponds to bamboo.n#2 (the second sense of the lemma bamboo). This BLC subsumes 7 synsets.

You can also modify the script `create_BLC.sh` with the proper version of WordNet to generate automatically the BLC for other versions.

##BLC extracted##

BLC from WordNet 3.0 have been already generated and can be found in the folder `BLC/wordnet_3.0`. There are two subfolders for the two types of
relations considered (all, hypo), and three subfolders for different values of the minimumn frequency (0,20,50).

##Related papers##

If you are interested in further information about the BLC you can read these publications. Please cite us if you make use of our BLCs.

+ Izquierdo R., Su�rez A. and Rigau G. Exploring the Automatic Selection of Basic Level Concepts. Proceedings of the International Conference on Recent Advances on Natural Language Processing (RANLP'07), Borovetz, Bulgaria. September, 2007. 
+ Izquierdo R., Su�rez A. and Rigau G. An Empirical Study on Class-based Word Sense Disambiguation. Proceedings of the 12th Conference of the European Chapter of the Association for Computational Linguistics (EACL-09). Athens, Greece. 2009.
+ Izquierdo R., Su�rez A. and Rigau G. Word vs. Class-Based Word Sense Disambiguation.Journal of Artificial Intelligence Research. Volume 54, pages 83-122. 2015.

##Contact##
* Ruben Izquierdo
* Vrije University of Amsterdam
* ruben.izquierdobevia@vu.nl  rubensanvi@gmail.com
* http://rubenizquierdobevia.com/

