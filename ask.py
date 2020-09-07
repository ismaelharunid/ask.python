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


def ask_help(short=False):
    print('ask.py (version {:}) -- query a stdin response.'.format(ask_version))
    print('Usage: ask.py [options] question message')
    if short:
        return
    print('Options:')
    print('  -?,-h,--help            Prints this text.')
    print('  -a,--accepted=answers   Comma seperated accepted answers.')
    print('  -d,--default=default    Use default answer if empty response.')
    print('  -i,--input=file         Read input from file.')
    print('  -n,--tries=tries        The number of tries before using default.')
    print('  -o,--output=file        Send output to file.')
    print('  -p,--previous=answer    The previous answer (maintain state).')
    print('  -q,-quiet               Set verbosity to 0.')
    print('  -v,-vv,-vvv,-vvvv       Set verbosity to 1, 2, 3, 4.')
    print('  --                      Terminates argument parsing.')
    print('Arguments:')
    print('  question                The question to ask.')
    print('  message                 The rejected response message.')
    print('Notes:')
    print('  * A dash("-") can be used to represent an empty argument.')
    print('  * The "accepted" argument is optional only if embedded as a ')
    print('    comma seperated encapsulated("[", "]") list in the question.')
    print('  * Accepted answers may include a capitalize letter to offer ')
    print('    single character responses.  Otherwise answers will match ')
    print('    only the first n characters of input.')
    print('  * Verbosity is set using "-v" and "-q", multiple v\'s may be ')
    print('    used with a single dash("-"), where "-q"=silent, ')
    print('    "-v"=errors, "-vv"=normal and "-vvv"=debug.')


def main():
    from sys import argv
    args, kwargs = list(argv[1:]), { }
    argi, argc = 0, len(args)
    showhelp, exitvalue = False, 0
    inp, out, err = sys.stdin, sys.stdout, sys.stderr
    def getargs(arg=None, t=str):
        nonlocal args
        result = None
        if type(arg) is str and '=' in arg:
            result = arg[arg.index('=') + 1:]
        if argi + 1 < argc:
            result = args.pop(argi + 1)
            argc -= 1
        if type(result) is str:
            result = None if result in ("-", "") else t(result)
        return result
    while argi < argc and exitvalue == 0:
        arg, argarg = args[argi], None
        if arg.startswith("-"):
            if arg == "--":
                args = args[:argi]
                break
            if len(arg) > 1:
                args.pop(argi)
                argc -= 1
                if '=' in arg:
                    i = arg.index('=') 
                    arg, argarg = arg[:i], arg[i+1:]
                if arg in ("-a", "--accepted"):
                    kwargs["accepted"] = getargs(argarg)
                elif arg in ("-d", "--default"):
                    kwargs["default"] = getargs(argarg)
                elif arg in ("-i", "--output"):
                    inp = getargs(argarg)
                    if inp is None:
                        inp = sys.stdin
                elif arg in ("-o", "--output"):
                    out = getargs(argarg)
                    if out is None:
                        out = sys.stdout
                elif arg in ("-p", "--previous"):
                    kwargs["previous"] = getargs(argarg)
                elif arg in("-q", "--quiet"):
                    kwargs["verbosity"] = 0
                elif arg in ("-n", "--tries"):
                    kwargs["tries"] = getargs(argarg, int)
                elif arg.startswith("-v") and all(c == 'v' for c in arg[1:]):
                    kwargs["verbosity"] = len(arg) - 1
                elif arg in ("-?", "-h", "--help"):
                    showhelp = True
                else:
                    print("[Error] bad switch or option: {:}".format(arg),
                          file=err)
                    showhelp = True
                    exitvalue = -1
                continue
            args[argi] = None
        argi += 1
    if argc > 2:
        print("[Error] extra arguments: {:}".format(', '.join(args[2:])),
              file=err)
        showhelp = True
        exitvalue = -1
    if argc == 0 or showhelp:
        ask_help()
    elif exitvalue == 0:
        if kwargs["verbosity"] >= 4:
            print("args: {:}".format(', '.join(repr(a) for a in args)), file=err)
            print("kwargs: {:}"
                  .format(', '.join("{:}: {:}"
                                    .format(repr(k), repr(a))
                                            for (k, a) in kwargs.items())),
                  file=err)
        try:
            answer = ask(*args, **kwargs)
            print(answer, file=out)
        except ValueError as ve:
            exitvalue = -1
            print("[Error] {:}".format(str(ve)), file=err)
            ask_help(True)
    exit(exitvalue)


if __name__ == '__main__':
    main()
