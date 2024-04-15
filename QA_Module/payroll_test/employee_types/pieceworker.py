import locale

from employee_types.employee import Employee


class PieceWorker(Employee):
    def __init__(self, first, last, ssn, wage_per_piece, pieces_produced):
        super().__init__(first, last, ssn)
        self.wage_per_piece = wage_per_piece  # validate wage per piece via property
        self.pieces_produced = pieces_produced  # validate pieces produced via property

    @property
    def wage_per_piece(self):
        return self._wage_per_piece

    @wage_per_piece.setter
    def wage_per_piece(self, value):
        if value < 0:
            raise ValueError("Wage must be >= 0")
        self._wage_per_piece = value

    @property
    def pieces_produced(self):
        return self._pieces_produced

    @pieces_produced.setter
    def pieces_produced(self, value):
        if value < 0:
            raise ValueError("Pieces must be >= 0")
        self._pieces_produced = value

    def earnings(self):
        return self.pieces_produced * self.wage_per_piece

    def __str__(self):
        return f"piece worker: {super().__str__()}\nwage per piece: {locale.currency(self.wage_per_piece)}; pieces produced: {self.pieces_produced}"
