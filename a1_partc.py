#    Main Author(s): Dharam Mehulbhai Ghevariya
#    Main Reviewer(s): Krutin Bharatbhai Polra

class Stack:
    """Implements a stack data structure with dynamic resizing."""
	
    def __init__(self, cap=10):
        # Initializes the stack with a specified capacity (default is 10).
        self.used_ = 0
        self.capacity_ = cap
        self.stack = [None] * cap
	
    def __resize(self):
        # Doubles the stack's capacity when it is full.
        temp = [None] * (self.capacity_ * 2)
        temp[:self.used_] = self.stack
        self.stack = temp
        self.capacity_ *= 2

    def capacity(self):
        # Returns the current capacity of the stack.
        return self.capacity_

    def push(self, data):
        # Adds an item to the top of the stack.
        if self.used_ == self.capacity_:
            self.__resize()
        self.stack[self.used_] = data
        self.used_ += 1 

    def pop(self):
        # Removes and returns the top item of the stack.
        if self.used_ == 0:
            raise IndexError('pop() used on empty stack')
        self.used_ -= 1
        return self.stack[self.used_]        	    

    def get_top(self):
        # Returns the top item of the stack without removing it.
        return self.stack[self.used_ - 1]

    def is_empty(self):
        # Checks if the stack is empty.
        return self.used_ == 0

    def __len__(self):
        # Returns the number of items in the stack.
        return self.used_


class Queue:
    """Implements a queue data structure with dynamic resizing."""
	
    def __init__(self, cap=10):
        # Initializes the queue with a specified capacity (default is 10).
        self.capacity_ = cap
        self.used_ = 0
        self.frontIndx_ = 0
        self.backIndx_ = 0
        self.queue = [None] * self.capacity_
	
    def __resize(self):
        # Doubles the queue's capacity when it is full.
        temp = [None] * (self.capacity_ * 2)
        j = self.frontIndx_
        for i in range(self.used_):
            temp[i] = self.queue[j]
            j = (j + 1) % self.capacity_
        self.queue = temp
        self.capacity_ *= 2
        self.frontIndx_ = 0
        self.backIndx_ = self.used_

    def capacity(self):
        # Returns the current capacity of the queue.
        return self.capacity_

    def enqueue(self, data):
        # Adds an item to the back of the queue.
        if self.used_ == self.capacity_:
            self.__resize()
        self.queue[self.backIndx_] = data
        self.backIndx_ = (self.backIndx_ + 1) % self.capacity_
        self.used_ += 1

    def dequeue(self):
        # Removes and returns the front item of the queue.
        if self.used_ == 0:
            raise IndexError('dequeue() used on empty queue')
        self.used_ -= 1
        r_value = self.queue[self.frontIndx_]
        self.frontIndx_ = (self.frontIndx_ + 1) % self.capacity_
        return r_value 

    def get_front(self):
        # Returns the front item of the queue without removing it.
        if self.used_ == 0:
            return None
        return self.queue[self.frontIndx_]

    def is_empty(self):
        # Checks if the queue is empty.
        return self.used_ == 0

    def __len__(self):
        # Returns the number of items in the queue.
        return self.used_


class Deque:
    """Implements a double-ended queue (deque) with dynamic resizing."""
	
    def __init__(self, cap=10):
        # Initializes the deque with a specified capacity (default is 10).
        self.capacity_ = cap
        self.used_ = 0
        self.frontIndx_ = 0
        self.backIndex_ = 0
        self.deque = [None] * self.capacity_

    def __resize(self):
        # Doubles the deque's capacity when it is full.
        temp = [None] * (self.capacity_ * 2)
        j = self.frontIndx_
        for i in range(self.used_):
            temp[i] = self.deque[j]
            j = (j + 1) % self.capacity_
        self.deque = temp
        self.capacity_ *= 2
        self.frontIndx_ = 0
        self.backIndex_ = self.used_

    def capacity(self):
        # Returns the current capacity of the deque.
        return self.capacity_

    def push_front(self, data):
        # Adds an item to the front of the deque.
        if self.used_ == self.capacity_:
            self.__resize()
        self.frontIndx_ = (self.frontIndx_ - 1) % self.capacity_
        self.deque[self.frontIndx_] = data
        self.used_ += 1

    def push_back(self, data):
        # Adds an item to the back of the deque.
        if self.used_ == self.capacity_:
            self.__resize()
        self.deque[self.backIndex_] = data
        self.backIndex_ = (self.backIndex_ + 1) % self.capacity_
        self.used_ += 1

    def pop_front(self):
        # Removes and returns the front item of the deque.
        if self.used_ == 0:
            raise IndexError('pop_front() used on empty deque')
        self.used_ -= 1
        r_value = self.deque[self.frontIndx_]
        self.frontIndx_ = (self.frontIndx_ + 1) % self.capacity_
        return r_value

    def pop_back(self):
        # Removes and returns the back item of the deque.
        if self.used_ == 0:
            raise IndexError('pop_back() used on empty deque')
        self.used_ -= 1
        self.backIndex_ = (self.backIndex_ - 1) % self.capacity_
        return self.deque[self.backIndex_]

    def get_front(self):
        # Returns the front item of the deque without removing it.
        if self.used_ == 0:
            return None
        return self.deque[self.frontIndx_]

    def get_back(self):
        # Returns the back item of the deque without removing it.
        if self.used_ == 0:
            return None
        return self.deque[(self.backIndex_ - 1) % self.capacity_]

    def is_empty(self):
        # Checks if the deque is empty.
        return self.used_ == 0

    def __len__(self):
        # Returns the number of items in the deque.
        return self.used_

    def __getitem__(self, k):
        # Returns the item at the specified index in the deque.
        if not (0 <= k < self.used_):
            raise IndexError('Index out of range')
        return self.deque[(self.frontIndx_ + k) % self.capacity_]
