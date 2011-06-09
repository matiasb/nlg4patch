# -*- coding: utf-8 -*-
# Author: Matías Bordese

"""Surface Realiser base classes for templates and joiners."""

class Realisable(object):
    """Base class for a realisable classes."""
    
    def realise(self):
        """Return realised object."""


class BaseSimpleSentence(Realisable):
    """Base class for a simple sentence: subject, verb and predicate."""

    def __init__(self, subject):
        self.subj = subject

    @property
    def singular(self):
        """Return True if the sentence should be referred as singular."""
        return self.subj.singular

    @property
    def subject(self):
        """Return realised subject."""
        return self.subj.realise()

    @property
    def verb(self):
        """Return realised verb (ie, conjugated)."""
        verb = 'is' if self.subj.singular else 'are'
        return verb

    @property
    def inline(self):
        """Return sentence information to be included as inline."""
        return ''

    @property
    def predicate(self):
        """Return realised predicate."""
        return "%s %s" % (self.verb, self.inline)
        
    def realise(self):
        """Return realised sentence."""
        return "%s %s" % (self.subject, self.predicate)


class Joiner(Realisable):
    """Base class for a sentence joiner class."""
