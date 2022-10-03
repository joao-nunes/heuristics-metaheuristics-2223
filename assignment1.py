import os
import time
import numpy as np
from copy import deepcopy
import pandas as pd

np.random.seed(58)

def load_instance(
    source: str ="C://Users//jdffn//OneDrive//Documentos//Instances//SCP-Instances//",
    instance: str ='scpd5.txt'
):
    with open(os.path.join(source, instance)) as f:
        data = f.readlines()
        
    return data
  
def ch1(universe, attributes, costs, del_redundancy=True):
    
    cost=0
    
    covered = list()
    
    cover = list()
    
    set_of_subsets = dict()
    
    while not all(item in covered for item in universe):
        
        # select an uncovered attribute
        for j in universe:
            if not j in covered:
                covered.append(j)
                break
                
        # select a random subset that covers the attribute
        if attributes[j-1] == []:
            covered.append(j)
            continue
        subset = np.random.choice(attributes[j-1])
        # add the selected subset to the set of subsets
        set_of_subsets[str(subset)] = [j]
        # append to covered all the attributes covered by the selected subset
        for i in universe:
            if subset in attributes[i-1]:
                covered.append(i)
                set_of_subsets[str(subset)].append(i)
        # store the selected subset
        cover.append(subset)
        cost += costs[subset-1]
        
    if del_redundancy:
        # list of redundant subsets
        redundant = []
        # iterate over the set of subsets
        for i, set1 in enumerate(list(set_of_subsets.keys())):
            # compare current position with all others
            flags = [False for elem in set_of_subsets[set1]]
            for j, set2 in enumerate(list(set_of_subsets.keys())[i+1:]):
                for k, elem in enumerate(set_of_subsets[set1]):
                    if elem in set_of_subsets[set2]:
                        flags[k]=True
            # if all elements of subset1 covered in other subsets, append subset1 to redundant
            if all(flags)==True:
                redundant.append(set1)
            
        for elem in redundant:
            # remove the redundant sets from the set_of_subsets
            del set_of_subsets[elem]
            # update the cost
            cost-=costs[int(elem)-1]
            # remove the set from the list of selected subsets
            cover.remove(int(elem))
    return set_of_subsets, cover, cost

  
def ch2(universe, attributes, costs, del_redundancy=True):
    
    cost=0
    
    covered = list()
    
    cover = list()
    set_of_subsets = dict()
    
    while not all(item in covered for item in universe):
        
        
        # select an uncovered attribute
        for j in universe:
            if not j in covered:
                covered.append(j)
                break
                
        # select the subset with the least cost that covers the attribute
        if attributes[j-1] == []:
            covered.append(j)
            continue
        subset = attributes[j-1][0]
        
        cmin = costs[subset-1]
        for sub in attributes[j-1]:
            if costs[sub-1] < cmin:
                cmin = costs[sub-1]
                subset = sub
        # add the selected subset to the set of subsets
        set_of_subsets[str(subset)] = [j]
        # append to covered all the attributes covered by the selected subset
        for i in universe:
            if subset in attributes[i-1] and not i in covered:
                covered.append(i)
                set_of_subsets[str(subset)].append(i)
        # store the selected subset
        cover.append(subset)
        cost += costs[subset-1]
        
    if del_redundancy:
        # list of redundant subsets
        redundant = []
        # iterate over the set of subsets
        for i, set1 in enumerate(list(set_of_subsets.keys())):
            # compare current position with all others
            flags = [False for elem in set_of_subsets[set1]]
            for j, set2 in enumerate(list(set_of_subsets.keys())[i+1:]):
                for k, elem in enumerate(set_of_subsets[set1]):
                    if elem in set_of_subsets[set2]:
                        flags[k]=True
            # if all elements of subset1 covered in other subsets, append subset1 to redundant
            if all(flags)==True:
                redundant.append(set1)
            
        for elem in redundant:
            # remove the redundant sets from the set_of_subsets
            del set_of_subsets[elem]
            # update the cost
            cost-=costs[int(elem)-1]
            # remove the set from the list of selected subsets
            cover.remove(int(elem))
            
    return set_of_subsets, cover, cost


def ch3(universe, attributes, costs, del_redundancy=True):
    
    cost=0
    
    covered = list()
    
    cover = list()
    set_of_subsets = dict()
    # step 1: count the number of attributes covered by each subset and update the costs
    subsets = list(range(1, len(costs)+1))
    costs_per_attr = deepcopy(costs)
    for s in subsets:
        counts = 0
        for elem in attributes:
            if len(elem) == 0:
                continue
            if s in elem:
                counts+=1
        costs_per_attr[s-1] = costs[s-1]/(counts+1e-6)
    while not all(item in covered for item in universe):
        
        # select an uncovered attribute
        for j in universe:
            if not j in covered:
                covered.append(j)
                break
                
        # step 2: select the subset with the smallest cost/(element) that covers the attribute
        if attributes[j-1] == []:
            covered.append(j)
            continue
        subset = attributes[j-1][0]
        
        cmin = costs_per_attr[subset-1]
        for sub in attributes[j-1]:
            if costs_per_attr[sub-1] < cmin:
                cmin = costs_per_attr[sub-1]
                subset = sub
        # add the selected subset to the set of subsets
        set_of_subsets[str(subset)] = [j]   
        # append to covered all the attributes covered by the selected subset
        for i in universe:
            if subset in attributes[i-1]:
                covered.append(i)
                set_of_subsets[str(subset)].append(i)
        # store the selected subset
        cover.append(subset)
        cost += costs[subset-1]
    if del_redundancy:
        # list of redundant subsets
        redundant = []
        # iterate over the set of subsets
        for i, set1 in enumerate(list(set_of_subsets.keys())):
            # compare current position with all others
            flags = [False for elem in set_of_subsets[set1]]
            for j, set2 in enumerate(list(set_of_subsets.keys())[i+1:]):
                for k, elem in enumerate(set_of_subsets[set1]):
                    if elem in set_of_subsets[set2]:
                        flags[k]=True
            # if all elements of subset1 covered in other subsets, append subset1 to redundant
            if all(flags)==True:
                redundant.append(set1)
            
        for elem in redundant:
            # remove the redundant sets from the set_of_subsets
            del set_of_subsets[elem]
            # update the cost
            cost-=costs[int(elem)-1]
            # remove the set from the list of selected subsets
            cover.remove(int(elem))
    return set_of_subsets, cover, cost
  
  parent_dir="Instances"

instances = [
    "4.2", "4.3", "4.4", "4.5", "4.6", "4.7", "4.8", "4.9",
    "5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7", "5.8", "5.9",
    "6.1", "6.2", "6.3", "6.4", "6.5",
    "A.1", "A.2", "A.3", "A.4", "A.5",
    "B.1", "B.2", "B.3", "B.4", "B.5",
    "C.1", "C.2", "C.3", "C.4", "C.5",
    "D.1", "D.2", "D.3", "D.4", "D.5",
]

for inst in instances:
    instance = 'scp'+''.join(inst.split('.')).lower() +'.txt'
    data = load_instance(instance=instance)

    # first line : nattr, nsets
    for i, elem in enumerate(data):
        data[i]= [int(e) for e in elem.strip().split(" ")]

    # second line: costs
    costs = []
    for i, elem in enumerate(data[1:]):
        if len(elem)==1:
            break
        costs.extend(elem)

    del data[1:i+1]
    data.insert(1, costs)

    # following lines (MxK), with M=nattr, and K=num sets that cover attribute m: nsets, list(sets)

    # 1: store de row indices that indicate nsets
    indices=[]
    for j, line in enumerate(data[:-1]):
        if len(line)==1 and len(data[j+1])>1: 
            # a line with 1 element is only an index if the next line contains more than 1 element
            # otherwise, it could still be a set (e.g. 25 (12+12+1))
            indices.append(j)

    # 2: iterate over the sets:
    for i in indices:
        s = []
        for j, elem in enumerate(data[i+1:-1]):
            if len(elem)==1 and len(data[j+1])>1:
                break
            s.extend(elem)
        data[i]=s

    sets = [data[i] for i in indices]
    del data[2:]
    data.extend(sets)

    m=data[0][0]
    universe = list(range(1, m+1))
    attributes = data[2:]
    costs =  data[1]
    sets, _, cost = ch3(universe, attributes, costs, True)
    with open(os.path.join(parent_dir,"results","scp_ch3.txt"), "a") as f:
            f.write(str(inst)+' '+str(cost)+'\n')
        
# Fraction of instances that have improved after redundancy elimination

f1 = "Instances//results//scp_ch3.txt"
f2 = "Instances//results//scp_ch3r.txt"

df1 = pd.read_csv(f1, sep=" ", header=None, names=["id", "cost"])
df2 = pd.read_csv(f2, sep=" ", header=None, names=["id", "cost"])

r = ((df1["cost"] < df2["cost"]).sum() / len(df1))*100

print(f"Fraction of improvement (CH3): {r:.2f} %")

# Average Percent Deviation from Best Known Solutions

f1 = "Instances//results//scp_best.txt"
f2 = "Instances//results//scp_ch3.txt"

df1 = pd.read_csv(f1, sep=" ", header=None, names=["id", "cost"])
df2 = pd.read_csv(f2, sep=" ", header=None, names=["id", "cost"])

avg_pc_deviation = (((df2["cost"] / df1["cost"]) - 1)*100).mean()

print(f"Average Percent Deviation from Best Known Solutions: {avg_pc_deviation:.2f} %")
  
