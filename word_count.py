# word_count.py
# ===================================================
# Implement a word counter that counts the number of
# occurrences of all the words in a file. The word
# counter will return the top X words, as indicated
# by the user.
# ===================================================

import re
from hash_map import HashMap

"""
This is the regular expression used to capture words. It could probably be endlessly
tweaked to catch more words, but this provides a standard we can test against, so don't
modify it for your assignment submission.
"""
rgx = re.compile("(\w[\w']*\w|\w)")

def hash_function_2(key):
    """
    This is a hash function that can be used for the hashmap.
    """

    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash

def top_words(source, number):
    """
    Takes a plain text file and counts the number of occurrences of case insensitive words.
    Returns the top `number` of words in a list of tuples of the form (word, count).

    Args:
        source: the file name containing the text
        number: the number of top results to return (e.g. 5 would return the 5 most common words)
    Returns:
        A list of tuples of the form (word, count), sorted by most common word. (e.g. [("a", 23), ("the", 20), ("it", 10)])
    """

    keys = set()
    keys_list = []
    max_count = 1

    ht = HashMap(2500,hash_function_2)

    # This block of code will read a file one word as a time and
    # put the word in `w`. It should be left as starter code.
    with open(source) as f:
        for line in f:
            words = rgx.findall(line)
            for w in words:
                w = w.lower()

                if w in keys:
                    # determine the current count
                    count = keys_list.count(w)

                    # remove the word from the hash table
                    ht.remove(w, count)

                    # put the link in the new bucket (buckets are assigned according to count, not word)
                    ht.put(w, count + 1, True)
                    if count + 1 > max_count:
                        max_count = count + 1
                else:
                    ht.put(w, 1, True)
                    keys.add(w)  # sets don't allow duplicates, so only add if it's a new word
                # add every key, whether or not it already exists, so we can easily get the count each time
                keys_list.append(w)

    # get the top used words by grabbing them from the buckets from the highest index down
    results = []
    number_reached = False
    for i in range(max_count, 1, -1):
        bucket = ht.get_bucket_by_key(i)
        if bucket is not None and not bucket.is_empty():
            for link in bucket:
                if link.value == i:
                    results.append((link.key, link.value))
                    if len(results) == number:
                        number_reached = True
                        break
        if number_reached:
            break
    return results







# print(top_words("alice.txt",10))  # COMMENT THIS OUT WHEN SUBMITTING TO GRADESCOPE