from sport_tracker.common.exceptions import IllegalArgumentException


class Activity:

    def __init__(self):
        self._duration = 0  # secs

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        if isinstance(value, int):
            self. _duration = value
        elif isinstance(value, str):
            values = value.split(":")
            if len(values) == 2:
                try:
                    self._duration = 60 * int(values[0]) + int(values[1])
                except TypeError:
                    raise
            elif len(values) == 3:
                try:
                    self._duration = 3600 * int(values[0]) + 60 * int(values[1]) + int(values[2])
                except TypeError:
                    raise 
            else:
                raise IllegalArgumentException("Illegal number of arguments.")
        else:
            raise TypeError


class MovingActivity(Activity):

    def __init__(self):
        super(MovingActivity, self).__init__()
        self._distance = 0  # meters

    @property
    def distance(self):

        return self._distance


class StaticActivity(Activity):

    def __init__(self):
        super(StaticActivity, self).__init__()


class Swimming(MovingActivity):

    def __init__(self):
        super(Swimming, self).__init__()
