class InvalidArgumentError(Exception):
    def __init__(self, *args, **kwargs):
        super(InvalidArgumentError, self).__init__(args, kwargs)
