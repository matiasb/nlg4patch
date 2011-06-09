# -*- coding: utf-8 -*-
# Author: Matías Bordese

from base import Joiner

class WhereJoin(Joiner):
    """Realise second sentence as 'where' complement of the first one."""
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def realise(self):
        return "%s, where %s" % (self.p1.realise(), self.p2.realise())


class AndJoin(Joiner):
    """Realise second sentence joined by 'and', assuming same subject."""
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def realise(self):
        return "%s and %s %s" % (self.p1.realise(), self.p2.subj.as_pronoun,
                                 self.p2.predicate)


class SentencesAndJoin(Joiner):
    """Realise sentences joined by 'and'."""
    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2

    def realise(self):
        return "%s and %s" % (self.s1.realise(), self.s2.realise())


class InlineJoin(Joiner):
    """Realise second sentence as a comma separated inline note."""
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def realise(self):
        return "%s, %s, %s" % (self.p1.subject, self.p2.inline,
                               self.p1.predicate)
