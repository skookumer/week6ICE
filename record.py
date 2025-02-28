class Record:

    def __init__(self, input_values, actual):

        '''
        my version does not use actual_label because I wanted to be able to change which
        label I optimized for
        '''
        
        self.attrs = input_values
        self.actual_label = actual
        self.predicted_label = None

        