# bflang
A custom language which compiles to brainfuck.

# How To Use:
Have a project in a folder, and have a "main.bfl" file in the folder.
"python main.py [folder]" - generates an out.bf file in [folder] 

# Syntax highlighting support for vscode:
https://github.com/CupOfJoeCode/bflang-vscode

# Instruction List:
(*var*iables can not be the same in one instruction, or it will break)
* **malloc** *var*,*var*,...;
* **copy** *var*/*const* -> *var*;
* **inc** *var*, *const*;
* **dec** *var*, *const*;
* **add** *var*, *var* -> *var*;
* **sub** *var*, *var* -> *var*;
* **mul** *var*, *var* -> *var*;
* **div** *var*, *var* -> *var*;
* **mod** *var*, *var* -> *var*;
* **putc** *var*;
* **getc** *var*;
* **printint** *var*;
* **while**(*var*) { (*var*) }
* **if**(*var*) { (*var*) } (if is the same as while, just used to make code look nicer)
* **and** *var*, *var* -> *var*; (logic)
* **or** *var*, *var* -> *var*; (logic)
* **not** *var* -> *var*; (logic)
* **equal** *var*, *var* -> *var*;
* **nequal** *var*, *var* -> *var*;
* **greater** *var*, *var* -> *var*;
* **less** *var*, *var* -> *var*;

# Preprocessor Directive List:
* **@define** [NAME] [value]
* **@incmacro** [file]
* **@prints** [*var*] Some sort of string

# Structure of a program:
```malloc var1, var2, var3; \This is where you declare variables\

\This is a comment\ 

@define VALUE 10

main {
    \This is where code goes\
    while(var1) {

    (var) } \While and if statements must be closed with the name of the variable\

    printint var2; \Instructions should end in ";"\

    if(var2) {
        copy 0 -> var2; \If statements function as while statements
        and it is good practice to end them with setting the variable to 0\
    (var2) } 
}```