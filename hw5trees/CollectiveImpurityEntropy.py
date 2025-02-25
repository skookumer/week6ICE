from parent_strategy import ParentStrategy
import math

class CollectiveImpurityEntropy(ParentStrategy):

    def compute(record_list, label, invert):
        '''
        decided to do this with a nested function to simplify writing the
        math
        '''

        def p_log2_p(x):
            '''
            added the conditional to avoid a math domain error
            '''
            if x != 0:
                return x * math.log2(x)
            else:
                return x


        p_i = ParentStrategy.probability(record_list, label, invert)

        return -1 * (p_log2_p(p_i) + p_log2_p(1 - p_i))