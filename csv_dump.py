import dis
import csv
from test import main
        
with open('disassembly.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header row with all attributes
    writer.writerow(['opname', 'opcode', 'arg', 'argval', 'argrepr', 'offset', 'starts_line', 'is_jump_target'])
    
    # Write all instruction attributes
    for instruction in dis.get_instructions(main):
        writer.writerow([
            instruction.opname,
            instruction.opcode,
            instruction.arg,
            instruction.argval,
            instruction.argrepr,
            instruction.offset,
            instruction.starts_line,
            instruction.is_jump_target
        ])