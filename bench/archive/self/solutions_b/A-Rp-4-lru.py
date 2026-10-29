class _Node:
    __slots__ = 'key', 'val', 'prev', 'next'
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        # Dummy nodes for the doubly linked list
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        p = node.prev
        n = node.next
        p.next = n
        n.prev = p

    def _add_to_front(self, node):
        # Insert right after the dummy head
        first_node = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = first_node
        first_node.prev = node

    def get(self, key: int) -> int:
        if self.capacity <= 0 or key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                # Evict least recently used (node before dummy tail)
                lru_node = self.tail.prev
                self._remove(lru_node)
                del self.cache[lru_node.key]
            
            new_node = _Node(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)
