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


def new(question, accepted=None, default=None, message=None, tries=100):
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
        raise ValueError("Invalid accepted argument.")
    accepted = tuple(s for s in (s.strip() for s in accepted) if s)
    fc = lambda s: ''.join(c.lower() if c.isupper() else '' for c in s)[:1] \
            or None
    singles = tuple(fc(s) for s in accepted)
    accepted = tuple(s.lower() for s in accepted)
    question = "{:s} [{:s}]{:s} " \
            .format(question, ", ".join(accepted), punctuation or "?")

    def ask(answer=None, verbosity=2):
        nonlocal accepted, default, message, question, singles, tries
        if verbosity < 2:
            if answer not in accepted and answer not in singles:
                answer = default or accepted[0] or None
        else:
            try_count = 0
            while answer not in accepted and try_count < tries:
                answer = input(question).lower()
                if answer:
                    if len(answer) == 1 and answer.lower() in singles:
                        return accepted[singles.index(answer)]
                    for a in accepted:
                        if answer == a[:len(answer)]:
                            return a
                try_count += 1
                if message and type(message) is str:
                    print(message)
            else:
                answer = default or accepted[0] or None
        return answer

    return ask


def ask(question, answer=None, accepted=None, default=None,
        message=None, verbosity=2, tries=100):
    return new(question, accepted, default, message, tries) \
            (answer, verbosity)

def ask_help():
    print('Usage: ask [options] question default message')
    print('question        The question to ask')
    print('accepted       *Accepted answers (comma seperated)')
    print('default         The default answer used for no response')
    print('message         The reject response message')
    print('Options:')
    print('  -a answer   **The previous answer (for maintaining state).')
    print('  -n tries    **The number of tries.')
    print('  -r accepted   Comma seperated accepted responses.')
    print('  -v            Increase verbosity.')
    print('  -q            Decrease verbosity.')
    print('  -?,-h,--help  Prints this message.')
    print('Notes:')
    print('  * The accepted argument is optional only if accepted ')
    print('     values are comma seperated and "[", "]" encapsulated ')
    print('    within the question.')
    print('  * The accepted understands captiol letters as single ')
    print('    character that will be expanded to a full response.  ')
    print('    Otherwise it will match only the first n characters ')
    print('    against the accepted answers.')
    print(' ** All options that require a value are space delimited, ')
    print('    equal symbols("=") are not accepred.')


def main():
    from sys import argv
    args, kwargs = list(argv[1:]), { "verbosity" : 2, "answer": None }
    argi, argc = 0, len(args)
    showhelp, exitvalue, out, err = False, 0, sys.stdout, sys.stderr
    while argi < argc and exitvalue == 0:
        arg = args[argi]
        if arg.startswith("-"):
            if len(arg) > 1:
                args.pop(argi)
                if arg.startswith("-v") and all(c == 'v' for c in arg[1:]):
                    kwargs["verbosity"] += len(arg) - 1
                elif arg.startswith("-q") and all(c == 'q' for c in arg[1:]):
                    kwargs["verbosity"] -= len(arg) - 1
                elif arg == "-a" and argi + 1 < argc:
                    kwargs["answer"] = args.pop(argi)
                    argc -= 1
                elif arg == "-n" and argi + 1 < argc:
                    kwargs["tries"] = int(args.pop(argi))
                    argc -= 1
                elif arg == "-r" and argi + 1 < argc:
                    kwargs["accepted"] = args.pop(argi)
                    argc -= 1
                elif arg in ("-?", "-h", "--help"):
                    showhelp = True
                else:
                    print("bad switch or option: {:}".format(arg), file=err)
                    showhelp = True
                    exitvalue = -1
                argc -= 1
                continue
            args[argi] = None
        argi += 1
    if argc == 0 or showhelp:
        ask_help()
    elif exitvalue == 0:
        try:
            answer = ask(*args, **kwargs)
            print(answer)
        except ValueError as ve:
            exitvalue = -1
            print("Error: {:}".format(str(ve)), file=err)
            ask_help()
    exit(exitvalue)


if __name__ == '__main__':
    main()
