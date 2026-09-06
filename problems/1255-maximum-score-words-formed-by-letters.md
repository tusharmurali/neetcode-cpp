# 1255. Maximum Score Words Formed By Letters

- **Difficulty:** Hard  
- **Pattern:** Backtracking  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-score-words-formed-by-letters/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-score-words-formed-by-letters>  
- **Video:** <https://www.youtube.com/watch?v=1cV8Hq9IAk4>  

[← Back to index](../INDEX.md)

## 1. Backtracking

We need to select a subset of words to maximize total score, where each word consumes letters from a shared pool. This is a classic subset selection problem. For each word, we decide whether to include it (if we have enough letters) or skip it. We explore all valid combinations using recursion and backtracking, restoring the letter counts after each recursive call.

```cpp
class Solution {
public:
    vector<int> letterCnt = vector<int>(26, 0);
    vector<int> score;
    vector<string> words;

    int maxScoreWords(vector<string>& words, vector<char>& letters, vector<int>& score) {
        this->words = words;
        this->score = score;

        for (char c : letters) {
            letterCnt[c - 'a']++;
        }

        return backtrack(0);
    }

    bool canFormWord(string& word) {
        vector<int> wordCnt(26, 0);
        for (char c : word) {
            wordCnt[c - 'a']++;
            if (wordCnt[c - 'a'] > letterCnt[c - 'a']) {
                return false;
            }
        }
        return true;
    }

    int getScore(string& word) {
        int res = 0;
        for (char c : word) {
            res += score[c - 'a'];
        }
        return res;
    }

    int backtrack(int i) {
        if (i == words.size()) {
            return 0;
        }

        int res = backtrack(i + 1);  // skip
        if (canFormWord(words[i])) {  // include (when possible)
            for (char c : words[i]) {
                letterCnt[c - 'a']--;
            }
            res = max(res, getScore(words[i]) + backtrack(i + 1));
            for (char c : words[i]) {
                letterCnt[c - 'a']++;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n * (w + m) + N)$
- Space complexity: $O(n + w)$

> Where $n$ is the number of words, $w$ is the maximum length of a word, $m$ is the size of the array $scores$, and $N$ is the size of the array $letters$.

## 2. Backtracking + Precomputation

The basic backtracking approach recalculates letter frequencies and scores for each word during recursion. We can speed this up by precomputing the frequency array and score for each word upfront. This avoids redundant character-by-character processing and makes the validity check and score lookup constant time operations.

```cpp
class Solution {
public:
    vector<int> letterCnt = vector<int>(26, 0);
    vector<int> wordScores;
    vector<vector<int>> wordFreqs;
    int n;

    int maxScoreWords(vector<string>& words, vector<char>& letters, vector<int>& score) {
        fill(letterCnt.begin(), letterCnt.end(), 0);
        for (char c : letters) {
            letterCnt[c - 'a']++;
        }

        n = words.size();
        wordScores = vector<int>(n, 0);
        wordFreqs = vector<vector<int>>(n, vector<int>(26, 0));

        for (int i = 0; i < n; i++) {
            for (char c : words[i]) {
                int idx = c - 'a';
                wordFreqs[i][idx]++;
                wordScores[i] += score[idx];
            }
        }

        return backtrack(0, words);
    }

private:
    int backtrack(int i, vector<string>& words) {
        if (i == n) {
            return 0;
        }

        int res = backtrack(i + 1, words); // skip
        bool canInclude = true;

        for (int j = 0; j < 26; j++) {
            if (wordFreqs[i][j] > letterCnt[j]) {
                canInclude = false;
                break;
            }
        }

        if (canInclude) {  // include (when possible)
            for (int j = 0; j < 26; j++) {
                letterCnt[j] -= wordFreqs[i][j];
            }
            res = max(res, wordScores[i] + backtrack(i + 1, words));
            for (int j = 0; j < 26; j++) {
                letterCnt[j] += wordFreqs[i][j];
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * 2 ^ n + N)$
- Space complexity: $O(n + w)$

> Where $n$ is the number of words, $w$ is the maximum length of a word, $m$ is the size of the array $scores$, and $N$ is the size of the array $letters$.

## 3. Backtracking (Bit Mask)

Instead of recursive backtracking, we can iterate through all possible subsets using bit manipulation. With `n` words, there are `2^n` possible subsets, each representable as an integer where bit `i` indicates whether word `i` is included. For each subset (bitmask), we check if all included words can be formed simultaneously and calculate the total score.

```cpp
class Solution {
public:
    int maxScoreWords(vector<string>& words, vector<char>& letters, vector<int>& score) {
        vector<int> letterCnt(26, 0);
        for (char c : letters) {
            letterCnt[c - 'a']++;
        }

        int n = words.size();
        vector<int> wordScores(n, 0);
        vector<vector<int>> wordFreqs(n, vector<int>(26, 0));

        for (int i = 0; i < n; i++) {
            for (char c : words[i]) {
                int idx = c - 'a';
                wordFreqs[i][idx]++;
                wordScores[i] += score[idx];
            }
        }

        int res = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            int curScore = 0;
            vector<int> curLetterCnt = letterCnt;
            bool valid = true;

            for (int i = 0; i < n; i++) {
                if (mask & (1 << i)) {
                    for (int j = 0; j < 26; j++) {
                        if (wordFreqs[i][j] > curLetterCnt[j]) {
                            valid = false;
                            break;
                        }
                    }
                    if (!valid) break;

                    for (int j = 0; j < 26; j++) {
                        curLetterCnt[j] -= wordFreqs[i][j];
                    }

                    curScore += wordScores[i];
                }
            }

            if (valid) {
                res = max(res, curScore);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n * 2 ^ n + N)$
- Space complexity: $O(n + w)$

> Where $n$ is the number of words, $w$ is the maximum length of a word, $m$ is the size of the array $scores$, and $N$ is the size of the array $letters$.
