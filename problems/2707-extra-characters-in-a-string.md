# 2707. Extra Characters in a String

- **Difficulty:** Medium  
- **Pattern:** Tries  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/extra-characters-in-a-string/>  
- **NeetCode:** <https://neetcode.io/problems/extra-characters-in-a-string>  
- **Video:** <https://www.youtube.com/watch?v=ONstwO1cD7c>  

[← Back to index](../INDEX.md)

## 1. Recursion

At each position in the string, we have two choices: either skip the current character (counting it as extra), or try to match a dictionary word starting at this position. If a word matches, we can jump past it without counting those characters as extra.

This recursive approach explores all possibilities. For each index, we take the minimum of skipping one character versus matching any dictionary word that starts at that index.

```cpp
class Solution {
public:
    int minExtraChar(string s, vector<string>& dictionary) {
        unordered_set<string> words(dictionary.begin(), dictionary.end());
        return dfs(0, s, words);
    }

private:
    int dfs(int i, const string& s, unordered_set<string>& words) {
        if (i == s.size()) {
            return 0;
        }

        int res = 1 + dfs(i + 1, s, words);
        for (int j = i; j < s.size(); j++) {
            if (words.count(s.substr(i, j - i + 1))) {
                res = min(res, dfs(j + 1, s, words));
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n + m * k)$
- Space complexity: $O(n + m * k)$

> Where $n$ is the length of the string $s$, $m$ is the number of words in the dictionary, and $k$ is the average length of a word in the dictionary.

## 2. Dynamic Programming (Top-Down) Using Hash Set

The recursive solution has overlapping subproblems since we may compute the answer for the same index multiple times. Memoization stores results so each subproblem is solved only once.

Using a hash set for the dictionary allows efficient substring lookups. The memoization table `dp[i]` stores the minimum extra characters from index `i` onward.

```cpp
class Solution {
public:
    int minExtraChar(string s, vector<string>& dictionary) {
        unordered_set<string> words(dictionary.begin(), dictionary.end());
        int n = s.size();
        vector<int> dp(n + 1, -1);
        dp[n] = 0;
        return dfs(0, s, words, dp);
    }

private:
    int dfs(int i, string& s, unordered_set<string>& words, vector<int>& dp) {
        if (dp[i] != -1) return dp[i];
        int res = 1 + dfs(i + 1, s, words, dp);
        for (int j = i; j < s.size(); j++) {
            if (words.count(s.substr(i, j - i + 1))) {
                res = min(res, dfs(j + 1, s, words, dp));
            }
        }
        dp[i] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3 + m * k)$
- Space complexity: $O(n + m * k)$

> Where $n$ is the length of the string $s$, $m$ is the number of words in the dictionary, and $k$ is the average length of a word in the dictionary.

## 3. Dynamic Programming (Bottom-Up) Using Hash Set

Instead of recursion with memoization, we can fill the DP table iteratively from right to left. `dp[i]` represents the minimum extra characters when starting from index `i`. Since `dp[i]` depends on `dp[j+1]` for `j >= i`, processing from right to left ensures all dependencies are resolved.

```cpp
class Solution {
public:
    int minExtraChar(string s, vector<string>& dictionary) {
        unordered_set<string> words(dictionary.begin(), dictionary.end());
        int n = s.size();
        vector<int> dp(n + 1, 0);

        for (int i = n - 1; i >= 0; i--) {
            dp[i] = 1 + dp[i + 1];
            for (int j = i; j < n; j++) {
                if (words.count(s.substr(i, j - i + 1))) {
                    dp[i] = min(dp[i], dp[j + 1]);
                }
            }
        }
        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3 + m * k)$
- Space complexity: $O(n + m * k)$

> Where $n$ is the length of the string $s$, $m$ is the number of words in the dictionary, and $k$ is the average length of a word in the dictionary.

## 4. Dynamic Programming (Top-Down)

Instead of checking all substrings against a hash set, we can iterate through dictionary words directly. For each position, we check if any dictionary word matches starting at that position. This can be faster when the dictionary is small relative to the string length.

```cpp
class Solution {
    unordered_map<int, int> dp;

public:
    int minExtraChar(string s, vector<string>& dictionary) {
        dp[s.size()] = 0;
        return dfs(0, s, dictionary);
    }

private:
    int dfs(int i, string& s, vector<string>& dictionary) {
        if (dp.count(i)) {
            return dp[i];
        }

        int res = 1 + dfs(i + 1, s, dictionary);
        for (const string& word : dictionary) {
            if (i + word.size() > s.size()) continue;

            bool flag = true;
            for (int j = 0; j < word.size(); j++) {
                if (s[i + j] != word[j]) {
                    flag = false;
                    break;
                }
            }
            if (flag) {
                res = min(res, dfs(i + word.size(), s, dictionary));
            }
        }
        return dp[i] = res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m * k)$
- Space complexity: $O(n)$

> Where $n$ is the length of the string $s$, $m$ is the number of words in the dictionary, and $k$ is the average length of a word in the dictionary.

## 5. Dynamic Programming (Bottom-Up)

This is the iterative version of the previous approach, iterating through dictionary words at each position rather than checking all possible substrings. It avoids recursion overhead while maintaining the same logic.

```cpp
class Solution {
public:
    int minExtraChar(string s, vector<string>& dictionary) {
        int n = s.size();
        vector<int> dp(n + 1, 0);

        for (int i = n - 1; i >= 0; i--) {
            dp[i] = 1 + dp[i + 1];
            for (const string& word : dictionary) {
                if (i + word.size() <= n && s.substr(i, word.size()) == word) {
                    dp[i] = min(dp[i], dp[i + word.size()]);
                }
            }
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n * m * k)$
- Space complexity: $O(n)$

> Where $n$ is the length of the string $s$, $m$ is the number of words in the dictionary, and $k$ is the average length of a word in the dictionary.

## 6. Dynamic Programming (Top-Down) Using Trie

A Trie (prefix tree) allows efficient prefix matching. Instead of checking each dictionary word independently, we traverse the Trie character by character. If we hit a dead end (no child for the current character), we stop early. This is faster than checking each word when there are many dictionary words sharing common prefixes.

```cpp
class TrieNode {
public:
    TrieNode* children[26];
    bool isWord;

    TrieNode() {
        for (int i = 0; i < 26; ++i) children[i] = nullptr;
        isWord = false;
    }
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
            if (!curr->children[c - 'a']) {
                curr->children[c - 'a'] = new TrieNode();
            }
            curr = curr->children[c - 'a'];
        }
        curr->isWord = true;
    }
};

class Solution {
public:
    int minExtraChar(string s, vector<string>& dictionary) {
        Trie trie;
        for (const string& word : dictionary) {
            trie.addWord(word);
        }

        vector<int> dp(s.size() + 1, -1);
        return dfs(0, s, trie, dp);
    }

private:
    int dfs(int i, const string& s, Trie& trie, vector<int>& dp) {
        if (i == s.size()) return 0;
        if (dp[i] != -1) return dp[i];

        int res = 1 + dfs(i + 1, s, trie, dp);
        TrieNode* curr = trie.root;

        for (int j = i; j < s.size(); ++j) {
            if (!curr->children[s[j] - 'a']) break;
            curr = curr->children[s[j] - 'a'];
            if (curr->isWord) {
                res = min(res, dfs(j + 1, s, trie, dp));
            }
        }

        dp[i] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 + m * k)$
- Space complexity: $O(n + m * k)$

> Where $n$ is the length of the string $s$, $m$ is the number of words in the dictionary, and $k$ is the average length of a word in the dictionary.

## 7. Dynamic Programming (Bottom-Up) Using Trie

This combines the bottom-up DP approach with Trie-based matching. We iterate from right to left, and at each position, we traverse the Trie to find all dictionary words that start at that position. The Trie allows early termination when no dictionary word can match the current prefix.

```cpp
class TrieNode {
public:
    TrieNode* children[26];
    bool isWord;

    TrieNode() {
        for (int i = 0; i < 26; ++i) children[i] = nullptr;
        isWord = false;
    }
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
            if (!curr->children[c - 'a']) {
                curr->children[c - 'a'] = new TrieNode();
            }
            curr = curr->children[c - 'a'];
        }
        curr->isWord = true;
    }
};

class Solution {
public:
    int minExtraChar(string s, vector<string>& dictionary) {
        Trie trie;
        for (const string& word : dictionary) {
            trie.addWord(word);
        }

        int n = s.size();
        vector<int> dp(n + 1);
        for (int i = n - 1; i >= 0; --i) {
            dp[i] = 1 + dp[i + 1];
            TrieNode* curr = trie.root;

            for (int j = i; j < n; ++j) {
                if (!curr->children[s[j] - 'a']) break;
                curr = curr->children[s[j] - 'a'];
                if (curr->isWord) {
                    dp[i] = min(dp[i], dp[j + 1]);
                }
            }
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 + m * k)$
- Space complexity: $O(n + m * k)$

> Where $n$ is the length of the string $s$, $m$ is the number of words in the dictionary, and $k$ is the average length of a word in the dictionary.

## Standalone solution file (`cpp/2707-extra-characters-in-a-string.cpp` in the NeetCode repo)

```cpp
/*
  You are given a 0-indexed string s and a dictionary of words dictionary. 
  You have to break s into one or more non-overlapping substrings such that each substring is present in dictionary. 
  There may be some extra characters in s which are not present in any of the substrings.

  Return the minimum number of extra characters left over if you break up s optimally.

  Ex. Input: s = "leetscode", dictionary = ["leet","code","leetcode"]
      Output: 1
      Explanation: We can break s in two substrings: "leet" from index 0 to 3 and "code" from index 5 to 8. There is only 1 unused character (at index 4), so we return 1.

  Time  : O(N^M)    M = dictionary.size(), N = s.size()
  Space : O(N)
*/

class Solution {
public:
    int minExtraChar(string s, vector<string>& dictionary) {
        int n = s.size();
        vector<int> dp(n + 1, n);

        dp[0] = 0; 

        for (int i = 1; i <= n; ++i) {
            for(int j = 0 ; j < dictionary.size() ; ++j) {
                int len = dictionary[j].size();
                if (i >= len && s.substr(i - len, len) == dictionary[j]) {
                    dp[i] = min(dp[i], dp[i - len]);
                }
            }
            dp[i] = min(dp[i], dp[i - 1] + 1);
        }

        return dp[n];
    }
};
```
