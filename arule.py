'''
 Mining tag-based association rule from a collection of documents
 
 @algorith: frequent pattern tree-based implementation
 
 @author: Riccardo Miotto
'''

from fpgrowth import fpgrowth
import math, random, sys, cPickle



'''
 mining the association rules using the fp-growth algorithm
 @param index: [(id_doc,[tags])]
 @param minsup: minimum support (between 0 and 1)
 @param minconf: minimum confidence (between 0 and 1)

 @output rule: association rules in the form {(antecedent): [(consequent, confidence)]}
'''
def arule_mining (index, minsup = 0.01, minconf = 0.2):
	nminsup = math.ceil (minsup * len(index))
	itemsets = fpgrowth (index, nminsup)
	return _derive_association_rule (itemsets, minconf)



# private functions

'''
 derive the association rules from the frequent itemsets
'''
def _derive_association_rule (itemsets, minconf):
	rule = {}
	for it in itemsets:
		if len(it) == 1:
			continue
		items = set(it)
		supp = itemsets[it]
		for sright in items:
			sleft = tuple(sorted(items - set([sright])))
			conf = supp / float(itemsets[tuple([sright])])
			if (conf >= minconf):
				cons = rule.setdefault (sleft, {})
				cons[sright] = conf
				rule[sleft] = cons
	# sort the right-sides by confidence
	for ru in rule.keys():
		cons = [(k,v) for (k,v) in reversed(sorted(rule[ru].iteritems(), key=lambda (k,v): (v,k)))]
		rule[ru] = cons
	return rule



'''
main

@param [1]: pickle object filename containing the dataset as [(id_doc, [tags])]
@param [2]: minimum support of the association rules (between 0 and 1)
@param [3]: minimum confidence fo the association rules (between 0 a 1)
'''

if __name__ == '__main__' :
	try:
		dataset = cPickle.load (open(sys.argv[1], 'rb'))
		minsup = float (sys.argv[2])
		minconf = float (sys.argv[3])
		r = arule_mining (dataset, minsup, minconf)
		print r
	except Exception as e:
		print e
