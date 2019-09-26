import argparse
import datetime
import random

def generate_string(num_chars):
    numbers = []
    for _ in range(num_chars):
        numbers.append(str(random.randrange(0, 10)))

    return "".join(numbers)

def generate(filename, filesize):

    numbers = []

    filesize_in_bytes = filesize * 1024 * 1024

    num_chars_per_line = 5 + 1 # endline
    size_per_char = 1
    num_lines = int(float(filesize_in_bytes) /
        float(num_chars_per_line * size_per_char))

    progress = int(float(num_lines) / 20.0)

    print ("Generating {} numbers to fit into {} MB".format(
        num_lines,
        filesize))

    for i in range(num_lines):
        if i % progress == 0:
            print ("{} {}%".format(
                datetime.datetime.now(),
                i / progress * 5))

        numbers.append(generate_string(5))

    print ("Finished generating {}".format(len(numbers)))
    print ("Saving to file {}".format(filename))
    with open(filename, "w") as f:
        data = "\n".join(numbers)
        f.write(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate numbers')

    parser.add_argument("-o", "--output",
        help='output file',
        dest='output',
        required=True)

    parser.add_argument("-s", "--size",
        help='file size in MB',
        dest='size',
        required=True)

    args = parser.parse_args()

    filename = args.output
    filesize = int(args.size)
    generate(filename, filesize)
