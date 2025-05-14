import subprocess

class Compiler:
    def __init__(self, instructions):
        self.instructions = instructions
        self.opcodes = {
            100: "self.load_const(instruction)",
            125: "self.store_fast(instruction)",
            116: "self.load_global(instruction)",
            124: "self.load_fast(instruction)",
            171: "self.call_function(instruction)",
        }
        self.call_stack = {
            "print": "self.global_print()",
        }
        self.bin_stack = []
        self.global_stack = []
        self.fast_stack = {}
        self.debug_stack = []
        self.transpiled_commands = []
        
    def dprint(self, opcode, argval):
        self.debug_stack.append((opcode, argval))
        
    
    def call_function(self, instruction):
        if self.global_stack[-1] in self.call_stack:
            exec(self.call_stack[self.global_stack[-1]])
        else:
            raise ValueError(f"Function {instruction.argval} not found.")
        self.dprint(instruction.opname, instruction.argval)
    
    def load_const(self, instruction):
        self.bin_stack.append(instruction.argval)
        self.dprint(instruction.opname, instruction.argval)
        
    def load_fast(self, instruction):
        if instruction.argval in self.fast_stack:
            self.bin_stack.append(instruction.argval)
            self.dprint(instruction.opname, instruction.argval)
        else:
            raise ValueError(f"Variable {self.bin_stack[-1]} not found in fast stack.")
    
    def store_fast(self, instruction):
        self.fast_stack[instruction.argval] = self.bin_stack[-1]
        store_type = type(self.fast_stack[instruction.argval])
        types = {
            int: "int",
            str: "string",
            float: "float",
            bool: "bool",
        }
        self.transpiled_commands.append(
            (instruction.offset,
             f"let mut {instruction.argval} = {self.bin_stack[-1]};"  if store_type != str else f"let mut {instruction.argval} = \"{self.bin_stack[-1]}\";")
        )
        self.bin_stack.pop()
        self.dprint(instruction.opname, instruction.argval)
    
    def load_global(self, instruction):
        self.global_stack.append(instruction.argval)
        self.dprint(instruction.opname, instruction.argval)
        pass
    
    def global_print(self):
        self.transpiled_commands.append(
            (0, f"println!(\"{{}}\", {self.bin_stack[-1]});")
        )
        self.dprint("PRINT", self.bin_stack[-1])
        
    def compile(self, output_name="output", print_output=False):
        for instruction in self.instructions:
            if instruction.opcode in self.opcodes:
                exec(self.opcodes[instruction.opcode])
        with open(f"{output_name}.rs", "w") as f:
            f.write("#![allow(warnings)]\n")
            f.write("fn main() {\n")
            for command in self.transpiled_commands:
                f.write(f"    {command[1]}\n")
            f.write("}\n")
        try:
            subprocess.run(["rustc", f"{output_name}.rs", "-o", f"{output_name}"], check=True)
            if print_output:
                subprocess.run([f"./{output_name}"], check=True)
            return True
        except:
            print("Compilation failed. Please check your code.")
            return False