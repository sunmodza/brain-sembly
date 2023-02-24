# brain-sembly

### This project is a programming language that will be compiled into Brainfuck. Actually, I don't even know how it will be used.
### Feel free to contribute to this. Try reading the source code to understand how it works or find a way to ask me.

## More info update later

## Example

CODE
```
from brainf import BrainF,opti_brain

d = BrainF(10)
d.execute_command("INPUT")
d.execute_command("PT IX")
d.execute_command("MOV 0")
d.execute_command("INPUT")
d.execute_command("PT IX")
d.execute_command("MOV 1")
d.execute_command("PT 0")
d.execute_command("ADDV 1")
d.execute_command("OUTPUT")
print(opti_brain(d._command))
```

RESULT
```
>>>>>>>>>>>>>>>>,[-<<<<<<<<<<<<<<<<+>>>>>>>>>>>>>>>>],[-<<<<<<<<<<<<<<<+>>>>>>>>>>>>>>>]<<<<<<<<<<<<<<<<[->>>>>>>>>>>>>>>+<<<<<<<<<<<<<<<]>>>>>>>>>>>>>>>[->>+<<<<<<<<<<<<<<<<<+>>>>>>>>>>>>>>>][-]<<<<<<<<<<<<<<[->>>>>>>>>>>>>>+<<<<<<<<<<<<<<]>>>>>>>>>>>>>>[->>+<<<<<<<<<<<<<<<<+>>>>>>>>>>>>>>][-]>>.<<<<<<<<<<<<<<<<<
```

