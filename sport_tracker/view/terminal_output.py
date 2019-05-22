from texttable import Texttable
from sport_tracker.common.exceptions import IllegalArgumentException


class TerminalOutput:
    @staticmethod
    def print_table(header: list, data: list):
        if len(header) != len(data[0]):
            raise IllegalArgumentException("Header and data must have the same number of columns")
        table = Texttable()
        table.add_rows([header] + data)
        print(table.draw())
