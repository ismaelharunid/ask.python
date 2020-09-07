#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys, re

try:
    from collections.abc import Sequence
except:
    # python2 version
    from collections import Sequence


ask_version = "0.1b"


def new(question="Continue?", message=None, accepted=None, default=None,
        tries=100, verbosity=2):
    pattern = r"^([^\[\]?:.]+)(?:\[([^\]]*)\]\s*)?(?:([?:.])\s*)?$"
    m = re.match(pattern, question) if question and type(question) is str \
            else None
    if m is None:
        raise ValueError("Invalid question")
    question, punctuation = m.group(1).strip(), m.group(3)
    if accepted is None:
        accepted = m.group(2)
    if type(accepted) is str:
        accepted = accepted.split(",")
    if not isinstance(accepted, Sequence):
        raise ValueError("Invalid or missing \"accepted\" argument.")
    accepted = tuple(s for s in (s.strip() for s in accepted) if s)
    fc = lambda s: ''.join(c.lower() if c.isupper() else '' for c in s)[:1] \
            or None
    singles = tuple(fc(s) for s in accepted)
    accepted = tuple(s.lower() for s in accepted)
    question = "{:s} [{:s}]{:s} " \
            .format(question, ", ".join(accepted), punctuation or "?")

    def ask(question=question, message=message, previous=None,
            tries=100, verbosity=verbosity):
        nonlocal accepted, default, singles
        if verbosity < 2:
            if previous not in accepted and previous not in singles:
                previous = default or accepted[0] or None
        else:
            try_count = 0
            while previous not in accepted and try_count < tries:
                previous = input(question).lower()
                if previous:
                    if len(previous) == 1 and previous.lower() in singles:
                        return accepted[singles.index(previous)]
                    for a in accepted:
                        if previous == a[:len(previous)]:
                            return a
                try_count += 1
                if message and type(message) is str:
                    print(message)
            else:
                previous = default or accepted[0] or None
        return previous

    return ask


def ask(question, message=None, accepted=None, default=None,
        tries=100, verbosity=2, previous=None):
    return new(question, message, accepted, default, tries, verbosity) \
            (previous=previous)

