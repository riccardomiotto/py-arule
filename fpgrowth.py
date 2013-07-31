'''
 FP-growth algorithm to mine frequent itemsets from a data collection

 @details: implementatio based on a frequent pattern tree

'''


# @param data = [(id_doc, [tags])]
def fpgrowth (data, minsup):
	itr = _frequent_pattern_generator (data, minsup)
	itemsets = {}
	for it in itr:
		pit = tuple(sorted(it[0]))
		itemsets[pit] = it[1]
	return itemsets



'''
 private functions
'''

# generate the frequent patterns
def _frequent_pattern_generator (data, minsup):
	fpt = FPTree.generate (data, minsup)
	for fp in fpt.mine_frequent_patterns():
		yield fp


		
'''
 Frequent-pattern tree classes
'''

# frequent pattern tree
class FPTree(object):
		
	# constructor	
	def __init__ (self, minsup):
		self.minsup = minsup
		self.header = {}
		self.root = FPNode (None, None)
		self.isup = {}

	
	# check if the tree is empty  
	def is_empty (self):
		return len(self.root.children) == 0


	# mine the frequent patterns
	def mine_frequent_patterns(self):
		for fi in self.__fp_growth(tuple()):
			yield fi

	
	# static functions
	
	# create FP-tree from data organized as [(id_doc, [items])}
	@staticmethod
	def generate (data, minsup):
		wdata = [(d[1],1) for d in data]
		return FPTree.generate_by_wdata (wdata, minsup)

  
	# create FP-tree from data organized as [(item,w)]
	@staticmethod
	def generate_by_wdata (wdata, minsup):
		self = FPTree(minsup)
		for it, w in wdata:
			for i in set(it):
				self.isup[i] = self.isup.get(i,0) + w
		# sort
  		lfreq_desc = sorted([(i,f) for (i,f) in self.isup.items() if f >= minsup], key=lambda(i,f):f, reverse=True)
		lfreq_desc_order = dict((i,o) for (o,(i,f)) in enumerate(lfreq_desc))
		# insert into the tree	
		for it, w in wdata:
			ifreq = sorted([i for i in set(it) if i in lfreq_desc_order], key = lambda i:lfreq_desc_order[i])
			self.__insert(ifreq, w)  
		return self


	# private functions
	  	
	# insert element in the tree
	def __insert (self, fitems, weight):
		cnode = self.root
		for it in fitems:
			if it not in cnode.children:
				nnode = FPNode(it, cnode)
				cnode.children[it] = nnode
				self.header.setdefault (it,[]).append(nnode)
			cnode = cnode.children[it]
			cnode.count += weight


	# fp-growth algorithm
	def __fp_growth(self, suffix):
		for it in self.header:
			nsfx = (it,) + suffix
			yield (nsfx, self.isup[it])
			ctree = self.__build_conditional_tree(it)
			if not ctree.is_empty():
				for fp in ctree.__fp_growth(nsfx):
					yield fp


	# build the conditional tree
	def __build_conditional_tree (self, item):
		ctree = []
		for node in self.header[item]:
			path = []
			pnode = node.parent
			while pnode is not self.root:
				path.append(pnode.item)
				pnode = pnode.parent
			ctree.append((path, node.count))
		return FPTree.generate_by_wdata (ctree, self.minsup)



# frequent pattern tree node
class FPNode(object):
	
	# constructor
	def __init__(self, item, parent):
		self.item = item
		self.count = 0
		self.children = {}
		self.parent = parent
