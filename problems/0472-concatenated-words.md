# 472. Concatenated Words

- **Difficulty:** Hard  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/concatenated-words/>  
- **NeetCode:** <https://neetcode.io/problems/concatenated-words>  
- **Video:** <https://www.youtube.com/watch?v=iHp7fjw1R28>  

[← Back to index](../INDEX.md)

## 1. Brute Force (Backtracking)

We can generate all possible concatenations of words and check if any concatenation exists in our word set. By building concatenations through backtracking and checking membership, we find words that are formed by joining two or more shorter words.

```cpp
class Solution {
private:
    unordered_set<string> wordSet;
    int maxLen;
    vector<string> res;
    vector<string> words;

public:
    vector<string> findAllConcatenatedWordsInADict(vector<string>& words) {
        this->words = words;
        wordSet = unordered_set<string>(words.begin(), words.end());
        maxLen = 0;
        res.clear();

        for (const string& w : words) {
            maxLen = max(maxLen, (int)w.length());
        }

        vector<string> concatWord;
        dfs(concatWord, 0);
        return res;
    }

private:
    void dfs(vector<string>& concatWord, int totLen) {
        if (concatWord.size() > 1) {
            string word = accumulate(concatWord.begin(), concatWord.end(), string(""));
            if (wordSet.count(word)) {
                res.push_back(word);
                wordSet.erase(word);
            }
        }

        for (const string& word : words) {
            if (totLen + word.size() > maxLen) continue;
            concatWord.push_back(word);
            dfs(concatWord, totLen + word.length());
            concatWord.pop_back();
        }
    }
};
```

**Complexity**

- Time complexity: $O(m * n ^ n)$
- Space complexity: $O(m * n)$

> Where $n$ is the size of the string array $words$ and $m$ is the length of the longest word in the array.

## 2. Recursion

For each word, we check if it can be split into parts where each part exists in the word set. We try every possible prefix; if a prefix is in the set, we recursively check if the remaining suffix can also be decomposed (or is itself in the set).

```cpp
class Solution {
public:
    vector<string> findAllConcatenatedWordsInADict(vector<string>& words) {
        unordered_set<string> wordSet(words.begin(), words.end());
        vector<string> res;

        for (const string& w : words) {
            if (dfs(w, wordSet)) {
                res.push_back(w);
            }
        }
        return res;
    }

private:
    bool dfs(const string& word, unordered_set<string>& wordSet) {
        for (int i = 1; i < word.size(); i++) {
            string prefix = word.substr(0, i);
            string suffix = word.substr(i);

            if ((wordSet.count(prefix) && wordSet.count(suffix)) ||
                (wordSet.count(prefix) && dfs(suffix, wordSet))) {
                return true;
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n * m ^ 4)$
- Space complexity: $O(n * m)$

> Where $n$ is the size of the string array $words$ and $m$ is the length of the longest word in the array.

## 3. Dynamic Programming (Top-Down)

The recursive approach has overlapping subproblems since the same suffix may be checked multiple times. By memoizing results for each suffix, we avoid recomputing whether a substring can be decomposed.

```cpp
class Solution {
    unordered_map<string, bool> dp;

public:
    vector<string> findAllConcatenatedWordsInADict(vector<string>& words) {
        unordered_set<string> wordSet(words.begin(), words.end());
        vector<string> res;

        for (const string& w : words) {
            if (dfs(w, wordSet)) {
                res.push_back(w);
            }
        }
        return res;
    }

private:
    bool dfs(const string& word, unordered_set<string>& wordSet) {
        if (dp.count(word)) {
            return dp[word];
        }

        for (int i = 1; i < word.size(); i++) {
            string prefix = word.substr(0, i);
            string suffix = word.substr(i);

            if ((wordSet.count(prefix) && wordSet.count(suffix)) ||
                (wordSet.count(prefix) && dfs(suffix, wordSet))) {
                dp[word] = true;
                return true;
            }
        }
        dp[word] = false;
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n * m ^ 3)$
- Space complexity: $O(n * m)$

> Where $n$ is the size of the string array $words$ and $m$ is the length of the longest word in the array.

## 4. Dynamic Programming (Bottom-Up)

For each word, we use a DP array where `dp[i]` indicates whether the substring from index `0` to `i` can be formed by concatenating words from the set. We build this array iteratively by checking all possible split points.

```cpp
class Solution {
public:
    vector<string> findAllConcatenatedWordsInADict(vector<string>& words) {
        unordered_set<string> wordSet(words.begin(), words.end());
        vector<string> res;

        for (string& word : words) {
            int m = word.length();
            vector<bool> dp(m + 1, false);
            dp[0] = true;

            for (int i = 1; i <= m; i++) {
                for (int j = 0; j < i; j++) {
                    if (j == 0 && i == m) continue;
                    if (dp[j] && wordSet.count(word.substr(j, i - j))) {
                        dp[i] = true;
                        break;
                    }
                }
            }

            if (dp[m]) {
                res.push_back(word);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m ^ 3)$
- Space complexity: $O(n * m)$

> Where $n$ is the size of the string array $words$ and $m$ is the length of the longest word in the array.
