from parent_strategy import ParentStrategy

class CollectiveImpurityGini(ParentStrategy):

    def compute(record_list, label, invert):

        '''
        coded according to the instructions. 1 - p_i facilitates getting the probability of False in any situation,
        as opposed to re-computing for the false label
        '''
    
        p_i = ParentStrategy.probability(record_list, label, invert)

        return 1 - (p_i ** 2 + (1 - p_i) ** 2)