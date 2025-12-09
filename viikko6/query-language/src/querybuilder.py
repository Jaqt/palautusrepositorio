from matchers import And, All, PlaysIn, HasAtLeast, HasFewerThan


class QueryBuilder:
    def __init__(self, matcher=None):
        self._matcher = matcher or All()

    def plays_in(self, team):
        uusi = PlaysIn(team)
        self._matcher = And(self._matcher, uusi)
        return self

    def has_at_least(self, value, attr):
        uusi = HasAtLeast(value, attr)
        self._matcher = And(self._matcher, uusi)
        return self

    def has_fewer_than(self, value, attr):
        uusi = HasFewerThan(value, attr)
        self._matcher = And(self._matcher, uusi)
        return self

    def build(self):
        return self._matcher
