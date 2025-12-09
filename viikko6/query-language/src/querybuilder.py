from matchers import And, Or, All, PlaysIn, HasAtLeast, HasFewerThan


class QueryBuilder:
    def __init__(self, matcher=None):
        self._matcher = matcher or All()

    def plays_in(self, team):
        uusi = PlaysIn(team)
        uusi_matcher = And(self._matcher, uusi)
        return QueryBuilder(uusi_matcher)

    def has_at_least(self, value, attr):
        uusi = HasAtLeast(value, attr)
        uusi_matcher = And(self._matcher, uusi)
        return QueryBuilder(uusi_matcher)

    def has_fewer_than(self, value, attr):
        uusi = HasFewerThan(value, attr)
        uusi_matcher = And(self._matcher, uusi)
        return QueryBuilder(uusi_matcher)
    
    def one_of(self, *queries):
        matchers = []
        for q in queries:
            if isinstance(q, QueryBuilder):
                matchers.append(q.build())
            else:
                matchers.append(q)

        uusi_matcher = Or(*matchers)
        return QueryBuilder(uusi_matcher)

    def build(self):
        return self._matcher
