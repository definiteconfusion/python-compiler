from utils import Compiler

def main():
    name = "Kevin"
    age = 30 + 1 - 2
    for i in range(10):
        print(age, name)
    pass

Compiler = Compiler(main)
r_out = Compiler.compile(
    output_name="output",
    trace_stack=False,
    print_output=True,
    dev_mode=True,
)

print(r_out)
# main()