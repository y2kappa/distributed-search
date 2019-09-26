# distributed-search

Contents:
1. Problem
2. Solution explanation
3. Run commands

## Problem
Find most occurrences of file that does not fit in memory.

## Solution explanation

This is essentially a file based n-way merge sort. Pseudocode:
```py

# 1. Split in chunks by reading one line at a time
chunked_files = split_big_file_in_chunks(
    file,
    max_size_in_mb)

# 2. Sort chunked files
for f in chunked_files:
    sort_file(f)

# 3. N Way merge, create a file based dictionary with frequencies

# firstly, read first value in each file
heap = Heap()
for f in chunked_files:
    heap.push(f.readline(), 1) # 1 count for each first word

# then, look through each file and pop the highest when it no
# longer exists in that file
current_val, current_file = heap.peak()
current_count = 0
while True:
    smallest_val, smallest_file = heap.pop()
    new_val = smallest_file.readline()
    if new_val == smallest_val:
        current_count++
        heap.push(smallest_val, smallest_file)
    else:
        dictionary_file.write(smallest_val + "-" + current_count)
        current_count = 0

# 4. Neap to get top values
heaptop = Heap()
for l in dictionary_file.read().splitlines():
    heaptop.push(l)
    ...

```

1. Split file in n chunks of 20MB each

```
abc
aab
aaa
```
2. Sort each chunk file

```
aaa
aaa
aab
```

3. Merge all chunks in a single file using a rolling heap and collapse values, ending up with a disk based dictionary. Still sorted lexicographically, but not by frequency.
```
aaa-2
aab-3
```
4. Iterate through the disk based dictionary and build a max heap keyed by frequency. End up with top 15 values.

## Run commands

Generate 500 MB worth of random numbers
```sh
$ python problem.py -o newdata.txt -s 500
```

Find the brute force solution if it fits you memory.
```sh
$ python solution.py -f newdata.txt -b

Brute force search in newdata.txt
Brute force searching through 87381333 values
2019-09-26 23:53:17.732893 5.0% Current Max Val 45508 Current Max Count 74 Out of 4369066 numbers
2019-09-26 23:53:21.111523 10.0% Current Max Val 68798 Current Max Count 136 Out of 8738132 numbers
...

-- Intermediary results --
Done through 87381333 numbers
Max occurrences 1001
Max value 97020
Dictionary size 100000
-- /Intermediary results --

Heapifying the dictionary ...
1001 times for 97020
997 times for 62954
994 times for 99552
990 times for 39261
988 times for 30752
987 times for 66178
987 times for 55599
987 times for 40148
986 times for 97565
985 times for 91387
985 times for 10074
984 times for 40296
984 times for 40865
984 times for 57789
984 times for 86451
983 times for 91098
```

Find the memory friendly solution
```sh
$ python solution.py -f newdata.txt
Batch search in newdata.txt
Splitting file newdata.txt in 20 MB chunks
Dumped newdata.txtchunk0.txt of size 19.999998092651367 MB
...
Sorting subfiles of newdata.txt
Sorting newdata.txtchunk7.txt
Sorted newdata.txtchunk7.txt True
Sorting newdata.txtchunk6.txt
...
Merging & collapsing sorted files of newdata.txt
2019-09-27 00:00:36.521639 Merging, reached count 33800000
2019-09-27 00:00:55.066465 Merging, reached count 39400000
2019-09-27 00:02:06.126490 Merging, reached count 61200000
Heapifying the merged dictionary file of newdata.txt
1001 times for 97020
997 times for 62954
994 times for 99552
990 times for 39261
988 times for 30752
987 times for 40148
987 times for 55599
987 times for 66178
986 times for 97565
985 times for 10074
985 times for 91387
984 times for 40296
984 times for 40865
984 times for 57789
984 times for 86451
983 times for 91098

```
