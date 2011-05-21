# -*- coding: utf-8 -*-
# Author: Matías Bordese


import os.path

from nlg4patch.unidiff.patch import PatchedFile

from config import (ADDITION, DELETION, MODIFICATION, HUNK, ADDED_FILE,
                    DELETED_FILE, MODIFIED_FILE)

class PatchedFileMessage(object):
    def __init__(self, filename, additions=0, deletions=0, modifications=0,
                 hunks=0, added=False, deleted=False):
        self.extension = os.path.splitext(filename)[1]
        self.filename = filename
        self.additions = additions
        self.deletions = deletions
        self.modifications = modifications
        self.hunks = hunks
        self.added = added
        self.deleted = deleted

    @property
    def score(self):
        score = (ADDITION * self.additions + DELETION * self.deletions +
                 MODIFICATION * self.modifications + HUNK * self.hunks)
        if self.added:
            score += ADDED_FILE
        elif self.deleted:
            score += DELETED_FILE
        else:
            score += MODIFIED_FILE
        return score


class DirectoryMessage(list):
    def __init__(self, dirname=''):
        self.dirname = dirname

    @property
    def file_extensions(self):
        return set([f.extension for f in self])

    @property
    def score(self):
        return sum(f.score for f in self)

    @property
    def hunks(self):
        return sum(f.hunks for f in self)

    @property
    def modified_files(self):
        return sum(1 for f in self if not f.added and not f.deleted)

    @property
    def added_files(self):
        return sum(1 for f in self if f.added)

    @property
    def deleted_files(self):
        return sum(1 for f in self if f.deleted)

    @property
    def modifications(self):
        return sum(f.modifications for f in self)

    @property
    def additions(self):
        return sum(f.additions for f in self)

    @property
    def deletions(self):
        return sum(f.deletions for f in self)


def content_planning(patch):
    # build directory messages list
    messages = {}
    for diff in patch:
        directory = os.path.dirname(diff.path)
        dirmsg = messages.get(directory, DirectoryMessage(dirname=directory))
        filemsg = PatchedFileMessage(os.path.basename(diff.path), diff.added,
                                     diff.deleted, diff.modified, len(diff),
                                     diff.is_added_file, diff.is_deleted_file)
        dirmsg.append(filemsg)
        messages[directory] = dirmsg
        
    # order by score
    sorted_messages = sorted((msg for msg in messages.itervalues()),
                             key=lambda m: m.score, reverse=True)

    # pop and set relations
    return sorted_messages


# microplanning
# dir_focus
# if len(sorted_messages) == 1:
#    "all the updated files are from the D directory"
#    "only one file from the D directory is updated"

# directory desc: extensions, number of files, 1 of N
# distribution phrase: blocks, additions, deletions, modifications (aleatoriamente: totalize, summarize)

# to_be(subject, object=None, from=None)
# to_have(subject, object)
# to_distribute(subject, object, pasive)
# to_update(subject, object, pasive)
# to_add(subject, object, pasive)
# to_deleted(subject, object, pasive)
