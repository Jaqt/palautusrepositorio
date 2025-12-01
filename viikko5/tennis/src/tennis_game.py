class TennisGame:
    def __init__(self, player1_name: str, player2_name: str) -> None:
        self.player1_name = player1_name
        self.player2_name = player2_name
        self._p1 = 0
        self._p2 = 0
        self.points = ["Love", "Fifteen", "Thirty", "Forty"]
        self.min_points = 4
        self.win_diff = 2

    def won_point(self, player_name: str) -> None:
        if player_name in ("player1", self.player1_name):
            self._p1 += 1
        else:
            self._p2 += 1

    def get_score(self) -> str:
        if self._is_tie():
            return self._format_tie()

        if self._is_endgame():
            return self._format_endgame()

        return self._format_regular()

    def _is_tie(self) -> bool:
        return self._p1 == self._p2

    def _is_endgame(self) -> bool:
        return self._p1 >= self.min_points or self._p2 >= self.min_points

    def _format_tie(self) -> str:
        if self._p1 >= 3:
            return "Deuce"
        return f"{self.points[self._p1]}-All"

    def _format_endgame(self) -> str:
        diff = self._p1 - self._p2
        if abs(diff) >= self.win_diff:
            return "Win for player1" if diff > 0 else "Win for player2"
        return "Advantage player1" if diff > 0 else "Advantage player2"

    def _format_regular(self) -> str:
        return f"{self.points[self._p1]}-{self.points[self._p2]}"
