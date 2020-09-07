# ask.python
A simple ask function and factory written in python for use as module or from CLI.

## Installation as command
```
git clone <this repository>
cp ./pythonask/ask.python /some/place/in/path/
chmod +x /some/place/in/path/ask.py  # to use from command line
````

## Usage from command line
```
$ ./ask.py "Do you want to continue[Yes, Quit]?"
Do you want to continue [yes, quit]? q
quit

$ ./ask.py "Do you want to continue?" -r No,nEver
Do you want to continue [no, nEver]? E
never
```

## Help usage
```
$ ask --help
ask.py (version 0.1b) -- query a stdin response.
Usage: ask.py [options] question message
Options:
  -?,-h,--help            Prints this text.
  -a,--accepted=answers   Comma seperated accepted answers.
  -d,--default=default    Use default answer if empty response.
  -i,--input=file         Read input from file.
  -n,--tries=tries        The number of tries before using default.
  -o,--output=file        Send output to file.
  -p,--previous=answer    The previous answer (maintain state).
  -q,-quiet               Set verbosity to 0.
  -v,-vv,-vvv,-vvvv       Set verbosity to 1, 2, 3, 4.
  --                      Terminates argument parsing.
Arguments:
  question                The question to ask.
  message                 The rejected response message.
Notes:
  * A dash("-") can be used to represent an empty argument.
  * The "accepted" argument is optional only if embedded as a 
    comma seperated encapsulated("[", "]") list in the question.
  * Accepted answers may include a capitalize letter to offer 
    single character responses.  Otherwise answers will match 
    only the first n characters of input.
  * Verbosity is set using "-v" and "-q", multiple v's may be 
    used with a single dash("-"), where "-q"=silent, 
    "-v"=errors, "-vv"=normal and "-vvv"=debug.
```

## Simple usage from python
```
from ask import ask
answer = ask("Continue?", "Yes, No")
```

## Factory usage from python
```
import ask
query = ask.new("Continue?", "Yes, No")
answer = query()
```

