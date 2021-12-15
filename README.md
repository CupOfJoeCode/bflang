# bflang
A custom language which compiles to brainfuck.

# How To Use:
Have a project in a folder, and have a "main.bfl" file in the folder.
"python main.py [folder]" - generates an out.bf file in [folder] 

# Instruction List:
(variables can not be the same in one instruction, or it will break)
* **copy** var/const -> var;
* **inc** var, const;
* **dec** var, const;
* **add** var, var -> var;
* **sub** var, var -> var;
* **mul** var, var -> var;
* **div** var, var -> var;
* **mod** var, var -> var;
* **putc** var;
* **getc** var;
* **printint** var;
* **while**(var) { (var) }
* **if**(var) { (var) } (if is the same as while, just used to make code look nicer)
* **and** var, var -> var; (logic)
* **or** var, var -> var; (logic)
* **not** var -> var; (logic)
* **equal** var, var -> var;
* **nequal** var, var -> var;
* **greater** var, var -> var;
* **less** var, var -> var;

# Preprocessor Directive List:
* @define [NAME] [value]
* @incmacro [file]
* @prints [var] Some sort of string