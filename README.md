# ask.python
A simple ask function and factory written in python for use as module or from CLI.

## Installation as command
```
git clone <this repository>
cp ./pythonask/ask.python/ask.py /some/place/in/python/paths/ # module
cp ./pythonask/ask.python/ask /some/place/in/bin/paths/       # command
# The following is optional, but allows you to run it as a command instead
# of prefixing it as "python ask ..."
chmod 755 ./pythonask/ask.python/ask
````

## Usage from the command line
```
$ ask "Do you want to continue[Yes, Quit]?" -- simple use.
Do you want to continue [Yes, quit]? q
quit

$ ask "Do you accept these terms?" -a No,nEver,maybe -- with "--accepted" option.
Do you accept these terms [no, nEver, maybe]? E
never

$ ask "Are you hungry [Yes, No]?" -n=3 "Huh?" -- give up after 3 attempts
Are you hungry [Yes, no]? Feed me
Huh?
Are you hungry [Yes, no]? sometimes
Huh?
Are you hungry [Yes, no]? Always
yes

$ ask --help
ask.py (version 0.1b) -- query a stdin response.
Usage: ask.py [options] question message
Options:
  -?,-h,--help           Prints this text.
  -a,--accepted=answers  Comma seperated accepted answers.
  -d,--default=answer    Use default answer if empty response.
  -i,--input=file        Read input from file.
  -n,--tries=tries       The number of tries before using default.
  -o,--output=file       Send output to file.
  -p,--previous=answer   The previous answer (maintain state).
  -q,--quiet             Set verbosity to 0.
  -v,-vv,-vvv,-vvvv      Set verbosity to 1, 2, 3, 4, respectively.
  --                     Terminates argument parsing.
Arguments:
  question               The question to ask.
  message                The rejected response message.
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
answer = ask("Continue[Yes, No]?", "Please answer Yes or No")
```

## Factory usage from python
```
import ask
query = ask.new("Continue?", accepted="Yes, No")
answer = query()
```

## Contributing
If you want to support our efforts, we accept paypal.
If you're interested in making a contribution, go ahead and clone this
archive, and make a push request.  We especially need a test suite to maintain
a bug free module, if you're interested in contributing one.
