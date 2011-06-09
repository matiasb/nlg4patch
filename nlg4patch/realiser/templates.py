# -*- coding: utf-8 -*-
# Author: Matías Bordese

"""Surface Realiser Templates."""

from base import Realisable, BaseSimpleSentence
from config import KNOWN_EXTENSIONS


class Paragraph(Realisable):
    """Realisable paragraph."""
    def __init__(self, *sentences):
        self.sentences = sentences

    def realise(self):
        """Return realised sentences separated by spaces."""
        # add spaces between sentences
        realisation = ' '.join([s.realise() for s in self.sentences])
        return realisation


class Sentence(Realisable):
    """Realisable sentence."""
    def __init__(self, p1, additional_begin='', additional_end=''):
        self.p1 = p1
        self.begin = additional_begin
        self.end = additional_end

    def realise(self):
        """Return realised sentence; capitalize and add punctuation."""
        # capitalize first word, add sentence punctuation
        realisation = ''.join([self.begin, self.p1.realise(), self.end])
        sentence = '%c%s.' % (realisation[0].upper(), realisation[1:])
        return sentence


class NounPhrase(Realisable):
    """Realisable noun phrase."""
    def __init__(self, phrase, singular=True):
        self.phrase = phrase
        self.singular = singular

    @property
    def as_pronoun(self):
        """Return noun phrase realised as a pronoun."""
        pronoun = 'it' if self.singular else 'they'
        return pronoun

    def realise(self):
        """Return realised noun phrase."""
        return self.phrase


class Directory(Realisable):
    """Realisable directory."""
    def __init__(self, name, parent_path='/', already_mentioned=False):
        self.name = name
        self.parent_path = parent_path
        self.already_mentioned = already_mentioned

    def realise(self):
        """Return directory realisation."""
        self.already_mentioned = True
        return self.name


class Summary(BaseSimpleSentence):
    """Global summary of affected files and changes distribution."""
    def __init__(self, directories, added, deleted, modified):
        self.directories = directories
        self.data = [(added, 'added file'),
                     (deleted, 'deleted file'),
                     (modified, 'modified file'),]
        singular = added + deleted + modified == 1
        super(Summary, self).__init__(NounPhrase('there', singular=singular))

    def _realise_param(self, param):
        ret = ' '.join([str(param[0]), param[1]])
        if param[0] > 1:
            ret += 's'
        return ret

    def _realise_data(self):
        filtered_data = filter(lambda x: x[0], self.data)
        filtered_data = map(lambda x: self._realise_param(x), filtered_data)
        if len(filtered_data) == 1:
            realised_data = filtered_data[0]
        else:
            realised_data = ', '.join(filtered_data[:-1])
            realised_data = '%s and %s' % (realised_data, filtered_data[-1])
        return realised_data

    @property
    def inline(self):
        realised_data = self._realise_data()
        if self.directories == 1:
            ret = "%s from 1 directory" % realised_data
        else:
            ret = "%s from %d directories" % (realised_data, self.directories)
        return ret


class NumberOfFiles(BaseSimpleSentence):
    """Realiser for: There are N [action] files in directory D."""
    def __init__(self, number, directory=None, action=None):
        self.number = number
        self.action = action
        self.directory = directory
        super(NumberOfFiles, self).__init__(NounPhrase('there'))

    @property
    def singular(self):
        return self.number == 1

    @property
    def inline(self):
        inline = "%d %s file" % (self.number, self.action)
        inline = inline if self.singular else '%ss' % inline

        if self.directory is not None and self.directory.already_mentioned:
            inline += " in that directory"
        elif self.directory is not None and not self.directory.already_mentioned:
            inline += " in directory %s" % self.directory.realise()

        return inline


class ChangesFromDirectory(BaseSimpleSentence):
    """Realiser for: Subject from directory D."""
    def __init__(self, subject, directory=None):
        self.directory = directory
        super(ChangesFromDirectory, self).__init__(subject)

    @property
    def inline(self):
        if self.directory is None:
            return ""
        if self.directory.already_mentioned:
            dir_desc = "from that directory"
        else:
            dir_desc = "from directory %s" % self.directory.realise()
        return dir_desc


class HaveExtension(BaseSimpleSentence):
    """Realiser for: Subject has/have the extension .ext | is/are [filetype]."""
    def __init__(self, subject, extensions):
        self.known_extensions = []
        self.unknown_extensions = []
        for ext in extensions:
            if ext in KNOWN_EXTENSIONS:
                self.known_extensions.append(KNOWN_EXTENSIONS[ext])
            else:
                self.unknown_extensions.append(ext)
        super(HaveExtension, self).__init__(subject)

    @property
    def verb(self):
        if not self.known_extensions:
            verb = 'has' if self.subj.singular else 'have'
        else:
            verb = 'is' if self.subj.singular else 'are'
        return verb

    @property
    def inline(self):
        extensions = self.known_extensions + self.unknown_extensions
        if not self.known_extensions and len(self.unknown_extensions) > 1:
            file_desc = 'with extensions %s' % (
                                    ', '.join(self.unknown_extensions[:-1]))
            file_desc = '%s and %s' % (file_desc, self.unknown_extensions[-1])
        elif not self.known_extensions and len(self.unknown_extensions) == 1:
            if self.unknown_extensions[0] == '':
                file_desc = "with no extension"
            else:
                file_desc = "with extension %s" % self.unknown_extensions[0]
        elif len(extensions) > 1:
            file_desc = ', '.join(extensions[:-1])
            file_desc = '%s and %s' % (file_desc, extensions[-1])
        else:
            file_desc = self.known_extensions[0]
        return file_desc

    @property
    def predicate(self):
        file_desc = self.inline
        if file_desc.startswith('with '):
            file_desc = file_desc[5:]
        return "%s %s" % (self.verb, file_desc)


class ChangesDistribution(BaseSimpleSentence):
    """Realiser for: Changes are distributed in N files,
       summarizing N additions, N deletions and N modifications."""
    def __init__(self, files, additions, deletions, modifications):
        self.files = files
        self.data = [(additions, 'addition'),
                     (deletions, 'deletion'),
                     (modifications, 'modification')]
        if (additions + deletions + modifications) == 1:
            subject = NounPhrase('change')
        else:
            subject = NounPhrase('all changes', singular=False)
        super(ChangesDistribution, self).__init__(subject)

    @property
    def inline(self):
        realised_data = self._realise_data()
        if self.files == 1:
            ret = "summarized in %s" % realised_data
        else:
            ret = "distributed in %d files, summarizing %s" % (self.files,
                                                               realised_data)
        return ret

    def _realise_param(self, param):
        ret = ' '.join([str(param[0]), param[1]])
        if param[0] > 1:
            ret += 's'
        return ret

    def _realise_data(self):
        filtered_data = filter(lambda x: x[0], self.data)
        filtered_data = map(lambda x: self._realise_param(x), filtered_data)
        if len(filtered_data) == 1:
            realised_data = filtered_data[0]
        else:
            realised_data = ', '.join(filtered_data[:-1])
            realised_data = '%s and %s' % (realised_data, filtered_data[-1])
        return realised_data


class AddedToDir(BaseSimpleSentence):
    """Realiser for: subject is/are added to directory D."""
    def __init__(self, subject, directory=None):
        self.directory = directory
        super(AddedToDir, self).__init__(subject)

    @property
    def inline(self):
        if self.directory is None:
            return "added"
        if self.directory.already_mentioned:
            dir_desc = "to that directory"
        else:
            dir_desc = "to directory %s" % self.directory.realise()
        return "added %s" % dir_desc


class DeletedFromDir(BaseSimpleSentence):
    """Realiser for: Subject is/are deleted from directory D."""
    def __init__(self, subject, directory=None):
        self.directory = directory
        super(DeletedFromDir, self).__init__(subject)

    @property
    def inline(self):
        if self.directory is None:
            return "deleted"
        if self.directory.already_mentioned:
            dir_desc = "from that directory"
        else:
            dir_desc = "from directory %s" % self.directory.realise()
        return "deleted %s" % dir_desc
