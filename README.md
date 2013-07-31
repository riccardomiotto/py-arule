Python implementation of the FP-Growth algorithm to mine association rules from a dataset. 

The documents in the collection must be indexed by an unique ID and a sequence of words/tags. 
The code accepts the dataset as a list of tuples in the form (id_doc,[tags]). 

The algorithm first grows a frequent pattern tree (FP-tree) to efficiently mine itemsets 
(i.e., combination of tags) frequently appearing in the collection (i.e., satisfying the 
minimum support requirement). Then, from these sets, the algorithm extracts all the 
possible rules and retains only those satisfying a pre-set minimum confidence.

More details about the algorithm and association rules can be found in:

1. http://en.wikibooks.org/wiki/Data_Mining_Algorithms_In_R/Frequent_Pattern_Mining/The_FP-Growth_Algorithm

2. http://csc.lsu.edu/~jianhua/FPGrowth.pdf

Python Requirement: None

Author: Riccardo Miotto