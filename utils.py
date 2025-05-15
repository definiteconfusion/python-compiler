import subprocess
import dis


############################
# Important: Need to add optional utility functions + imports for the rust file

# Type Function:
# `o_type": "fn o_type<T>(t: &T) -> String {\n    std::any::type_name::<T>().to_string()\n}`

############################


class Compiler:
    def __init__(self, function):
        self.instructions = dis.get_instructions(function)
        self.debug_stack = []
        self.main_stack = []
        self.transpiled_commands = []
        self.opcode_map = {
            100: "self.load_const(instruction)",
            125: "self.store_fast(instruction)",
            124: "self.load_fast(instruction)",
            122: "self.binary_operation(instruction)",
            116: "self.load_global(instruction)",
            171: "self.call_function(instruction)",
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
    
    def call_function(self, instruction):
        self.debug_print(instruction.opcode, instruction.argval)
        
        # Extract function arguments from the stack
        arg_count = instruction.arg
        args = []
        for _ in range(arg_count):
            if self.main_stack:
                args.append(self.main_stack.pop())
        
        # Get the function name
        if self.main_stack and self.main_stack[-1].com_type == "GLOBAL":
            function_name = self.main_stack.pop().argval
            
            # Handle specific functions
            if function_name == "print":
                self._handle_print_function(args)
            else:
                # For unsupported functions
                self.transpiled_commands.append(f"// Unsupported function: {function_name}")
    
    def _handle_print_function(self, args):
        # Format args for Rust println!
        if not args:
            self.transpiled_commands.append('println!();')
            return
            
        format_placeholders = []
        rust_args = []
        
        for arg in reversed(args):
            if arg.com_type == "FAST" or arg.com_type == "ADD" or arg.com_type == "SUB":
                format_placeholders.append("{}")
                rust_args.append((arg.argval, "FAST"))
            else:
                format_placeholders.append("{}")
                rust_args.append((arg.argval, "CONST"))
        
        format_string = " ".join(format_placeholders)
        # Convert Python args to Rust format, ensuring variables aren't quoted
        args_string = ""
        for idx, arg in enumerate(rust_args):
            # Check if this looks like a variable reference
            if arg[1] == "FAST":
                args_string += f"{arg[0]}"
            elif isinstance(arg[0], str):
                args_string += f'"{arg[0]}"'
            else:
                args_string += str(arg[0])
                
            # Add separator if not the last element
            if idx < len(rust_args) - 1:
                args_string += ", "
        
        self.transpiled_commands.append(f'println!("{format_string}", {args_string});')
        
                           
            
    def load_const(self, instruction):
        self.debug_print(instruction.opcode, instruction.argval)
        self.main_stack.append(self.Stack_Object.create(_type=type(instruction.argval), com_type="CONST", argval=instruction.argval))
        pass
    
    def store_fast(self, instruction):
        self.debug_print(instruction.opcode, instruction.argval)
        self.transpiled_commands.append(f'let mut {instruction.argval} = "{self.main_stack[-1].argval}";') if self.main_stack[-1]._type == str else self.transpiled_commands.append(f"let mut {instruction.argval} = {self.main_stack[-1].argval};")
        self.main_stack.append(self.Stack_Object.create(_type=type(instruction.argval), com_type="FAST", argval=instruction.argval))
        pass
    
    def binary_operation(self, instruction):
        self.debug_print(instruction.opcode, instruction.argval)
        if instruction.arg == 0:
            self.main_stack.append(self.Stack_Object.create(_type=None, com_type="ADD", argval=f"{self.main_stack[-2].argval} + {self.main_stack[-1].argval}"))
            self.main_stack.pop(-2)
            self.main_stack.pop(-2)
        elif instruction.arg == 10:
            self.main_stack.append(self.Stack_Object.create(_type=None, com_type="SUB", argval=f"{self.main_stack[-2].argval} - {self.main_stack[-1].argval}"))
            self.main_stack.pop(-2)
            self.main_stack.pop(-2)
        else:
            pass
    
    def load_fast(self, instruction):
        self.debug_print(instruction.opcode, instruction.argval)
        self.main_stack.append(self.Stack_Object.create(_type=type(instruction.argval), com_type="FAST", argval=instruction.argval))
        pass
    
    def load_global(self, instruction):
        self.debug_print(instruction.opcode, instruction.argval)
        self.main_stack.append(self.Stack_Object.create(_type=type(instruction.argval), com_type="GLOBAL", argval=instruction.argval))
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
                
        self.instructions
        
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