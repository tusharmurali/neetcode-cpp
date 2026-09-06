# 14. Longest Common Prefix

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/longest-common-prefix/>  
- **NeetCode:** <https://neetcode.io/problems/longest-common-prefix>  
- **Video:** <https://www.youtube.com/watch?v=0sWShKIJoo4>  

[← Back to index](../INDEX.md)

## 1. Horizontal Scanning

Start with the first string as the initial prefix candidate. Then compare it with each subsequent string, shrinking the prefix to match only the common portion. After processing all strings, what remains is the longest common prefix. The prefix can only shrink or stay the same as we go through more strings.

```cpp
class Solution {
public:
    string longestCommonPrefix(vector<string>& strs) {
        string prefix = strs[0];
        for (int i = 1; i < strs.size(); i++) {
            int j = 0;
            while (j < min(prefix.length(), strs[i].length())) {
                if (prefix[j] != strs[i][j]) {
                    break;
                }
                j++;
            }
            prefix = prefix.substr(0, j);
        }
        return prefix;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(1)$

> Where $n$ is the length of the shortest string and $m$ is the number of strings.

## 2. Vertical Scanning

Instead of comparing entire strings horizontally, we can compare characters column by column across all strings. Check if all strings have the same character at position `0`, then position `1`, and so on. The moment we find a mismatch or reach the end of any string, we've found where the common prefix ends.

```cpp
class Solution {
public:
    string longestCommonPrefix(vector<string>& strs) {
        for (int i = 0; i < strs[0].length(); i++) {
            for (const string& s : strs) {
                if (i == s.length() || s[i] != strs[0][i]) {
                    return s.substr(0, i);
                }
            }
        }
        return strs[0];
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(1)$ since we did not use extra space.

> Where $n$ is the length of the shortest string and $m$ is the number of strings.

## 3. Sorting

When strings are sorted lexicographically, the first and last strings in the sorted order are the most different from each other. If these two extremes share a common prefix, then all strings in between must also share that same prefix. So we only need to compare the first and last strings after sorting.

```cpp
class Solution {
public:
    string longestCommonPrefix(vector<string>& strs) {
        if (strs.size() == 1) {
            return strs[0];
        }

        sort(strs.begin(), strs.end());
        for (int i = 0; i < min(strs[0].length(), strs.back().length()); i++) {
            if (strs[0][i] != strs.back()[i]) {
                return strs[0].substr(0, i);
            }
        }
        return strs[0];
    }
};
```

**Complexity**

- Time complexity: $O(n * m \log m)$
- Space complexity: $O(1)$ or $O(m)$ depending on the sorting algorithm.

> Where $n$ is the length of the longest string and $m$ is the number of strings.

## 4. Trie

A Trie naturally represents all prefixes. We insert the shortest string into the trie, then query each other string against it. For each string, we walk down the trie as far as characters match, tracking how deep we get. The minimum depth reached across all strings is the length of the longest common prefix.

```cpp
class TrieNode {
public:
    unordered_map<char, TrieNode*> children;
};

class Trie {
public:
    TrieNode* root;
    Trie() {
        root = new TrieNode();
    }

    void insert(const string& word) {
        TrieNode* node = root;
        for (char c : word) {
            if (node->children.find(c) == node->children.end()) {
                node->children[c] = new TrieNode();
            }
            node = node->children[c];
        }
    }

    int lcp(const string& word, int prefixLen) {
        TrieNode* node = root;
        int i = 0;
        while (i < min((int)word.length(), prefixLen)) {
            if (node->children.find(word[i]) == node->children.end()) {
                return i;
            }
            node = node->children[word[i]];
            i++;
        }
        return min((int)word.length(), prefixLen);
    }
};

class Solution {
public:
    string longestCommonPrefix(vector<string>& strs) {
        if (strs.size() == 1) {
            return strs[0];
        }
        int mini = 0;
        for (int i = 1; i < strs.size(); i++) {
            if (strs[mini].size() > strs[i].size()) {
                mini = i;
            }
        }

        Trie trie;
        trie.insert(strs[mini]);
        int prefixLen = strs[mini].length();

        for (int i = 0; i < strs.size(); i++) {
            prefixLen = trie.lcp(strs[i], prefixLen);
        }

        return strs[0].substr(0, prefixLen);
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n)$

> Where $n$ is the length of the shortest string and $m$ is the number of strings.

## Standalone solution file (`cpp/0014-longest-common-prefix.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    string longestCommonPrefix(vector<string>& strs) {
        string result = strs[0];
        int charIndex = 0;
        
        //finding minimum string length  - that could be max common prefix
        long maxCharIndex = strs[0].length();
        for (int i = 1; i < strs.size(); ++i) {
            if (strs[i].length() < maxCharIndex) {
                maxCharIndex = strs[i].length();
            }
        }

        while (charIndex < maxCharIndex) {
            char prevChar = strs[0][charIndex];
            for (int i = 1; i < strs.size(); ++i) {
                if (prevChar == strs[i][charIndex]) {
                    continue;
                }
                return result.substr(0, charIndex);
            }
            ++charIndex;
            result += prevChar;
        }
        return result.substr(0, charIndex);
    }
};
```
