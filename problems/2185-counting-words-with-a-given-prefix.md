# 2185. Counting Words With a Given Prefix

- **Difficulty:** Easy  
- **Pattern:** Tries  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/counting-words-with-a-given-prefix/>  
- **NeetCode:** <https://neetcode.io/problems/counting-words-with-a-given-prefix>  
- **Video:** <https://www.youtube.com/watch?v=B26hW8fBMj0>  

[← Back to index](../INDEX.md)

## 1. Brute Force

To check if a word has a given prefix, we compare the first few characters of the word with the prefix string. If the word is shorter than the prefix, it cannot have that prefix. Otherwise, we check character by character until we either find a mismatch or confirm all prefix characters match.

```cpp
class Solution {
public:
    int prefixCount(vector<string>& words, string pref) {
        int N = pref.size(), res = 0;

        for (auto &w : words) {
            if ((int)w.size() < N) continue;
            int inc = 1;
            for (int i = 0; i < N; i++) {
                if (w[i] != pref[i]) {
                    inc = 0;
                    break;
                }
            }
            res += inc;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(1)$

> Where $m$ is the number of words and $n$ is the length of the string $pref$.

## 2. Built-In Method

Most programming languages provide built-in methods to check if a string starts with a given prefix. These methods handle the character comparison internally and are optimized for the task, making the code cleaner and less error-prone.

```cpp
class Solution {
public:
    int prefixCount(vector<string>& words, string pref) {
        int res = 0;
        for (string& w : words) {
            if (w.rfind(pref, 0) == 0) {
                res++;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(1)$

> Where $m$ is the number of words and $n$ is the length of the string $pref$.

## 3. Trie

A Trie (prefix tree) is a tree structure where each node represents a character. By inserting only the first few characters of each word (up to the prefix length), we build a compact structure. Each node keeps a count of how many words pass through it. After inserting all words, we traverse the trie following the prefix characters and return the count at the final node.

```cpp
struct PrefixNode {
    PrefixNode* children[26];
    int count;
    PrefixNode() {
        for (int i = 0; i < 26; i++) children[i] = nullptr;
        count = 0;
    }
};

class PrefixTree {
public:
    PrefixNode* root;
    PrefixTree() {
        root = new PrefixNode();
    }

    void add(const string& w, int length) {
        PrefixNode* cur = root;
        for (int i = 0; i < length; i++) {
            int idx = w[i] - 'a';
            if (!cur->children[idx]) {
                cur->children[idx] = new PrefixNode();
            }
            cur = cur->children[idx];
            cur->count++;
        }
    }

    int count(const string& pref) {
        PrefixNode* cur = root;
        for (char c : pref) {
            int idx = c - 'a';
            if (!cur->children[idx]) return 0;
            cur = cur->children[idx];
        }
        return cur->count;
    }
};

class Solution {
public:
    int prefixCount(vector<string>& words, string pref) {
        PrefixTree prefixTree;
        for (string& w : words) {
            if ((int)w.size() >= (int)pref.size()) {
                prefixTree.add(w, pref.size());
            }
        }
        return prefixTree.count(pref);
    }
};
```

**Complexity**

- Time complexity: $O(m * l + n)$
- Space complexity: $O(m * l)$

> Where $m$ is the number of words, $n$ is the length of the string $pref$ and $l$ is the maximum length of a word.
