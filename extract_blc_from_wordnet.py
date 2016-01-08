#!/usr/bin/env python
from collections import defaultdict
import argparse

def extract_synset(wn_line):
    p = wn_line.find(' ')
    return wn_line[:p]

def extract_num_relations_and_hyperonyms(wn_line, type_relations):
    p = wn_line.find('|')
    info = wn_line[:p]
    fields = info.split(' ')
    num_words = int(fields[3],16)  #It is hexadecimal
    position_pointer_count = 4 + 2*num_words
    num_relations = int(fields[position_pointer_count])
    
    this_position = position_pointer_count + 1
    hypo_relations = 0
    hyperonyms = []
    for r in xrange(num_relations):
        this_relation = fields[this_position]
        if this_relation == '~':
            hypo_relations += 1
        elif this_relation in ['@','@i']:
            hyperonyms.append(fields[this_position+1])
        this_position += 4
        
    
    if type_relations == 'all':
        pass
    elif type_relations == 'hypo':
        num_relations = hypo_relations
    
    return num_relations, hyperonyms

def get_max_hyperonym(list_hyperonyms, type_relations, wn_line_for_synset):
    best_hy = None
    best_num_rel = -1
    for hy in list_hyperonyms:
        wn_line = wn_line_for_synset[hy]
        num_relations, _ = extract_num_relations_and_hyperonyms(wn_line, type_relations)
        if num_relations > best_num_rel:
            best_num_rel = num_relations
            best_hy = hy
    return best_hy, best_num_rel

def extract_hyperonyms(best_hyperonym,wn_list_for_synset):
    wn_line = wn_list_for_synset[best_hyperonym]
    _, list_hyperonyms = extract_num_relations_and_hyperonyms(wn_line, 'all')
    return list_hyperonyms


def extract_blc(this_synset, wn_line_for_synset, type_relations, start_at_synset, show_log=False):
    this_blc = 'fake_blc'

    wn_line = wn_line_for_synset[this_synset]
    #print wn_line
    
    num_relations_for_synset, list_hyperonyms = extract_num_relations_and_hyperonyms(wn_line, type_relations)

    if show_log:
        print 'BLC for synset', this_synset, 'with %d relations' % num_relations_for_synset
    
    already_visited = set()
    if len(list_hyperonyms) == 0:
        this_blc = this_synset
    else:
        if show_log:
            print 'First level of hyperonyms:', list_hyperonyms
        best_hyperonym, best_num_relations_for_hyperonym = get_max_hyperonym(list_hyperonyms, type_relations, wn_line_for_synset)
        already_visited.add(best_hyperonym)
        if show_log:
            print 'Best syn and num relations:', best_hyperonym, best_num_relations_for_hyperonym
            
        if start_at_synset:
            previous = this_synset
        else:
            previous = None
        
        if show_log:
            print '  Starting iteration'
            
        while best_num_relations_for_hyperonym > num_relations_for_synset or (not start_at_synset and previous is None):
            if show_log:
                print '    Step'
            hyperonyms = extract_hyperonyms(best_hyperonym,wn_line_for_synset)
            if show_log:
                print '    Hyperonyms obtained for %s --> %s' % (best_hyperonym,str(hyperonyms))
            if len(hyperonyms) != 0:
                num_relations_for_synset = best_num_relations_for_hyperonym
                previous = best_hyperonym
                best_hyperonym, best_num_relations_for_hyperonym = get_max_hyperonym(hyperonyms, type_relations, wn_line_for_synset)
                if show_log:
                    print '      Best hyperonym and nu relations:',best_hyperonym, best_num_relations_for_hyperonym
                if best_hyperonym in already_visited:
                    #Cycle
                    if show_log:
                        print '       There is a cycle'
                    break
                already_visited.add(best_hyperonym)
            else:
                if show_log:
                    print '       There are no hyperonyms, so STOP'
                previous = best_hyperonym
                break
        
        this_blc = previous
            
    if show_log:
        print 'Synset: %s BLC %s' % (this_synset, this_blc)
        print
    return this_blc


def reassign_blc(this_blc, min_frequency,subsumed_by_blc,wn_line_for_synset,type_relations, show_log=False):
    subsumed = subsumed_by_blc[this_blc]
    if show_log:
        print 'Calculating new BLC for %s which subsumes %d synsets' % (this_blc, subsumed)
    already_visited = set()
    best_hyperonym = this_blc
    greatest_synset = None
    greatest_subsumed = -1
    while subsumed < min_frequency:
        this_wn_line = wn_line_for_synset[best_hyperonym]
        hyperonyms = extract_hyperonyms(best_hyperonym,wn_line_for_synset)
        if show_log:
            print '  Hyperonyms:', hyperonyms
        if len(hyperonyms) != 0:
            best_hyperonym, best_num_relations_for_hyperonym = get_max_hyperonym(hyperonyms, type_relations, wn_line_for_synset)
            if show_log:
                print '    Best hyperonym %s' % best_hyperonym
            if best_hyperonym in already_visited:
                if show_log:
                    print '    Already visited, we stop'
                break
            else:
                subsumed = subsumed_by_blc.get(best_hyperonym,0)
                if subsumed >= greatest_subsumed:
                    greatest_subsumed = subsumed
                    greatest_synset = best_hyperonym
                if show_log:
                    print '    This one subsumes: %d' % subsumed
            already_visited.add(best_hyperonym) 
        else:
            if show_log:
                print '   No hyperonyms, so we stop'
            if greatest_subsumed >= 0:  
                # we return the one with greatest number subsumed in the chain
                best_hyperonym = greatest_synset
            else:
                #We dont find any other BLC in the chain that subsumes the min
                # so we stay with the same as it was assigned
                best_hyperonym = this_blc
            break

    return best_hyperonym
        
    
def load_friendly_blc(path_to_sense_index):
    friendly_blc_for_synset_pos = {}
    fd = open(path_to_sense_index,'r')
    for line in fd:
        lexkey, synset, sense, freq = line.strip().split()
        p = lexkey.find('%')
        lemma = lexkey[:p]
        int_pos = lexkey[p+1]
        
        pos = None
        if int_pos == '1':
            pos = 'n'
        elif int_pos == '2':
            pos = 'v'
        
        if pos is not None:
            fr_blc = '%s.%s#%s' % (lemma,pos,sense)
            if (synset,pos) not in friendly_blc_for_synset_pos:
                friendly_blc_for_synset_pos[(synset,pos)] = (fr_blc,freq)
            else:
                _ , prev_freq =  friendly_blc_for_synset_pos[(synset,pos)]
                if freq > prev_freq:
                    friendly_blc_for_synset_pos[(synset,pos)] = (fr_blc,freq)
    fd.close()
    return friendly_blc_for_synset_pos
                    
                
            
    

if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(description='Extract BLC concepts from WordNet')
    argument_parser.add_argument('-i', type=argparse.FileType('r'), dest='fd_wn_data_file', help='Wordnet data file', required=True)
    argument_parser.add_argument('-o', type=argparse.FileType('w'), dest='fd_output', help='Output file', required=True)
    argument_parser.add_argument('-t', dest='type_relations', choices=['all','hypo'], help='Type of relations to consider', required=True)
    argument_parser.add_argument('-m', dest='min_frequency', type=int, help='Minimum number of synsets subsumed per BLC', required=True)
    argument_parser.add_argument('-log', dest='log', action='store_true', help='Show log')
    argument_parser.add_argument('-pos', dest='pos', choices=['n','v'], help='POS tag', required=True)
    argument_parser.add_argument('-start-at-synset', dest='start_at_synset', action='store_true', help='Start the iteration process at the synset itself')
    args = argument_parser.parse_args()

      
    wn_line_for_synset = {}
    for wn_line in args.fd_wn_data_file:
        if wn_line[0] != ' ':
            wn_line = wn_line.strip()
            synset = extract_synset(wn_line)
            wn_line_for_synset[synset] = wn_line
    
    blc_for_synset = {}
    subsumed_by_blc = defaultdict(int)
    
    
    #First selection of a BLC candidate for every synset
    for this_synset in wn_line_for_synset.keys():
        this_blc = extract_blc(this_synset, wn_line_for_synset, args.type_relations, args.start_at_synset, args.log)
        #print this_synset, '-->', this_blc
        blc_for_synset[this_synset] = this_blc
        subsumed_by_blc[this_blc] += 1


    #Filtering to make sure every BLC at least subsumes enough number
    reassigned = {}
    final_blc_for_synset = {}
    for this_synset, this_blc in blc_for_synset.items():
        subsumed = subsumed_by_blc[this_blc]
        if subsumed < args.min_frequency:
            new_blc = None
            if this_blc in reassigned:
                new_blc = reassigned[this_blc]
            else:
                new_blc = reassign_blc(this_blc,args.min_frequency,subsumed_by_blc,wn_line_for_synset, args.type_relations, args.log)
                reassigned[this_blc] = new_blc
                if args.log:
                    print 'Reassing blc to %s because %s only subsumes %d symsets' % (this_synset, this_blc, subsumed)
                    print '\tReassigned to: %s which subsumes %d synsets' % (new_blc, subsumed_by_blc[new_blc])
            final_blc_for_synset[this_synset] = new_blc
        else:
            final_blc_for_synset[this_synset] = this_blc
    
    path_to_data = args.fd_wn_data_file.name
    p = path_to_data.rfind('/')
    path_to_sense_index = path_to_data[:p+1]+'index.sense'
    friendly_blc_for_synset_pos = load_friendly_blc(path_to_sense_index)
    
    args.fd_output.write('### START PARAMETERS\n')
    for p, v in args._get_kwargs():
        if isinstance(v,file):
            v = v.name
        args.fd_output.write('### %s => %s\n' % (p,v))
    args.fd_output.write('### END PARAMETERS\n')

    
    for this_synset, this_blc in final_blc_for_synset.items():
        friendly, frequency = friendly_blc_for_synset_pos[(this_blc,args.pos)]
        args.fd_output.write('%s %s %s %d\n' % (this_synset, this_blc, friendly, subsumed_by_blc[this_blc]))
    
                
        
    args.fd_output.close()
    print 'Output in %s' % args.fd_output.name
                    
    args.fd_wn_data_file.close()
