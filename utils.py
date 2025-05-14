import subprocess

class Compiler:
    def __init__(self, instructions):
        self.instructions = instructions
        self.debug_stack = []
        self.main_stack = []
        self.transpiled_commands = []
        self.opcode_map = {
            100: "self.load_const(instruction)",
            125: "self.store_fast(instruction)",
        }
        
    ###########################
    #
    ## Utility Functions
    #
    ###########################
        
    def debug_print(self, opcode, argval):
        self.debug_stack.append((opcode, argval))
        pass
    
    class Stack_Object:
        def __init__(self, _type=None, com_type=None, argval=None):
            self._type = _type
            self.com_type = com_type
            self.argval = argval
            
        @classmethod
        def create(cls, _type=None, com_type=None, argval=None):
            return cls(_type, com_type, argval)
            
    ###########################
    #
    ## OP Functions 
    #
    ###########################
            
    def load_const(self, instruction):
        self.debug_print(instruction.opcode, instruction.argval)
        self.main_stack.append(self.Stack_Object.create(_type=type(instruction.argval), com_type="CONST", argval=instruction.argval))
        pass
    
    def store_fast(self, instruction):
        self.debug_print(instruction.opcode, instruction.argval)
        self.transpiled_commands.append(f'let mut {instruction.argval} = "{self.main_stack[-1].argval}";') if self.main_stack[-1]._type == str else self.transpiled_commands.append(f"let mut {instruction.argval} = {self.main_stack[-1].argval};")
        self.main_stack.append(self.Stack_Object.create(_type=type(instruction.argval), com_type="FAST", argval=instruction.argval))
        pass
    
    ###########################
    #
    ## Compiler Functions
    #
    ###########################
    
    def compile(self, output_name, trace_stack=False, print_output=False):
        for instruction in self.instructions:
            if instruction.opcode in self.opcode_map:
                exec(self.opcode_map[instruction.opcode])
        if trace_stack:
            for item in self.main_stack:
                print(f"Type: {str(item._type):<15} Com Type: {str(item.com_type):<10} Argval: {str(item.argval)}")
            print("\n"*2)
            for item in self.transpiled_commands:
                print(item)
                
        with open(f"{output_name}.rs", "w") as f:
            f.write("fn main() {\n")
            for command in self.transpiled_commands:
                f.write(f"    {command}\n")
            f.write("}\n")
        try:
            subprocess.run(["rustc", f"{output_name}.rs", "-o", f"{output_name}"], check=True)
            if print_output:
                subprocess.run([f"./{output_name}"], check=True)
            return True
        except:
            print("Compilation failed. Please check your code.")
            return False