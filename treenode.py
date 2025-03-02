from CollectiveImpurityEntropy import CollectiveImpurityEntropy
from CollectiveImpurityGini import CollectiveImpurityGini

class Leaf:
    def __init__(self):
        self.pivot = "LEAF"

    def __str__(self):
        return "LEAF"

class TreeNode:

    def __init__(self, record_list, 
                 strategy, 
                 max_depth, 
                 pivots,
                 target, 
                 invert,
                 parent_pivot,
                 depth = 0,
                 score = 0
                 ):
        
        self.record_list = record_list
        self.strategy = strategy
        self.max_depth = max_depth
        self.pivots = pivots.copy()
        self.pivot_name = "none"

        self.target = target
        self.invert = invert
        self.score = score
        self.parent_pivot = parent_pivot
        self.depth = depth + 1
        self.risk = self.risk_assessment()

        self.children = []
        
        if len(self.pivots) > 1:
            self.pivot = self.select_pivot()
            self.homogenous = self.is_homogenous()
            
            if self.pivot != None and not self.homogenous:
                self.grow_tree()
        
            
        #print(self, len(self.children), "\n")
        #[c.parent_pivot for c in self.children if isinstance(c, TreeNode)]


    def __str__(self):
        return f"{self.parent_pivot}, impurity: {self.score}, risk: {self.risk}, pivot: {self.pivot_name} h = {self.is_homogenous()}, length: {len(self.record_list)}, depth: {self.depth}"


    def risk_assessment(self):
        risk = 0
        for record in self.record_list:
            if record.attrs[self.target] == True:
                risk += 1
        return risk / len(self.record_list)

    def classify(self, record):
        if len(self.children) == 0:
            return self.risk
        
        elif len(self.children) == 1:
            if self.pivot:
                return self.children[0].classify(record)
            else:
                return self.risk
        elif len(self.children) == 2:
            if self.pivot(record):
                return self.children[0].classify(record)
            else:
                return self.children[1].classify(record)

    def is_homogenous(self):
        if len(self.record_list) == 0:
            return True
        
        first = self.record_list[0].attrs[self.target]
        hom = True
        for record in self.record_list:
            if record.attrs[self.target] != first:
                hom = False
        
        return hom
    

    def compute_val(self, split):
        if len(split) > 0:
            gini = self.strategy.compute(split, label=self.target, invert=self.invert)
            w = len(split) / len(self.record_list)
        else:
            return 0, 0
        return gini, w
    

    def weighted_impurity(self, splits):
        gini_1, w_1 = self.compute_val(splits[0])
        gini_2, w_2 = self.compute_val(splits[1])
        return w_1 * gini_1 + w_2 * gini_2
    

    def split(self, pivot):
        splits= [[],[]]
        for record in self.record_list:
            if pivot(record):
                splits[0].append(record)
            else:
                splits[1].append(record)
        return splits


    def select_pivot(self):
        scores = {}

        for pivot in self.pivots:
            if pivot != self.target:
                splits = self.split(self.pivots[pivot])
                if len(self.record_list) > 0:
                    x = self.weighted_impurity(splits)
                else:
                    x = 0
                scores.update({pivot: x})

        if len(scores) > 0:
            minim = min(scores.items(), key=lambda x: x[1])[0]
            pivot = self.pivots[minim]
            self.score = min([k[1] for k in scores.items()])
            self.pivot_name = minim
            self.pivots.pop(minim)
        else:
            pivot = None
        return pivot
    

    def split(self, pivot):
        splits = [[],[]]
        for record in self.record_list:
            if pivot(record):
                splits[0].append(record)
            else:
                splits[1].append(record)
        return splits


    def grow_tree(self):
        splits = self.split(self.pivot)

        for i in range(len(splits)):
            if len(splits[i]) > 0:
                if i == 0:
                    dir = "_True"
                else:
                    dir = "_False"
                node = TreeNode(splits[i], self.strategy, self.max_depth,
                                self.pivots, self.target, self.invert,
                                self.pivot_name + f"{dir}", self.depth,
                                )
                self.children.append(node)