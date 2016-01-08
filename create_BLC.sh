#!/usr/bin/bash

############################
wn_folder=wordnets
wn_version_folder=WordNet-3.0
url_wn=http://wordnetcode.princeton.edu/3.0/WordNet-3.0.tar.gz
wn_tgz=WordNet-3.0.tar.gz
#############################


if [ ! -d $wn_folder ];
then
  mkdir $wn_folder
fi
cd $wn_folder

wget $url_wn
tar xzf $wn_tgz
rm $wn_tgz

cd ..

if [ ! -d BLC ];
then
  mkdir BLC
fi

if [ -d BLC/$wn_version_folder ];
then
  rm -rf BLC/$wn_version_folder
fi

mkdir BLC/$wn_version_folder

for relation in all hypo
do
  echo "Creating BLC for $relation"
  mkdir BLC/$wn_version_folder/$relation
  for freq in 0 20 50
  do
    echo "  with frequency $freq ..."
    mkdir BLC/$wn_version_folder/$relation/$freq
    #python extract_blc_from_wordnet.py -i $wn_folder/$wn_version_folder/dict/data.noun -o BLC/$wn_version_folder/$relation/$freq/blc.noun -t $relation -m $freq -pos n
    #python extract_blc_from_wordnet.py -i $wn_folder/$wn_version_folder/dict/data.verb -o BLC/$wn_version_folder/$relation/$freq/blc.verb -t $relation -m $freq -pos v
    python extract_blc_from_wordnet_german.py -i $wn_folder/$wn_version_folder/dict/data.noun -o BLC/$wn_version_folder/$relation/$freq/blc.noun -t $relation -m $freq -pos n
    python extract_blc_from_wordnet_german.py -i $wn_folder/$wn_version_folder/dict/data.verb -o BLC/$wn_version_folder/$relation/$freq/blc.verb -t $relation -m $freq -pos v
 
  done
done

