# 208. Implement Trie Prefix Tree

- **Difficulty:** Medium  
- **Pattern:** Tries  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/implement-trie-prefix-tree/>  
- **NeetCode:** <https://neetcode.io/problems/implement-prefix-tree>  
- **Video:** <https://www.youtube.com/watch?v=oobqoCJlHA0>  
- **Video approach:** 1. Prefix Tree (Array)  

[← Back to index](../INDEX.md)

## 1. Prefix Tree (Array) ▶ video

A **Prefix Tree (Trie)** is a tree-like data structure designed for **fast string operations**.

Each node represents a character, and paths from the root represent words.

- Common prefixes are **shared**, which saves space.
- Each node has **26 children** (for letters `a`-`z`), indexed directly using character positions.
- A boolean flag `endOfWord` tells us whether a complete word ends at that node.

Why Trie is useful:

- Searching words and prefixes is **O(length of word)**, not dependent on how many words exist.
- Ideal for problems involving **dictionary lookups**, **autocomplete**, and **prefix checks**.

```cpp
class TrieNode {
public:
    TrieNode* children[26];
    bool endOfWord;

    TrieNode() {
        for (int i = 0; i < 26; i++) {
            children[i] = nullptr;
        }
        endOfWord = false;
    }
};

class PrefixTree {
    TrieNode* root;

public:
    PrefixTree() {
        root = new TrieNode();
    }

    void insert(string word) {
        TrieNode* cur = root;
        for (char c : word) {
            int i = c - 'a';
            if (cur->children[i] == nullptr) {
                cur->children[i] = new TrieNode();
            }
            cur = cur->children[i];
        }
        cur->endOfWord = true;
    }

    bool search(string word) {
        TrieNode* cur = root;
        for (char c : word) {
            int i = c - 'a';
            if (cur->children[i] == nullptr) {
                return false;
            }
            cur = cur->children[i];
        }
        return cur->endOfWord;
    }

    bool startsWith(string prefix) {
        TrieNode* cur = root;
        for (char c : prefix) {
            int i = c - 'a';
            if (cur->children[i] == nullptr) {
                return false;
            }
            cur = cur->children[i];
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$ for each function call.
- Space complexity: $O(t)$

> Where $n$ is the length of the string and $t$ is the total number of TrieNodes created in the Trie.

## 2. Prefix Tree (Hash Map)

```cpp
class TrieNode {
public:
    unordered_map<char, TrieNode*> children;
    bool endOfWord = false;
};

class PrefixTree {
    TrieNode* root;

public:
    PrefixTree() {
        root = new TrieNode();
    }

    void insert(string word) {
        TrieNode* cur = root;
        for (char c : word) {
            if (cur->children.find(c) == cur->children.end()) {
                cur->children[c] = new TrieNode();
            }
            cur = cur->children[c];
        }
        cur->endOfWord = true;
    }

    bool search(string word) {
        TrieNode* cur = root;
        for (char c : word) {
            if (cur->children.find(c) == cur->children.end()) {
                return false;
            }
            cur = cur->children[c];
        }
        return cur->endOfWord;
    }

    bool startsWith(string prefix) {
        TrieNode* cur = root;
        for (char c : prefix) {
            if (cur->children.find(c) == cur->children.end()) {
                return false;
            }
            cur = cur->children[c];
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$ for each function call.
- Space complexity: $O(t)$

> Where $n$ is the length of the string and $t$ is the total number of TrieNodes created in the Trie.

## Standalone solution file (`cpp/0208-implement-trie-prefix-tree.cpp` in the NeetCode repo)

```cpp
/*
    Implement trie (store/retrieve keys in dataset of strings)

    Each node contains pointer to next letter & is word flag

    Time: O(n) insert, O(n) search, O(n) startsWith
    Space: O(n) insert, O(1) search, O(1) startsWith
*/

class TrieNode {
public:
    TrieNode* children[26];
    bool isWord;
    
    TrieNode() {
        for (int i = 0; i < 26; i++) {
            children[i] = NULL;
        }
        isWord = false;
    }
};

class Trie {
public:
    Trie() {
        root = new TrieNode();
    }
    
    void insert(string word) {
        TrieNode* node = root;
        int curr = 0;
        
        for (int i = 0; i < word.size(); i++) {
            curr = word[i] - 'a';
            if (node->children[curr] == NULL) {
                node->children[curr] = new TrieNode();
            }
            node = node->children[curr];
        }
        
        node->isWord = true;
    }
    
    bool search(string word) {
        TrieNode* node = root;
        int curr = 0;
        
        for (int i = 0; i < word.size(); i++) {
            curr = word[i] - 'a';
            if (node->children[curr] == NULL) {
                return false;
            }
            node = node->children[curr];
        }
        
        return node->isWord;
    }
    
    bool startsWith(string prefix) {
        TrieNode* node = root;
        int curr = 0;
        
        for (int i = 0; i < prefix.size(); i++) {
            curr = prefix[i] - 'a';
            if (node->children[curr] == NULL) {
                return false;
            }
            node = node->children[curr];
        }
        
        return true;
    }
private:
    TrieNode* root;
};

/**
 * Your Trie object will be instantiated and called as such:
 * Trie* obj = new Trie();
 * obj->insert(word);
 * bool param_2 = obj->search(word);
 * bool param_3 = obj->startsWith(prefix);
 */
```
