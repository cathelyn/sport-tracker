from pint import UnitRegistry

from sport_tracker.common.exceptions import InvalidArgumentError


class Sport:
    def __init__(self, name: str):
        self._duration = 0  # secs
        self.name = name

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
                raise InvalidArgumentError("Illegal number of arguments.")
        else:
            raise TypeError


class MovingSport(Sport):  # otherwise Activity is static
    def __init__(self, name: str):
        super(MovingSport, self).__init__(name)
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
            except InvalidArgumentError("Not valid distance"):
                # TODO: Verify
                raise
