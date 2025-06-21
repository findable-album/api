class TrieNode:
    def __init__(self):
        self.children = {}
        self.items = []


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, key: str, item):
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.items.append(item)

    def search_prefix(self, prefix: str):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return node.items
