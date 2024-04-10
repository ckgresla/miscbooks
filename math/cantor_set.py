# cantor's set ala Measure Theory
# https://en.wikipedia.org/wiki/Cantor_set

def cantor_set_iterative(iterations):
    # Start with an initial line representing the set
    line_length = 81  # Adjust as needed for more detailed steps
    line = ['-'] * line_length

    def print_line(line):
        print(''.join(line))

    for i in range(iterations):
        # Divide every segment into thirds, and for each segment, remove the middle third
        third_length = line_length // (3 ** (i + 1))
        for start in range(0, line_length, 3 * third_length):
            for j in range(start + third_length, start + 2 * third_length):
                line[j] = ' '
        print(f"Step {i + 1}:")
        print_line(line)

# Specify the number of iterations you want to visualize
iterations = 4
cantor_set_iterative(iterations)

