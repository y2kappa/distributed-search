import glob
import argparse
import datetime

class Heap:
    def __init__(self):
        self.data = []

    def push(self, key, val):
        self.data.append((key, val))

    def _get_smallest_index(self):

        index = 0
        min_key = self.data[0][0]
        i = 0
        for key, val in self.data:
            if key < min_key:
                min_key = key
                index = i
            i += 1

        return index

    def _get_largest_index(self):

        index = 0
        min_key = self.data[0][0]
        i = 0
        for key, val in self.data:
            if key > min_key:
                min_key = key
                index = i
            i += 1

        return index

    def peak_smallest(self):
        return self.data[self._get_smallest_index()]

    def peak_largest(self):
        return self.data[self._get_largest_index()]

    def pop_smallest(self):
        return self.data.pop(self._get_smallest_index())

    def pop_largest(self):
        return self.data.pop(self._get_largest_index())

    def sorted_descending(self):
        self.data.sort(key=lambda r:r[0], reverse=True)
        return self.data

    def empty(self):
        return len(self.data) == 0

def batch_search(filename):
    print ("Batch search in {}".format(filename))

    def dump_to_file(filename, chunk_no, contents):
        filename = filename + "chunk"+str(chunk_no)+".txt"
        with open(filename, "w") as g:
            g.write(contents)
            print ("Dumped {} of size {} MB".format(
                filename,
                float(len(contents))/(1024.0 * 1024.0)
            ))

    def split_file(filename):
        max_size = 20 # megabytes

        print ("Splitting file {} in {} MB chunks".format(
            filename, max_size))

        one_char_size = 1 # bytes
        max_bytes = 20 * 1024 * 1024
        max_chars = max_bytes / one_char_size

        contents = ""
        with open(filename) as f:

            chunk = 0
            while True:
                line = f.readline()

                if len(contents) + len(line) > max_chars:
                        dump_to_file(filename, chunk, contents)
                        contents = line
                        chunk += 1
                else:
                    contents += line

                if len(line) == 0:
                    if len(contents) > 0:
                        dump_to_file(filename, chunk, contents)
                    break

    def sort_files(filename):
        print ("Sorting subfiles of {}".format(filename))

        def is_sorted_file(filename):
            data = []
            with open(filename) as f:
                data = f.read().splitlines()

            for i in range(1, len(data)):
                if data[i-1] > data[i]:
                    return False

            return True

        def sort_file(filename):
            with open(filename) as f:
                data = f.read().splitlines()
                data = sorted(data)
            with open(filename, "w") as f:
                f.write("\n".join(data))

        for filename in glob.glob(filename+"chunk*"):
            print("Sorting {}".format(filename))

            sort_file(filename)

            print("Sorted {} {} ".format(
                filename,
                is_sorted_file(filename)))


    def multiway_merge(filename):
        print ("Merging & collapsing sorted files of {}".format(
            filename))

        filenames = []
        for chunkfilename in glob.glob(filename+"chunk*"):
            filenames.append(chunkfilename)
        openfiles = {}
        for chunkfilename in filenames:
            openfiles[chunkfilename] = open(chunkfilename)

        current_values = Heap()

        for fname, f in openfiles.items():
            line = f.readline()
            if len(line) != 0:
                line = line.replace("\n", "")
                current_values.push(line, fname)

        current_value, current_file = current_values.peak_smallest()
        current_count = 0
        output_file = open(filename+"merged_dictionary.txt", "w")

        count = 0
        while not current_values.empty():
            count += 1
            val, fname = current_values.pop_smallest()

            if val == current_value:
                current_count += 1
            else:
                output_file.write(str(current_value) + "-" + str(current_count) + "\n")
                current_value = val
                current_count = 1

            line = openfiles[fname].readline()
            if len(line) != 0:
                line = line.replace("\n", "")
                current_values.push(line, fname)

            if count % 100000 == 0 and current_count == 1:
                print ("{} Merging, reached count {}".format(
                    datetime.datetime.now(), count))

        for _, f in openfiles.items():
            f.close()

        output_file.close()

    def get_top_values(filename):
        print ("Heapifying the merged dictionary file of {}".format(
            filename))

        li = []
        rank = 15

        top = Heap()

        with open(filename+"merged_dictionary.txt") as f:
            while rank >= 0:
                line = f.readline().replace("\n", "")
                if len(line) == 0:
                    continue
                try:
                    val = line.split("-")[0]
                    count = int(line.split("-")[1])
                except Exception as e:
                    print (e)
                    print (line)
                    print (line.split("-"))

                top.push(count, val)
                rank -= 1

            while True:
                line = f.readline().replace("\n", "")
                if len(line) == 0:
                    break
                current_val = line.split("-")[0]
                current_count = int(line.split("-")[1])
                smallest_count, smallest_value = top.peak_smallest()
                if current_count > smallest_count:
                    top.pop_smallest()
                    top.push(current_count, current_val)

            top = top.sorted_descending()
            top = [(str(x) + " times for " + str(y)) for x, y in top]
            for v in top:
                print (v)


    # split file in chunks
    split_file(filename)

    # sort the split files
    sort_files(filename)

    # merge files
    multiway_merge(filename)

    # get top values
    get_top_values(filename)

def brute_force(filename):
    print ("Brute force search in {}".format(filename))

    data = []
    with open(filename) as f:
        data = f.read().splitlines()

    progress = int(float(len(data)) / 20.0)

    dictionary = {}
    max_count = 0
    max_value = None

    i = 0
    print ("Brute force searching through {} values".format(len(data)))
    for value in data:

        i += 1
        if i % progress == 0:
            print ("{} {}% Current Max Val {} Current Max Count {} Out of {} numbers".format(
                datetime.datetime.now(),
                i / progress * 5,
                max_value,
                max_count,
                i))

        if value in dictionary:
            dictionary[value] += 1
        else:
            dictionary[value] = 1

        if dictionary[value] > max_count:
            max_value = value
            max_count = dictionary[value]

    print ("-- Intermediary results -- ")
    print ("Done through {} numbers".format(len(data)))
    print ("Max occurrences {}".format(max_count))
    print ("Max value {}".format(max_value))
    print ("Dictionary size {}".format(len(dictionary)))
    print ("-- /Intermediary results -- ")

    print ("Heapifying the dictionary ...")

    top = Heap()
    rank = 15

    for val, count in dictionary.items():
        top.push(count, val)
        rank -= 1
        if rank < 0:
            break


    for val, count in dictionary.items():
        (smallest_count, smallest_val) = top.peak_smallest()
        if count > smallest_count:
            top.pop_smallest()
            top.push(count, val)

    top = top.sorted_descending()
    top = [(str(x) + " times for " + str(y)) for x, y in top]
    for v in top:
        print (v)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate numbers')

    parser.add_argument("-f", "--filename",
        help='input file',
        dest='filename',
        required=True)

    parser.add_argument("-b",
        help='brute force',
        dest='brute',
        action='store_true')

    args = parser.parse_args()

    filename = args.filename
    brute = args.brute

    if brute:
        brute_force(filename)
    else:
        batch_search(filename)
