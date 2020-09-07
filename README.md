# pythonask
A simple ask function and factory written in python for use as module or from CLI.

## Installation as command
```
git clone <this repository>
cp ./pythonask/ask.py /some/place/in/path/
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
$ ./ask.py -h
Usage: ask [options] question default message
question        The question to ask
default         The default answer used for no response
message         The reject response message
Options:
  -a answer   **The previous answer (for maintaining state).
  -n tries    **The number of tries.
  -r responses  Comma seperated accepted responses 
  -v            Increase verbosity.
  -q            Decrease verbosity.
  -?,-h,--help  Prints this message.
Notes:
  * The accepted argument is optional only if accepted 
     values are comma seperated and "[", "]" encapsulated 
    within the question.
  * The Accepted understands captiol letters as single 
    character that will be expanded to a full response.  
    Otherwise it will match only the first n characters 
    against the accepted answers.
 ** All options that require a value are space delimited, 
    equal symbols("=") are not accepred.
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

