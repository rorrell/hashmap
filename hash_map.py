# hash_map.py
# ===================================================
# Implement a hash map with chaining
# ===================================================

class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedListIterator:
    def __init__(self, linked_list):
        self._linked_list = linked_list
        self._index = 0
        self._cur = self._linked_list.head

    def __next__(self):
        if self._cur is None:
            raise StopIteration
        result = self._cur
        self._index += 1
        self._cur = self._cur.next
        return result


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def is_empty(self):
        return self.head is None

    def __iter__(self):
        return LinkedListIterator(self)

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def get_bucket_by_index(self, index):
        """
        Retrieve a bucket by its index
        :param index: The desired bucket's index
        :return: The associated bucket, if it exists, else None
        """
        if index < 0 or index > self.capacity - 1:
            return None
        return self._buckets[index]

    def get_bucket_index_by_key(self, key: any, capacity: any = None) -> int:
        """
        Determines the appropriate bucket for a given key
        :param capacity: the capacity of array that the hashed key will be fit to.  defaults to None, in which case it
            will be set to self.capacity
        :param key: The value that gets hashed to determine the bucket
        :return: The linked list for the appropriate bucket
        """
        if capacity is None:
            capacity = self.capacity
        hash_result = self._hash_function(str(key))
        if hash_result > capacity - 1:  # if the result is outside the array capacity, fit it to the array size
            hash_result %= capacity
        return hash_result

    def get_bucket_by_key(self, key: any) -> LinkedList:
        """
        Determines the appropriate bucket for a given key
        :param key: The value that gets hashed to determine the bucket
        :return: The linked list for the appropriate bucket
        """
        hash_result = self.get_bucket_index_by_key(key)
        return self._buckets[hash_result]

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """
        for bucket in self._buckets:
            bucket.head = None  # cut off all data from each linked list

    def get(self, key, valToHash=None):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
            :param valToHash: provides the value to hash to determine the bucket, if different from the key
        Return:
            The value associated to the key. None if the link isn't found.
        """
        bucket = self.get_bucket_by_key(key if valToHash is None else valToHash)
        node = bucket.contains(key)
        return node if node is None else node.value

    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """
        # create a new set of buckets
        new_table = []
        for i in range(capacity):
            new_table.append(LinkedList())

        for bucket in self._buckets:
            for node in bucket:
                # rehash each node based on the new capacity
                new_bucket_index = self.get_bucket_index_by_key(node.key, capacity)
                new_table[new_bucket_index].add_front(node.key, node.value)
        # assign the new bucket list and new capacity to self
        self._buckets = new_table
        self.capacity = capacity

    def put(self, key, value, useValueToDetermineBucket=False):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            :param key: they key to use to has the entry
            :param value: the value associated with the entry
            :param useValueToDetermineBucket: set this to True if you want to hash the value instead of the key when
                determining the bucket to use.  Defaults to False.
        """
        # find the appropriate bucket
        bucket = self.get_bucket_by_key(key if not useValueToDetermineBucket else value)

        # determine whether the key exists in the bucket
        node = bucket.contains(key)
        if node is None:  # if not, add at front
            bucket.add_front(key, value)
            self.size += 1
        else:  # if so, update the value
            node.value = value

    def remove(self, key, valToHash=None):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            :param key: they key to search for and remove along with its value
            :param valToHash: the value to hash to determine the bucket from which to remove; defaults to None, which
                will just hash the key parameter.
        """
        # find the appropriate bucket
        bucket = self.get_bucket_by_key(key if valToHash is None else valToHash)

        # remove the given key if it is present
        bucket.remove(key)  # returns True or False, but no need to return that to caller of this method

    def contains_key(self, key: any) -> bool:
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """
        # check each bucket for the key until it is found or until the whole thing has been searched
        for bucket in self._buckets:
            if bucket.contains(key):
                return True
        return False

    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """
        # go through the buckets and count the empty ones
        num_empty = 0
        for bucket in self._buckets:
            if bucket.is_empty():
                num_empty += 1
        return num_empty

    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        return float(self.size) / float(self.capacity)  # forcing a float return type

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out
