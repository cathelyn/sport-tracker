from texttable import Texttable
from sport_tracker.common.exceptions import InvalidArgumentError


class TerminalOutput:
    @staticmethod
    def print_table(header: list, data: list):
        if len(header) != len(data[0]):
            raise InvalidArgumentError("Header and data must have the same number of columns")
        table = Texttable()
        table.add_rows([header] + data)
        print(table.draw())
