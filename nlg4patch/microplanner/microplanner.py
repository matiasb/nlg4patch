# -*- coding: utf-8 -*-
# Author: Matías Bordese

"""Microplanning module."""

import random

from nlg4patch.realiser.realiser import (Paragraph, Sentence, NounPhrase,
    Directory, HaveExtension, ChangesFromDirectory, ChangesDistribution,
    AddedToDir, DeletedFromDir, NumberOfFiles, Summary)

from nlg4patch.realiser.realiser import (AndJoin, InlineJoin, SentencesAndJoin,
    WhereJoin)

def microplanning(messages):
    paragraphs = []
    iteration = 1

    if messages:
        # create global summarization paragraph
        total_directories = len(messages)
        total_added_files = sum(m.added_files for m in messages)
        total_deleted_files = sum(m.deleted_files for m in messages)
        total_modified_files = sum(m.modified_files for m in messages)
        s1 = Summary(total_directories, total_added_files,
                     total_deleted_files, total_modified_files)

        total_additions = sum(m.additions for m in messages)
        total_deletions = sum(m.deletions for m in messages)
        total_modifications = sum(m.modifications for m in messages)
        s2 = ChangesDistribution(1, total_additions, total_deletions,
                                 total_modifications)

        p = Paragraph(Sentence(s1), Sentence(s2))
        paragraphs.append(p)
    
    for msg in messages:
        sentences = []
        directory = Directory(msg.dirname)

        if random.uniform(0, 1) > 0.5:
            # in directory and extensions
            if len(messages) == 1 and msg.modified_files == 1:
                subject = NounPhrase('the only updated file')
            elif len(messages) == 1 and msg.modified_files > 1:
                subject = NounPhrase('all the updated files', singular=False)
            elif msg.modified_files == 1 and iteration == 1:
                subject = NounPhrase('one updated file')
            elif msg.modified_files == 1 and iteration > 1:
                subject = NounPhrase('another updated file')
            elif iteration > 1:
                subject = NounPhrase('some other updated files', singular=False)
            else:
                subject = NounPhrase('some updated files', singular=False)
            s1 = ChangesFromDirectory(subject, directory)
        else:
            subject = NounPhrase('', singular=(len(msg)==1))
            s1 = NumberOfFiles(len(msg), action='updated',
                              directory=Directory(msg.dirname))

        s2 = HaveExtension(subject, msg.file_extensions)
        s = Sentence(AndJoin(s1, s2))

        sentences.append(s)

        # Files added
        added_sentence = None
        if msg.added_files == 1:
            subject = NounPhrase('a new file')
        elif msg.added_files > 1:
            subject = NounPhrase('some files', singular=False)

        if msg.added_files > 0:
            s1 = AddedToDir(subject, directory)
            s2 = HaveExtension(subject, msg.added_file_extensions)
            if msg.modified_files:
                s = Sentence(InlineJoin(s1, s2), additional_begin='also, ')
            else:
                s = Sentence(InlineJoin(s1, s2))
            added_sentence = s

        # Files deleted
        deleted_sentence = None
        if msg.deleted_files == 1:
            subject = NounPhrase('a file')
        elif msg.deleted_files > 1:
            subject = NounPhrase('some files', singular=False)

        if msg.deleted_files > 0:
            s1 = DeletedFromDir(subject, directory)
            s2 = HaveExtension(subject, msg.deleted_file_extensions)
            if msg.modified_files and not msg.added_files:
                s = Sentence(InlineJoin(s1, s2), additional_begin='also, ')
            else:
                s = Sentence(InlineJoin(s1, s2))
            deleted_sentence = s

        if added_sentence and deleted_sentence:
            s = SentencesAndJoin(added_sentence, deleted_sentence)
            sentences.append(s)
        elif added_sentence:
            sentences.append(added_sentence)
        elif deleted_sentence:
            sentences.append(deleted_sentence)

        # Changes distribution
        s1 = ChangesDistribution(len(msg), msg.additions, msg.deletions,
                                 msg.modifications)
        s = Sentence(s1)
        sentences.append(s)

        # create paragraph and add to final text
        p = Paragraph(*sentences)
        paragraphs.append(p)
        iteration += 1
    return paragraphs
