# 211. Design Add And Search Words Data Structure

- **Difficulty:** Medium  
- **Pattern:** Tries  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/design-add-and-search-words-data-structure/>  
- **NeetCode:** <https://neetcode.io/problems/design-word-search-data-structure>  
- **Video:** <https://www.youtube.com/watch?v=BTf05gs_8iU>  
- **Video approach:** 2. Depth First Search (Trie)  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest way to solve this problem is to **store all words as-is** and check every stored word during search.

When searching:

- If the lengths don't match → it can't be a match.
- Compare characters one by one:
    - Exact match is required **unless** the search character is `.`
    - `.` acts as a **wildcard** and can match **any character**.

This approach works because the constraints are small enough, but it is **not efficient** for large datasets.

```cpp
class WordDictionary {
public:
    vector<string> store;

    WordDictionary() {}

    void addWord(string word) {
        store.push_back(word);
    }

    bool search(string word) {
        for (string w : store) {
            if (w.length() != word.length()) continue;
            int i = 0;
            while (i < w.length()) {
                if (w[i] == word[i] || word[i] == '.') {
                    i++;
                } else {
                    break;
                }
            }
            if (i == w.length()) {
                return true;
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(1)$ for $addWord()$, $O(m * n)$ for $search()$.
- Space complexity: $O(m * n)$

> Where $m$ is the number of words added and $n$ is the length of the string.

## 2. Depth First Search (Trie) ▶ video

```cpp
class TrieNode {
public:
    vector<TrieNode*> children;
    bool word;

    TrieNode() : children(26, nullptr), word(false) {}
};

class WordDictionary {
public:
    TrieNode* root;

    WordDictionary() : root(new TrieNode()) {}

    void addWord(string word) {
        TrieNode* cur = root;
        for (char c : word) {
            if (cur->children[c - 'a'] == nullptr) {
                cur->children[c - 'a'] = new TrieNode();
            }
            cur = cur->children[c - 'a'];
        }
        cur->word = true;
    }

    bool search(string word) {
        return dfs(word, 0, root);
    }

private:
    bool dfs(string word, int j, TrieNode* root) {
        TrieNode* cur = root;

        for (int i = j; i < word.size(); i++) {
            char c = word[i];
            if (c == '.') {
                for (TrieNode* child : cur->children) {
                    if (child != nullptr && dfs(word, i + 1, child)) {
                        return true;
                    }
                }
                return false;
            } else {
                if (cur->children[c - 'a'] == nullptr) {
                    return false;
                }
                cur = cur->children[c - 'a'];
            }
        }
        return cur->word;
    }
};
```

**Complexity**

- Time complexity: $O(n)$ for $addWord()$, $O(n)$ for $search()$.
- Space complexity: $O(t + n)$

> Where $n$ is the length of the string and $t$ is the total number of TrieNodes created in the Trie.

## Standalone solution file (`cpp/0211-design-add-and-search-words-data-structure.cpp` in the NeetCode repo)

```cpp
/*
    Design add & search words data structure

    Implement trie, handle wildcards: traverse all children & search substrings

    Time: O(m x 26^n) -> m = # of words, n = length of words
    Space: O(n)
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

class WordDictionary {
public:
    WordDictionary() {
        root = new TrieNode();
    }
    
    void addWord(string word) {
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
        return searchInNode(word, 0, node);
    }
private:
    TrieNode* root;
    
    bool searchInNode(string& word, int i, TrieNode* node) {
        if (node == NULL) {
            return false;
        }
        if (i == word.size()) {
            return node->isWord;
        }
        if (word[i] != '.') {
            return searchInNode(word, i + 1, node->children[word[i] - 'a']);
        }
        for (int j = 0; j < 26; j++) {
            if (searchInNode(word, i + 1, node->children[j])) {
                return true;
            }
        }
        return false;
    }
};

/**
 * Your WordDictionary object will be instantiated and called as such:
 * WordDictionary* obj = new WordDictionary();
 * obj->addWord(word);
 * bool param_2 = obj->search(word);
 */
```
