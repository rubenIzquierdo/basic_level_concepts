#!/usr/bin/env python

import argparse
import os
from collections import defaultdict

'''
XXX  number of different BLC
XXX average number of synset subsumed per different BLC
XXX average depth in the WordNet hierarchy
+ average polysemy in terms of BLC
XXX how many synsets are assigned to hthemlseves
'''


def calculate_depth_for_synset(synset,hyperonyms_for_sense, already_visited):
    if synset in already_visited:
        return 1
    these_hyperonyms = hyperonyms_for_sense[synset]
    if len(these_hyperonyms) == 0:
        #Base case, this is a root node
        return 1
    else:
        already_visited.append(synset)
        depths = [calculate_depth_for_synset(h,hyperonyms_for_sense,already_visited) for h in these_hyperonyms]
        avg_depth = sum(depths)*1.0/len(depths)
        return 1 + avg_depth



def load_hyperonyms(path_to_file):
    fd_data = open(path_to_file,'r')
    hyperonyms_for_synset = {}
    for wn_line in fd_data:
        if wn_line[0] != ' ':
            p = wn_line.find('|')
            info = wn_line[:p]
            fields = info.split(' ')
            synset = fields[0]
            num_words = int(fields[3],16)  #It is hexadecimal
            position_pointer_count = 4 + 2*num_words
            num_relations = int(fields[position_pointer_count])
            this_position = position_pointer_count + 1
            hyperonyms = []
            for r in xrange(num_relations):
                this_relation = fields[this_position]
                if this_relation in ['@','@i']:
                    hyperonyms.append(fields[this_position+1])
                this_position += 4
            hyperonyms_for_synset[synset] = hyperonyms
    fd_data.close()
    return hyperonyms_for_synset
                
def load_synsets_per_lemma(path_to_index,pos):
    synsets_for_lemma = defaultdict(list)
    fd = open(path_to_index,'r')
    for line in fd:
        #drum_out%2:41:00:: 02401809 1 1
        fields = line.strip().split(' ')
        p = fields[0].find('%')
        lemma = fields[0][:p]
        this_pos = fields[0][p+1]
        if (pos == 'n' and this_pos == '1') or (pos=='v' and this_pos=='2'):
            synsets_for_lemma[lemma].append(fields[1])            
    fd.close()
    return synsets_for_lemma
    
            
if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(description='Extract statistics from a set of BLC')
    argument_parser.add_argument('-bf', type=argparse.FileType('r'), dest='fd_blc', help='Path to BLC file',required=True)
    argument_parser.add_argument('-wn', dest='path_to_wn_dict', help='Path to WN dict file',required=True)
    argument_parser.add_argument('-pos', dest='pos', choices=['n','v'], help='PoS of the BLC file',required=True)
    
    args = argument_parser.parse_args()
    
    #Load the synset-> BLC
    synsets_per_blc = defaultdict(list)
    blc_for_synset = {}
    assigned_to_themselves = 0
    for line in args.fd_blc:
        if line[:2] != '##':
            fields = line.strip().split(' ')
            synset, synset_blc, friendly_blc, subsumed = fields
            if synset == synset_blc:
                assigned_to_themselves += 1
            subsumed = int(subsumed)
            synsets_per_blc[(synset_blc,friendly_blc)].append(synset)
            blc_for_synset[synset] = synset_blc
    args.fd_blc.close()

    n = T = 0
    maxV = minV = maxB = minB = None
    for (synset_blc,friendly_blc), subsumed in synsets_per_blc.items():
        n+=1
        T += len(subsumed)
        if minV is None or len(subsumed) < minV:
            minV = len(subsumed)
            minB = friendly_blc
        if maxV is None or len(subsumed) > maxV:
            maxV = len(subsumed)
            maxB = friendly_blc
            
    avg_subsumed = T*1.0/n
    
    ##################################################################
    ##Average depth
    #Calculate for eevery BLC, how many jumps till the root it has
    data_file = None
    if args.pos == 'n':
        data_file = os.path.join(args.path_to_wn_dict,'data.noun')
    elif args.pos == 'v':
        data_file = os.path.join(args.path_to_wn_dict,'data.verb')
                                            
    hyperonyms_for_sense = load_hyperonyms(data_file)
    total_depth = n = 0
    deepest_value = deepest_synset = shallowest_value = shallowest_synset = None
    for (synset_blc,friendly_blc), _ in synsets_per_blc.items():
        depth = calculate_depth_for_synset(synset_blc,hyperonyms_for_sense,[])
        if deepest_value is None or deepest_value < depth:
            deepest_value = depth
            deepest_synset = friendly_blc
        
        if shallowest_value is None or shallowest_value > depth:
            shallowest_value = depth
            shallowest_synset = friendly_blc
            
        total_depth += depth
        n += 1
    avg_depth = total_depth*1.0/n
    #############################################################################
    #############################################################################
    path_to_index = os.path.join(args.path_to_wn_dict,'index.sense')
    synsets_per_lemma = load_synsets_per_lemma(path_to_index,args.pos)
    total_synsets = total_blc = total_lemmas = total_lemmas_poly = total_synsets_poly = total_blc_poly = 0
    
    for lemma, list_synsets in synsets_per_lemma.items():
        total_lemmas += 1
        total_synsets += len(list_synsets)
        list_blc = [blc_for_synset[s] for s in list_synsets]
        total_blc += len(set(list_blc))
        if len(list_synsets) > 1:
            total_lemmas_poly += 1
            total_synsets_poly += len(list_synsets)
            total_blc_poly += len(set(list_blc))
        

    avg_poly_senses = total_synsets * 1.0 / total_lemmas
    avg_poly_blc = total_blc * 1.0 / total_lemmas
    
    avg_poly_senses_poly = total_synsets_poly * 1.0 / total_lemmas_poly
    avg_poly_blc_poly = total_blc_poly * 1.0 / total_lemmas_poly
    
    ##Avg polysemy in terms of BLC
    
    print
    print '#'*50
    print 'Number of different BLC: %d' % len(synsets_per_blc)
    print 'Number of synsets assigned to themselves: %d' % assigned_to_themselves
    print 'Avg subsumed per BLC: %.2f' % avg_subsumed
    print '\tMin num subsumed: %d by the BLC %s' % (minV,minB)
    print '\tMax num subsumed: %d by the BLC %s' % (maxV,maxB)
    print 'Avg depth for BLCs: %.2f' % avg_depth
    print '\tDeepest BLC: %s with a depth of %d' % (deepest_synset, deepest_value)
    print '\tMost shallow BLC: %s with a depth of %d' % (shallowest_synset, shallowest_value)
    print 'Avg polysemy on wordnet for lemmas for the pos %s' % args.pos
    print '\tMonosemous and polysemous: %d lemmas' % total_lemmas
    print '\t\tSense level: %.2f' % avg_poly_senses
    print '\t\t  BLC level: %.2f' % avg_poly_blc
    print '\tPolysemous: %d lemmas' % total_lemmas_poly
    print '\t\tSense level: %.2f' % avg_poly_senses_poly
    print '\t\t  BLC level: %.2f' % avg_poly_blc_poly
    
    print '#'*50

    
    