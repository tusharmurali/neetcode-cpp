# 140. Word Break II

- **Difficulty:** Hard  
- **Pattern:** Backtracking  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/word-break-ii/>  
- **NeetCode:** <https://neetcode.io/problems/word-break-ii>  
- **Video:** <https://www.youtube.com/watch?v=QgLKdluDo08>  

[← Back to index](../INDEX.md)

## 1. Backtracking

We need to find all possible ways to segment the string into valid dictionary words. Starting from the beginning of the string, we try every possible prefix that exists in the dictionary. When we find a valid prefix, we recursively process the remaining substring. When we reach the end of the string, we have found a valid segmentation and add it to our result.

```cpp
class Solution {
    unordered_set<string> wordSet;
    vector<string> res;

public:
    vector<string> wordBreak(string s, vector<string>& wordDict) {
        wordSet = unordered_set<string>(wordDict.begin(), wordDict.end());
        vector<string> cur;
        backtrack(s, 0, cur);
        return res;
    }

private:
    void backtrack(const string& s, int i, vector<string>& cur) {
        if (i == s.size()) {
            res.push_back(join(cur));
            return;
        }

        for (int j = i; j < s.size(); ++j) {
            string w = s.substr(i, j - i + 1);
            if (wordSet.count(w)) {
                cur.push_back(w);
                backtrack(s, j + 1, cur);
                cur.pop_back();
            }
        }
    }

    string join(const vector<string>& words) {
        ostringstream oss;
        for (int i = 0; i < words.size(); ++i) {
            if (i > 0) oss << " ";
            oss << words[i];
        }
        return oss.str();
    }
};
```

**Complexity**

- Time complexity: $O(m + n * 2 ^ n)$
- Space complexity: $O(m + 2 ^ n)$

> Where $n$ is the length of the string $s$ and $m$ is the sum of the lengths of the strings in the $wordDict$.

## 2. Backtracking + Trie

Building a Trie from the dictionary words allows us to efficiently check prefixes while traversing the string. Instead of checking each substring against a set, we walk character by character through the Trie. This can provide early termination when no dictionary word starts with the current prefix, avoiding unnecessary substring operations.

```cpp
struct TrieNode {
    unordered_map<char, TrieNode*> children;
    bool isWord = false;
};

class Trie {
public:
    TrieNode* root;

    Trie() {
        root = new TrieNode();
    }

    void addWord(const string& word) {
        TrieNode* curr = root;
        for (char c : word) {
            if (!curr->children.count(c)) {
                curr->children[c] = new TrieNode();
            }
            curr = curr->children[c];
        }
        curr->isWord = true;
    }
};

class Solution {
public:
    vector<string> wordBreak(string s, vector<string>& wordDict) {
        Trie trie;
        for (const string& word : wordDict) {
            trie.addWord(word);
        }

        vector<string> res;
        vector<string> path;
        backtrack(0, s, path, trie, res);
        return res;
    }

private:
    void backtrack(int index, string& s, vector<string>& path, Trie& trie, vector<string>& res) {
        if (index == s.size()) {
            stringstream ss;
            for (int i = 0; i < path.size(); ++i) {
                if (i > 0) ss << " ";
                ss << path[i];
            }
            res.push_back(ss.str());
            return;
        }

        TrieNode* node = trie.root;
        string word;
        for (int i = index; i < s.size(); ++i) {
            char c = s[i];
            if (!node->children.count(c)) break;

            word.push_back(c);
            node = node->children[c];

            if (node->isWord) {
                path.push_back(word);
                backtrack(i + 1, s, path, trie, res);
                path.pop_back();
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(m + n * 2 ^ n)$
- Space complexity: $O(m + 2 ^ n)$

> Where $n$ is the length of the string $s$ and $m$ is the sum of the lengths of the strings in the $wordDict$.

## 3. Dynamic Programming (Top-Down)

The pure backtracking approach may recompute results for the same suffix multiple times. By caching the list of all valid sentences that can be formed starting from each index, we avoid redundant computation. When we encounter a starting position we have already processed, we simply return the cached result.

```cpp
class Solution {
public:
    vector<string> wordBreak(string s, vector<string>& wordDict) {
        wordSet = unordered_set<string>(wordDict.begin(), wordDict.end());
        cache = unordered_map<int, vector<string>>();
        return backtrack(s, 0);
    }

private:
    unordered_set<string> wordSet;
    unordered_map<int, vector<string>> cache;

    vector<string> backtrack(const string& s, int i) {
        if (i == s.size())
            return {""};
        if (cache.count(i))
            return cache[i];

        vector<string> res;
        for (int j = i; j < s.size(); ++j) {
            string w = s.substr(i, j - i + 1);
            if (!wordSet.count(w))
                continue;
            vector<string> strings = backtrack(s, j + 1);
            for (const string& substr : strings) {
                string sentence = w;
                if (!substr.empty())
                    sentence += " " + substr;
                res.push_back(sentence);
            }
        }
        cache[i] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m + n * 2 ^ n)$
- Space complexity: $O(m + n * 2 ^ n)$

> Where $n$ is the length of the string $s$ and $m$ is the sum of the lengths of the strings in the $wordDict$.

## 4. Dynamic Programming (Bottom-Up)

Instead of recursing from the start, we can build the solution iteratively from the beginning. For each position `i`, we store all valid sentences that can be formed using characters from index `0` to `i-1`. We extend existing sentences by appending new words when a valid dictionary word ends at position `i`.

```cpp
class Solution {
public:
    vector<string> wordBreak(string s, vector<string>& wordDict) {
        unordered_set<string> wordSet(wordDict.begin(), wordDict.end());
        int n = s.size();
        vector<vector<string>> dp(n + 1);
        dp[0] = {""};

        for (int i = 1; i <= n; ++i) {
            for (int j = 0; j < i; ++j) {
                string word = s.substr(j, i - j);
                if (wordSet.count(word)) {
                    for (const string& sentence : dp[j]) {
                        if (sentence.empty()) {
                            dp[i].push_back(word);
                        } else {
                            dp[i].push_back(sentence + " " + word);
                        }
                    }
                }
            }
        }

        return dp[n];
    }
};
```

**Complexity**

- Time complexity: $O(m + n * 2 ^ n)$
- Space complexity: $O(m + n * 2 ^ n)$

> Where $n$ is the length of the string $s$ and $m$ is the sum of the lengths of the strings in the $wordDict$.

## 5. Dynamic Programming (Top-Down) Using Trie

This combines the benefits of Trie-based prefix matching with memoization. The Trie provides efficient character-by-character matching and early termination, while the `cache` prevents recomputation of results for the same starting positions. This is particularly effective when the dictionary contains many words with common prefixes.

```cpp
struct TrieNode {
    unordered_map<char, TrieNode*> children;
    bool isWord = false;
};

class Trie {
public:
    TrieNode* root;

    Trie() {
        root = new TrieNode();
    }

    void addWord(const string& word) {
        TrieNode* curr = root;
        for (char c : word) {
            if (!curr->children.count(c)) {
                curr->children[c] = new TrieNode();
            }
            curr = curr->children[c];
        }
        curr->isWord = true;
    }
};

class Solution {
public:
    vector<string> wordBreak(string s, vector<string>& wordDict) {
        Trie trie;
        for (const string& word : wordDict) {
            trie.addWord(word);
        }

        unordered_map<int, vector<string>> cache;
        return backtrack(0, s, trie, cache);
    }

private:
    vector<string> backtrack(int index, string& s, Trie& trie, unordered_map<int, vector<string>>& cache) {
        if (index == s.size()) {
            return {""};
        }

        if (cache.count(index)) {
            return cache[index];
        }

        vector<string> res;
        TrieNode* curr = trie.root;

        for (int i = index; i < s.size(); ++i) {
            char c = s[i];
            if (!curr->children.count(c)) {
                break;
            }
            curr = curr->children[c];
            if (curr->isWord) {
                for (const string& suffix : backtrack(i + 1, s, trie, cache)) {
                    if (!suffix.empty()) {
                        res.push_back(s.substr(index, i - index + 1) + " " + suffix);
                    } else {
                        res.push_back(s.substr(index, i - index + 1));
                    }
                }
            }
        }

        return cache[index] = res;
    }
};
```

**Complexity**

- Time complexity: $O(m + n * 2 ^ n)$
- Space complexity: $O(m + n * 2 ^ n)$

> Where $n$ is the length of the string $s$ and $m$ is the sum of the lengths of the strings in the $wordDict$.
