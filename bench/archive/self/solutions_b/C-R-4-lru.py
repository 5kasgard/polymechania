class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # maps key to [value, prev_key, next_key]
        # Using a doubly linked list approach with a dummy head and tail
        # to avoid null checks.
        self.head = object()
        self.tail = object()
        self.cache_nodes = {} # key -> node
        
        # Internal node structure
        class Node:
            def __init__(self, key=None, value=None):
                self.key = key
                self.value = value
                self.prev = None
                self.next = None

        self.dummy_head = Node()
        self.dummy_tail = Node()
        self.dummy_head.next = self.dummy_tail
        self.dummy_tail.prev = self.dummy_head
        self.map = {} # key -> Node

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map = {}
        
        class Node:
            def __init__(self, key=None, value=None):
                self.key = key
                self.value = value
                self.prev = None
                self.next = None
        
        self.Node = Node
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        prev = node.prev
        nxt = node.next
        prev.next = nxt
        nxt.prev = prev

    def _add_to_front(self, node):
        # Add right after dummy head
        nxt = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = nxt
        nxt.prev = node

    def get(self, key: int) -> int:
        if self.capacity <= 0 or key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._add_to_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        
        if key in self.map:
            node = self.map[key]
            node.value = value
            self._remove(node)
            self._add_to_front(node)
        else:
            if len(self.map) >= self.capacity:
                # Evict least recently used (the one before dummy tail)
                lru_node = self.tail.prev
                self._remove(lru_node)
                del self.map[lru_node.key]
            
            new_node = self.Node(key, value)
            self.map[key] = new_node
            self._add_to_front(new_node)

# Redefining to ensure clean structure for the final block
class LRUCache:
    class _Node:
        __slots__ = ['key', 'value', 'prev', 'next']
        def __init__(self, key=None, value=None):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map = {}
        self.head = self._Node()
        self.tail = self._Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        p = node.prev
        n = node.next
        p.next = n
        n.prev = p

    def _add_to_front(self, node):
        first = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = first
        first.prev = node

    def get(self, key: int) -> int:
        if self.capacity <= 0 or key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._add_to_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.map:
            node = self.map[key]
            node.value = value
            self._remove(node)
            self._add_to_front(node)
        else:
            if len(self.map) >= self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.map[lru.key]
            new_node = self._Node(key, value)
            self.map[key] = new_node
            self._add_to_front(new_node)
