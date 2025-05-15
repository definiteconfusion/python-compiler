from utils import Compiler
import dis

def main():
    name = "Kevin"
    age = 30
    age1 = age + 1
    print(age, name, age1 - 1)
    pass

Compiler = Compiler(dis.get_instructions(main))
Compiler.compile(
    output_name="output",
    trace_stack=False,
    print_output=True
)