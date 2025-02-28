
from parent_strategy import ParentStrategy
from CollectiveImpurityGini import CollectiveImpurityGini
from CollectiveImpurityEntropy import CollectiveImpurityEntropy
from treenode import TreeNode
from config import PIVOTS
from config import PIVOTS_O
from record import Record
from pathlib import Path

import csv
import os


def open_file(filename):

    '''
    copied from hw5
    added encoding =utf-8 from hw5 utils
    '''
    with open(filename, "r", encoding='utf-8-sig') as file:
        rows = list(csv.reader(file))
    
    labels = rows.pop(0)
    #labels[0] = "ID"

    records = []
    swaps = {"TRUE": True, "FALSE": False, "Male": True, "Female": False, "High Risk": True, "Low Risk": False}
    for i in range(0, len(rows)):
        row = {}
        for j in range(len(rows[i])):
            if rows[i][j] in swaps:
                val = swaps[rows[i][j]]
            elif rows[i][j].isdigit():
                val = int(rows[i][j])
            else:
                '''
                added a little error checking that i didn't have in hw5
                '''
                raise ValueError("bad value in csv")
            row.update({labels[j]: val})
        records.append(Record(row, row["Assessment"]))
    return records, labels


def open_file_in_folder(foldername, filename):
    '''
    also copied from hw5
    '''

    current_directory = Path(__file__).parent

    folder_path = current_directory / foldername
    os.chdir(folder_path)
    return open_file(filename)


def make_partition(record_list, lam):

    '''
    simple split function implemented as described in the insturctions
    '''
    left_split = []
    right_split = []
    for record in record_list:
        if lam(record):
            left_split.append(record)
        else:
            right_split.append(record)

    return [left_split, right_split]

def subdivide_ordinal_data(records, pivots, category, subtensions):
    vals = []
    for record in records:
        vals.append(record.attrs[category])
    r = max(vals) - min(vals)
    increment = r * subtensions
    n_increments = int(max(vals) // increment) - 1
    

    minimum = min(vals)
    l_b = minimum
    u_b = minimum + increment
    for i in range(n_increments):
        '''
        had to eliminate the overlapping boundaries to increase efficiency
        because the number of permutations was putting me into
        the bad part of the exponential time curve

        also was having issues interpreting overlapping boundaries as multiple
        lambdas would ping true, indicating the whole range was significant,
        when clearly only the first half was when testing with only one lambda
        '''
        # for j in range(i + 1, n_increments + 1):
        #     l_b = minimum + increment * i
        #     u_b = l_b + increment * (j - i)
        #     pivots.update({f"{category}_{l_b}_{u_b}": lambda x: l_b <= x.attrs[category] <= u_b})
        l_b = minimum + increment * i
        u_b = minimum + increment * (i + 1)
        pivots.update({f"{category}_{l_b}_{u_b}": lambda x: l_b <= x.attrs[category] <= u_b})
    return pivots




def find_best_partition(record_list, strategy, max_depth = 3, pivots = PIVOTS, target = "Assessment", invert = False):

    '''
    Was having trouble simply returning the optimal combination up the tree,
    so i decided to just have it return evey possible combination and then select the
    best one at the root.

    target="Assessment" defaults to finding the lowest entropy combination for
    risk level. However, I modified the program to change this to find the lowest
    entropy combination for any boolean variable

    decided to do this as a recursive function as it made the most sense to me given
    what we've done in the past. Also didn't know if the order of the partitions mattered
    for the outcome. It doesn't seem to -- like cutting a pie, it doesn't matter
    which way you cut first as long as the slices end up being the same size in the end

    so i could make this function much more efficient by not doing every permutation
    of partition. maybe next time
    '''

    def recurse(record_list, 
                strategy,
                max_depth,
                pivots, 
                target,
                invert, 
                seq = [], 
                depth = 0, 
                outcomes = {}):

        if len(record_list) == 0:
            return outcomes
        else:
            depth += 1
            x = strategy.compute(strategy, record_list, target, invert)
            if x != 0 and len(seq) > 0 and depth < max_depth:
                outcomes.update({x: seq})

            partitions = {}
            for pivot in pivots:
                new = []
                if pivot != target and pivot not in seq:
                    #make treenode
                    new = make_partition(record_list, pivots[pivot])
                    for i in range(2):
                        if i == 0:
                            dir = True
                        elif i == 1:
                            dir = False
                        partitions.update({pivot + f"{i}": {"list": new[i], "dir": dir}})

            for partition in partitions:
                outcomes_next = recurse(partitions[partition]["list"], strategy, max_depth, pivots, target, invert, 
                                    seq + [partition[:-1]] + [partitions[partition]["dir"]],
                                    depth, outcomes)
                # outcomes.update(outcomes_next)
            return outcomes
    

    outcomes = recurse(record_list, strategy, max_depth, pivots, target, invert)
    minimum = min(outcomes)
    
    return minimum, outcomes[minimum]


def main():
    records, labels = open_file_in_folder("data", "ICE6TrainingDataFile.csv")
    
    root = TreeNode(records,
                    CollectiveImpurityGini, 
                    1000, 
                    PIVOTS, 
                    target="Assessment", 
                    invert=False, 
                    parent_pivot="ROOT", 
                    score=CollectiveImpurityGini.compute(records, 
                                                         "Assessment", 
                                                         invert=False))
    
    new_records, labels = open_file_in_folder("data", "test_data.csv")

    '''
    CLASSIFYING NEW RECORDS
    '''
    for new_record in new_records:
        x = root.classify(new_record)
        if x > 0:
            x = True
        else:
            x = False
        new_record.predicted_label = x
    

    '''
    SCORING THE NEW RECORDS
    '''
    score = 0
    for new_record in new_records:
        #print(new_record.predicted_label, new_record.attrs["Assessment"])
        if new_record.predicted_label == new_record.attrs["Assessment"]:
            score += 1
    print("MORE NOISY TRAINING DATA")
    print("raw score", score)
    score = score / len(new_records)

    print(score)

    less_noisy_records, labels = open_file_in_folder("data", "training_data_more_noise-1.csv")

    root2 = TreeNode(less_noisy_records,
                    CollectiveImpurityGini, 
                    1000, 
                    PIVOTS, 
                    target="Assessment", 
                    invert=False, 
                    parent_pivot="ROOT", 
                    score=CollectiveImpurityGini.compute(records, 
                                                         "Assessment", 
                                                         invert=False))
    
    '''
    CLASSIFYING NEW RECORDS
    '''
    for new_record in new_records:
        x = root2.classify(new_record)
        if x > 0.5:
            x = True
        else:
            x = False
        new_record.predicted_label = x
    

    '''
    SCORING THE NEW RECORDS
    '''
    score = 0
    for new_record in new_records:
        #print(new_record.predicted_label, new_record.attrs["Assessment"])
        if new_record.predicted_label == new_record.attrs["Assessment"]:
            score += 1
    print("LESS NOISY TRAINING DATA")
    print("RAW SCORE", score)
    score = score / len(new_records)

    print(score)



if __name__ == "__main__":
    main()