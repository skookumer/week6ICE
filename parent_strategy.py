class ParentStrategy:

    def probability(record_list, label, invert):

        '''
        simple function coded per the instructions. However, I added a 'label' option
        to designate the target variable. So if we want to optimize for risk, we can do that,
        but we can also optimize for gender or color or anything else if we wanted to

        added "invert" parameter later on. This just flips the relationship between
        how the probability is computed. So in the case of gender, we can find which combination
        reduces complexity wrt female, or lowrisk in assessment
        '''


        val = 0
        for record in record_list:
            if record.attrs[label] == True:
                val += 1
        
        if invert:
            return 1 - val / len(record_list)
        else:
            return val / len(record_list)

    
    def probability_split(self, records, label):

        '''
        wrote this function early on when trying out the partition function
        '''

        split = []
        for record_list in records:
            split.append(self.probability(self, record_list, label))
        return tuple(split)