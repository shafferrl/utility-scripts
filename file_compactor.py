"""
Count lines containing non-whitespace characters
in a file and save to file without blank lines.
"""

# Specify input and output files
input_file = ''
output_file = ''

# Loop through and write each line to output if not blank
with open(input_file) as full_file:
    with open(output_file, 'w') as compact_file:
        line_count = 0
        for line in full_file:
            if line.strip():
                line_count += 1
                compact_file.write(line)
            else: continue

print(line_count)
