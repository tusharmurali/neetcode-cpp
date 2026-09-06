# 3042. Count Prefix and Suffix Pairs I

- **Difficulty:** Easy  
- **Pattern:** Tries  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/count-prefix-and-suffix-pairs-i/>  
- **NeetCode:** <https://neetcode.io/problems/count-prefix-and-suffix-pairs-i>  
- **Video:** <https://www.youtube.com/watch?v=zQrtsvo8lgM>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each pair of indices `(i, j)` where `i < j`, we need to check if `words[i]` is both a prefix and suffix of `words[j]`. We compare characters at the beginning and end of `words[j]` with `words[i]`.

```cpp
class Solution {
public:
    int countPrefixSuffixPairs(vector<string>& words) {
        int res = 0;
        for (int i = 0; i < words.size(); i++) {
            for (int j = i + 1; j < words.size(); j++) {
                if (isPrefixAndSuffix(words[i], words[j])) {
                    res++;
                }
            }
        }
        return res;
    }

    bool isPrefixAndSuffix(string s1, string s2) {
        if (s1.size() > s2.size()) return false;

        for (int i = 0; i < s1.size(); i++) {
            if (s1[i] != s2[i]) return false;
        }

        int j = 0;
        for (int i = s2.size() - s1.size(); i < s2.size(); i++) {
            if (s1[j] != s2[i]) return false;
            j++;
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * m)$
- Space complexity: $O(1)$

> Where $n$ is the size of the input array $words$, and $m$ is the maximum length of a string.

## 2. Trie

We can use a trie where each node is keyed by a pair of characters: one from the prefix and one from the suffix. By processing words in reverse order and storing them in this combined trie, when we look up a word, we find how many previously seen words have it as both prefix and suffix.

```cpp
class TrieNode {
public:
    unordered_map<string, TrieNode*> children;
    int count = 0;
};

class Trie {
public:
    TrieNode* root;
    Trie() {
        root = new TrieNode();
    }

    void add(string w) {
        TrieNode* cur = root;
        int n = w.size();
        for (int i = 0; i < n; i++) {
            string key = string(1, w[i]) + w[n - 1 - i];
            if (cur->children.find(key) == cur->children.end()) {
                cur->children[key] = new TrieNode();
            }
            cur = cur->children[key];
            cur->count++;
        }
    }

    int count(string w) {
        TrieNode* cur = root;
        int n = w.size();
        for (int i = 0; i < n; i++) {
            string key = string(1, w[i]) + w[n - 1 - i];
            if (cur->children.find(key) == cur->children.end()) return 0;
            cur = cur->children[key];
        }
        return cur->count;
    }
};

class Solution {
public:
    int countPrefixSuffixPairs(vector<string>& words) {
        int res = 0;
        Trie root;
        for (int i = words.size() - 1; i >= 0; i--) {
            res += root.count(words[i]);
            root.add(words[i]);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$

> Where $n$ is the size of the input array $words$, and $m$ is the maximum length of a string.
