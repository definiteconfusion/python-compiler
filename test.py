from utils import Compiler

def main():
    name = "Kevin"
    age = 30
    age1 = age + 1
    type_of_name = type(name)
    print(age, name)
    pass

Compiler = Compiler(main)
Compiler.compile(
    output_name="output",
    trace_stack=False,
    print_output=True
)