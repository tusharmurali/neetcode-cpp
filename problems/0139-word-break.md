# 139. Word Break

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/word-break/>  
- **NeetCode:** <https://neetcode.io/problems/word-break>  
- **Video:** <https://www.youtube.com/watch?v=Sx9NNgInc3A>  
- **Video approach:** 5. Dynamic Programming (Bottom-Up)  

[← Back to index](../INDEX.md)

## 1. Recursion

At every index `i` in the string, we want to decide:

> **Can the suffix starting at index `i` be segmented into valid dictionary words?**

The recursive idea is:

- Try **every word** in `wordDict`
- If a word matches the string starting at position `i`
- Recursively check whether the **remaining substring** (starting at `i + len(word)`) can also be broken successfully

If **any path** reaches the end of the string, the answer is `true`.

This is a classic **decision-based recursion** where:

- Each index `i` represents a subproblem
- Base case: reaching the end means a valid segmentation

```cpp
class Solution {
public:
    bool wordBreak(string s, vector<string>& wordDict) {
        return dfs(s, wordDict, 0);
    }

private:
    bool dfs(const string& s, const vector<string>& wordDict, int i) {
        if (i == s.length()) {
            return true;
        }

        for (const string& w : wordDict) {
            if (i + w.length() <= s.length() &&
                s.substr(i, w.length()) == w) {
                if (dfs(s, wordDict, i + w.length())) {
                    return true;
                }
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(t * m ^ n)$
- Space complexity: $O(n)$

> Where $n$ is the length of the string $s$, $m$ is the number of words in $wordDict$ and $t$ is the maximum length of any word in $wordDict$.

## 2. Recursion (Hash Set)

This version improves the brute-force recursion by **optimizing word lookup**.

Instead of trying every word from `wordDict` at each index, we:

- Fix a starting index `i`
- Try **all possible substrings** `s[i : j+1]`
- Check if the substring exists in a **Hash Set** (`O(1)` lookup)

If a valid word is found:

- Recursively check whether the remaining suffix starting at `j + 1` can be segmented

The key idea:

> If we can split the string at **any valid word boundary** and the rest is solvable, then the whole string is solvable.

```cpp
class Solution {
public:
    bool wordBreak(string s, vector<string>& wordDict) {
        unordered_set<string> wordSet(wordDict.begin(), wordDict.end());
        return dfs(s, wordSet, 0);
    }

    bool dfs(const string& s, const unordered_set<string>& wordSet, int i) {
        if (i == s.size()) {
            return true;
        }

        for (int j = i; j < s.size(); j++) {
            if (wordSet.find(s.substr(i, j - i + 1)) != wordSet.end()) {
                if (dfs(s, wordSet, j + 1)) {
                    return true;
                }
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O( (n * 2 ^ n) + m)$
- Space complexity: $O(n + (m * t))$

> Where $n$ is the length of the string $s$ and $m$ is the number of words in $wordDict$.

## 3. Dynamic Programming (Top-Down)

This is an **optimized version of recursion using memoization**.

The key observation:

- While recursively checking splits, the **same index `i` is reached many times**
- The result of `dfs(i)` (can suffix `s[i:]` be segmented?) **never changes**

So we **cache the result for each index**:

- If `dfs(i)` was already computed, reuse it
- This avoids recomputing exponential subtrees

In short:

> Convert exponential recursion into linear states using memoization.

```cpp
class Solution {
public:
    unordered_map<int, bool> memo;

    bool wordBreak(string s, vector<string>& wordDict) {
        memo[s.length()] = true;
        return dfs(s, wordDict, 0);
    }

    bool dfs(string& s, vector<string>& wordDict, int i) {
        if (memo.find(i) != memo.end()) {
            return memo[i];
        }

        for (const string& w : wordDict) {
            if (i + w.length() <= s.length() &&
                s.substr(i, w.length()) == w) {
                if (dfs(s, wordDict, i + w.length())) {
                    memo[i] = true;
                    return true;
                }
            }
        }
        memo[i] = false;
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n * m * t)$
- Space complexity: $O(n)$

> Where $n$ is the length of the string $s$, $m$ is the number of words in $wordDict$ and $t$ is the maximum length of any word in $wordDict$.

## 4. Dynamic Programming (Hash Set)

This approach is a **top-down dynamic programming solution with pruning**.

Key ideas:

- Checking every possible substring is expensive.
- A word can only be as long as the **maximum word length** in `wordDict`.
- Use a **Hash Set** for `O(1)` word lookup.
- Use **memoization** so each index in the string is solved only once.

So we:

- Limit how far we try to split from each index
- Cache results for indices to avoid repeated work

This turns exponential recursion into efficient DP.

```cpp
class Solution {
public:
    unordered_set<string> wordSet;
    vector<int> memo;
    int t;

    bool wordBreak(string s, vector<string>& wordDict) {
        wordSet.insert(wordDict.begin(), wordDict.end());
        memo.resize(s.size(), -1);
        t = 0;
        for (string& w : wordDict) {
            t = max(t, int(w.length()));
        }
        return dfs(s, 0);
    }

    bool dfs(string& s, int i) {
        if (i == s.size()) {
            return true;
        }
        if (memo[i] != -1) {
            return memo[i] == 1;
        }

        for (int j = i; j < (i + t, s.size()); j++) {
            if (wordSet.count(s.substr(i, j - i + 1))) {
                if (dfs(s, j + 1)) {
                    memo[i] = 1;
                    return true;
                }
            }
        }
        memo[i] = 0;
        return false;
    }
};
```

**Complexity**

- Time complexity: $O((t ^ 2 * n) + m)$
- Space complexity: $O(n + (m * t))$

> Where $n$ is the length of the string $s$, $m$ is the number of words in $wordDict$ and $t$ is the maximum length of any word in $wordDict$.

## 5. Dynamic Programming (Bottom-Up) ▶ video

This is a **bottom-up dynamic programming** approach.

Instead of trying to split the string recursively, we solve the problem **from the end of the string toward the start**.

Key idea:

- `dp[i]` means **whether the substring `s[i:]` can be segmented**
- If we know the answer for future positions, we can decide the current one
- We reuse already computed results → no recursion, no stack overhead

```cpp
class Solution {
public:
    bool wordBreak(string s, vector<string>& wordDict) {
        vector<bool> dp(s.size() + 1, false);
        dp[s.size()] = true;

        for (int i = s.size() - 1; i >= 0; i--) {
            for (const auto& w : wordDict) {
                if ((i + w.size()) <= s.size() &&
                     s.substr(i, w.size()) == w) {
                    dp[i] = dp[i + w.size()];
                }
                if (dp[i]) {
                    break;
                }
            }
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n * m * t)$
- Space complexity: $O(n)$

> Where $n$ is the length of the string $s$, $m$ is the number of words in $wordDict$ and $t$ is the maximum length of any word in $wordDict$.

## 6. Dynamic Programming (Trie)

The normal DP checks every word at every index, which can waste time comparing strings again and again.

A **Trie** stores all dictionary words like a prefix tree, so from any starting index `i` in `s`, we can **walk forward character-by-character** and quickly know:

- whether the current prefix matches some dictionary word path
- and when we hit a complete word (`is_word = true`)

We still use DP:

- `dp[i]` = can we break the suffix `s[i:]` into dictionary words?
- If from `i` we can reach some `j` where `s[i..j]` is a word, then `dp[i] = dp[j+1]`

Trie helps us _find valid words starting at `i` efficiently_.

```cpp
class TrieNode {
public:
    unordered_map<char, TrieNode*> children;
    bool is_word = false;
};

class Trie {
public:
    TrieNode* root;

    Trie() {
        root = new TrieNode();
    }

    void insert(string word) {
        TrieNode* node = root;
        for (char c : word) {
            if (!node->children.count(c)) {
                node->children[c] = new TrieNode();
            }
            node = node->children[c];
        }
        node->is_word = true;
    }

    bool search(string& s, int i, int j) {
        TrieNode* node = root;
        for (int idx = i; idx <= j; ++idx) {
            if (!node->children.count(s[idx])) {
                return false;
            }
            node = node->children[s[idx]];
        }
        return node->is_word;
    }
};

class Solution {
public:
    bool wordBreak(string s, vector<string>& wordDict) {
        Trie trie;
        for (string word : wordDict) {
            trie.insert(word);
        }

        int n = s.length();
        vector<bool> dp(n + 1, false);
        dp[n] = true;

        int maxLen = 0;
        for (string w : wordDict) {
            maxLen = max(maxLen, (int)w.size());
        }

        for (int i = n - 1; i >= 0; --i) {
            for (int j = i; j < min(n, i + maxLen); ++j) {
                if (trie.search(s, i, j)) {
                    dp[i] = dp[j + 1];
                    if (dp[i]) break;
                }
            }
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O((n * t ^ 2) + m)$
- Space complexity: $O(n + (m * t))$

> Where $n$ is the length of the string $s$, $m$ is the number of words in $wordDict$ and $t$ is the maximum length of any word in $wordDict$.

## Standalone solution file (`cpp/0139-word-break.cpp` in the NeetCode repo)

```cpp
/*
    Given a string & dictionary, return true if:
    Can segment string into 1 or more dictionary words

    DP, at each loop, substring, check if in dict, & store

    Time: O(n^3)
    Space: O(n)
*/

class Solution {
public:
    bool wordBreak(string s, vector<string>& wordDict) {
        unordered_set<string> words;
        for (int i = 0; i < wordDict.size(); i++) {
            words.insert(wordDict[i]);
        }
        
        int n = s.size();
        vector<bool> dp(n + 1);
        dp[0] = true;
        
        for (int i = 1; i <= n; i++) {
            for (int j = i - 1; j >= 0; j--) {
                if (dp[j]) {
                    string word = s.substr(j, i - j);
                    if (words.find(word) != words.end()) {
                        dp[i] = true;
                        break;
                    }
                }
            }
        }
        
        return dp[n];
    }
};
```
