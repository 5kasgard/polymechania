class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # maps key to [value, prev_key, next_key]
        # Using a doubly linked list approach with a dummy head and tail
        # to avoid null checks.
        self.head = object()
        self.tail = object()
        self.cache_nodes = {} # key -> node
        
        # Internal node structure: [key, value, prev, next]
        class Node:
            def __init__(self, key=None, value=None):
                self.key = key
                self.value = value
                self.prev = None
                self.next = None

        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.map = {} # key -> Node
        self.size = 0

    def _remove(self, node):
        p = node.prev
        n = node.next
        p.next = n
        n.prev = p

    def _add_to_front(self, node):
        # Add right after head (most recent)
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
            if self.size >= self.capacity:
                # Evict least recently used (node before tail)
                lru_node = self.tail.prev
                self._remove(lru_node)
                del self.map[lru_node.key]
                self.size -= 1
            
            new_node = self._Node(key, value)
            self.map[key] = new_node
            self._add_to_front(new_node)
            self.size += 1

    class _Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None

    # Redefining to ensure clean structure for the final implementation
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map = {}
        self.size = 0
        class Node:
            def __init__(self, k, v):
                self.key = k
                self.val = v
                self.prev = None
                self.next = None
        self.Node = Node
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        if self.capacity <= 0 or key not in self.map:
            return -1
        node = self.map[key]
        self._move_to_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.map:
            node = self.map[key]
            node.val = value
            self._move_to_front(node)
        else:
            if self.size == self.capacity:
                lru = self.tail.prev
                self._remove_node(lru)
                del self.map[lru.key]
                self.size -= 1
            
            new_node = self.Node(key, value)
            self.map[key] = new_node
            self._add_node(new_node)
            self.size += 1

    def _add_node(self, node):
        # Add after head
        nxt = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = nxt
        nxt.prev = node

    def _remove_node(self, node):
        prv = node.prev
        nxt = node.next
        prv.next = nxt
        nxt.prev = prv

    def _move_to_front(self, node):
        self._remove_node(node)
        self._add_node(node)

# Re-writing cleanly to avoid the class-in-class confusion in the final block
class LRUCache:
    class _Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map = {}
        self.size = 0
        self.head = self._Node(None, None)
        self.tail = self._Node(None, None)
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
            if self.size >= self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.map[lru.key]
                self.size -= 1
            new_node = self._Node(key, value)
            self.map[key] = new_node
            self._add_to_front(new_node)
            self.size += 1
