class IllegalArgumentException(Exception):

    def __init__(self, *args, **kwargs):
        super(IllegalArgumentException, self).__init__(args, kwargs)
