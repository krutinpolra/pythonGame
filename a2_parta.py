#Main Author(s): KRUTIN BHARATBHAI POLRA
#Main Reviewer(s): DHARAM MEHULBHAI GHEVARIYA

class HashTable:
    """
    A hash table implementation using linear probing for collision resolution.

    Attributes:
        cap (int): The initial capacity of the hash table (default is 32).
        table (list): The internal list storing key-value pairs.
        size (int): The current number of elements in the hash table.
    """

    def __init__(self, cap=32):
        """
        Initialize the hash table with a given capacity.

        Args:
            cap (int): The initial capacity of the hash table. Must be positive. Default is 32.

        Initializes an internal table with the specified capacity and sets the initial size to 0.
        """
        self.cap = cap
        self.table = [None] * self.cap
        self.size = 0

    def insert(self, key, value):
        """
        Insert a key-value pair into the hash table.

        Args:
            key (any): The key to be inserted. Must be hashable.
            value (any): The value associated with the key.

        Returns:
            bool: True if the key-value pair was inserted successfully, False if the key already exists.

        Triggers a resize if the load factor exceeds 0.7 after insertion.
        """
        index = hash(key) % self.cap
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return False
            index = (index + 1) % self.cap

        self.table[index] = (key, value)
        self.size += 1

        if self.size / self.cap > 0.7:
            self._resize()

        return True

    def _resize(self):
        """
        Resize the hash table to double its current capacity.

        Rehashes all existing key-value pairs to ensure proper distribution in the new table.
        """
        new_cap = self.cap * 2
        new_table = [None] * new_cap
        for item in self.table:
            if item is not None:
                key, value = item
                index = hash(key) % new_cap
                while new_table[index] is not None:
                    index = (index + 1) % new_cap
                new_table[index] = (key, value)
        self.cap = new_cap
        self.table = new_table

    def modify(self, key, value):
        """
        Modify the value associated with a given key.

        Args:
            key (any): The key to modify. Must be hashable.
            value (any): The new value to associate with the key.

        Returns:
            bool: True if the key was found and modified, False otherwise.
        """
        index = hash(key) % self.cap
        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = (key, value)
                return True
            index = (index + 1) % self.cap
        return False

    def remove(self, key):
        """
        Remove a key-value pair from the hash table.

        Args:
            key (any): The key to remove. Must be hashable.

        Returns:
            bool: True if the key was found and removed, False otherwise.

        Triggers rehashing of subsequent keys to maintain table consistency.
        """
        index = hash(key) % self.cap
        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = None
                self.size -= 1
                self._rehash(index)
                return True
            index = (index + 1) % self.cap
        return False

    def _rehash(self, index):
        """
        Rehash keys following a removed key to maintain proper table integrity.

        Args:
            index (int): The index from which rehashing starts.
        """
        next_index = (index + 1) % self.cap
        while self.table[next_index] is not None:
            key, value = self.table[next_index]
            self.table[next_index] = None
            self.size -= 1
            self.insert(key, value)
            next_index = (next_index + 1) % self.cap

    def search(self, key):
        """
        Search for a value associated with a given key.

        Args:
            key (any): The key to search for. Must be hashable.

        Returns:
            any: The value associated with the key if found, or None if the key does not exist.
        """
        index = hash(key) % self.cap
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.cap
        return None

    def capacity(self):
        """
        Get the current capacity of the hash table.

        Returns:
            int: The current capacity of the hash table.
        """
        return self.cap

    def __len__(self):
        """
        Get the current number of elements in the hash table.

        Returns:
            int: The current size of the hash table.
        """
        return self.size
