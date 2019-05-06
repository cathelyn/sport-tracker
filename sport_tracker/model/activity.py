from sport_tracker.common.exceptions import IllegalArgumentException
from pint import UnitRegistry


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


class MovingActivity(Activity):  # otherwise Activity is static

    def __init__(self):
        super(MovingActivity, self).__init__()
        self._distance = 0  # meters

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        if isinstance(value, int):
            self._distance = value
        else:
            try:
                unit_reg = UnitRegistry()
                self._distance = unit_reg.parse_expression(value).to(unit_reg.meter).magnitude
            except IllegalArgumentException("Not valid distance"):
                raise


# TODO: Implement activity factory

class Swimming(MovingActivity):

    def __init__(self):
        super(Swimming, self).__init__()


class Rowing(MovingActivity):

    def __init__(self):
        super(Rowing, self).__init__()


class Cycling(MovingActivity):

    def __init__(self):
        super(Cycling, self).__init__()


class RopeJumping(Activity):

    def __init__(self):
        super(RopeJumping, self).__init__()


class Running(MovingActivity):

    def __init__(self):
        super(Running, self).__init__()


class Squash(Activity):

    def __init__(self):
        super(Squash, self).__init__()


class Badminton(Activity):

    def __init__(self):
        super(Badminton, self).__init__()


class WeightLifting(Activity):
    def __init__(self):
        super(WeightLifting, self).__init__()


class Yoga(Activity):

    def __init__(self):
        super(Yoga, self).__init__()

