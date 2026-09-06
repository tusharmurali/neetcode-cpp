# 1048. Longest String Chain

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/longest-string-chain/>  
- **NeetCode:** <https://neetcode.io/problems/longest-string-chain>  
- **Video:** <https://www.youtube.com/watch?v=7b0V1gT_TIk>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

A word chain is built by repeatedly adding one character to form the next word. If we think backwards, each word can potentially extend to multiple shorter words by removing one character at a time. We can model this as a graph where each word points to its predecessors (words formed by deleting one character).

For each word, we try removing each character one at a time and check if that predecessor exists in our word list. If it does, we recursively find the longest chain starting from that predecessor. Memoization ensures we don't recompute chains for words we've already processed.

```cpp
class Solution {
public:
    int longestStrChain(vector<string>& words) {
        sort(words.begin(), words.end(), [](const string& a, const string& b) {
            return b.length() < a.length();
        });

        unordered_map<string, int> wordIndex;
        for (int i = 0; i < words.size(); i++) {
            wordIndex[words[i]] = i;
        }

        vector<int> dp(words.size(), -1);
        int maxChain = 1;
        for (int i = 0; i < words.size(); i++) {
            maxChain = max(maxChain, dfs(i, words, wordIndex, dp));
        }
        return maxChain;
    }

private:
    int dfs(int i, vector<string>& words, unordered_map<string, int>& wordIndex, vector<int>& dp) {
        if (dp[i] != -1) {
            return dp[i];
        }

        int res = 1;
        string w = words[i];
        for (int j = 0; j < w.length(); j++) {
            string pred = w.substr(0, j) + w.substr(j + 1);
            if (wordIndex.find(pred) != wordIndex.end()) {
                res = max(res, 1 + dfs(wordIndex[pred], words, wordIndex, dp));
            }
        }
        dp[i] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m ^ 2)$
- Space complexity: $O(n * m)$

> Where $n$ is the number of words and $m$ is the average length of each word.

## 2. Dynamic Programming (Bottom-Up)

We can build chains from shorter words to longer words. By sorting words by length, we ensure that when we process a word, all potential predecessors have already been processed. For each word, we check all previous words of length exactly one less to see if the current word can be formed by adding one character.

```cpp
class Solution {
public:
    int longestStrChain(vector<string>& words) {
        sort(words.begin(), words.end(), [](const string& a, const string& b) {
            return a.length() < b.length();
        });

        int n = words.size();
        vector<int> dp(n, 1);

        for (int i = 1; i < n; i++) {
            for (int j = i - 1; j >= 0; j--) {
                if (words[j].length() + 1 < words[i].length()) {
                    break;
                }
                if (words[j].length() + 1 > words[i].length() || !isPred(words[j], words[i])) {
                    continue;
                }
                dp[i] = max(dp[i], 1 + dp[j]);
            }
        }

        return *max_element(dp.begin(), dp.end());
    }

private:
    bool isPred(const string& w1, const string& w2) {
        int i = 0;
        for (char c : w2) {
            if (i == w1.length()) {
                return true;
            }
            if (w1[i] == c) {
                i++;
            }
        }
        return i == w1.length();
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * m)$
- Space complexity: $O(n)$

> Where $n$ is the number of words and $m$ is the average length of each word.

## 3. Dynamic Programming (Bottom-Up Optimized)

Instead of comparing each word with all shorter words, we can generate all possible predecessors by removing one character at a time. Using a hash map to store the longest chain ending at each word, we can look up predecessors in O(1) time. This avoids the expensive pairwise comparisons of the previous approach.

```cpp
class Solution {
public:
    int longestStrChain(vector<string>& words) {
        sort(words.begin(), words.end(), [](const string& a, const string& b) {
            return a.length() < b.length();
        });

        unordered_map<string, int> dp;
        int res = 0;

        for (const string& word : words) {
            dp[word] = 1;
            for (int i = 0; i < word.length(); i++) {
                string pred = word.substr(0, i) + word.substr(i + 1);
                if (dp.find(pred) != dp.end()) {
                    dp[word] = max(dp[word], dp[pred] + 1);
                }
            }
            res = max(res, dp[word]);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m ^ 2)$
- Space complexity: $O(n * m)$

> Where $n$ is the number of words and $m$ is the average length of each word.
