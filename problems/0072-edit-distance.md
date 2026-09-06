# 72. Edit Distance

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/edit-distance/>  
- **NeetCode:** <https://neetcode.io/problems/edit-distance>  
- **Video:** <https://www.youtube.com/watch?v=XYi2-LPrwm4>  
- **Video approach:** 3. Dynamic Programming (Bottom-Up)  

[← Back to index](../INDEX.md)

## 1. Recursion

This problem asks for the **minimum number of operations** required to convert `word1` into `word2`.  
The allowed operations are:

- insert a character
- delete a character
- replace a character

At any position in both strings, we compare characters at indices `i` and `j`.

The recursive function represents:
**"What is the minimum number of operations needed to convert `word1[i:]` into `word2[j:]`?"**

If the characters already match, we simply move forward in both strings without using any operation.
If they do not match, we try all three possible operations and take the minimum cost.

```cpp
class Solution {
public:
    int minDistance(string word1, string word2) {
        int m = word1.size(), n = word2.size();
        return dfs(0, 0, word1, word2, m, n);
    }

    int dfs(int i, int j, string& word1, string& word2, int m, int n) {
        if (i == m) return n - j;
        if (j == n) return m - i;
        if (word1[i] == word2[j]){
            return dfs(i + 1, j + 1, word1, word2, m, n);
        }

        int res = min(dfs(i + 1, j, word1, word2, m, n),
                      dfs(i, j + 1, word1, word2, m, n));
        res = min(res, dfs(i + 1, j + 1, word1, word2, m, n));
        return res + 1;
    }
};
```

**Complexity**

- Time complexity: $O(3 ^ {m + n})$
- Space complexity: $O(m + n)$

> Where $m$ is the length of $word1$ and $n$ is the length of $word2$.

## 2. Dynamic Programming (Top-Down)

This problem asks for the **minimum number of edit operations** required to convert `word1` into `word2`.  
The allowed operations are:

- insert a character
- delete a character
- replace a character

The recursive solution explores all possibilities, but many subproblems repeat. To optimize this, we use **top-down dynamic programming (memoization)**.

A state is uniquely defined by:

- `i`: current index in `word1`
- `j`: current index in `word2`

The recursive function answers:
**"What is the minimum number of operations needed to convert `word1[i:]` into `word2[j:]`?"**

By caching results for each `(i, j)` pair, we avoid recomputing the same states.

```cpp
class Solution {
    vector<vector<int>> dp;
public:
    int minDistance(string word1, string word2) {
        int m = word1.size(), n = word2.size();
        dp = vector<vector<int>>(m, vector<int>(n, -1));
        return dfs(0, 0, word1, word2, m, n);
    }

    int dfs(int i, int j, string& word1, string& word2, int m, int n) {
        if (i == m) return n - j;
        if (j == n) return m - i;
        if (dp[i][j] != -1) return dp[i][j];
        if (word1[i] == word2[j]){
            dp[i][j] = dfs(i + 1, j + 1, word1, word2, m, n);
        } else {
            int res = min(dfs(i + 1, j, word1, word2, m, n),
                        dfs(i, j + 1, word1, word2, m, n));
            res = min(res, dfs(i + 1, j + 1, word1, word2, m, n));
            dp[i][j] = res + 1;
        }
        return dp[i][j];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the length of $word1$ and $n$ is the length of $word2$.

## 3. Dynamic Programming (Bottom-Up) ▶ video

We want the **minimum number of edits** needed to convert `word1` into `word2`, where an edit can be:

- insert a character
- delete a character
- replace a character

Instead of using recursion, we can solve this using **bottom-up dynamic programming** by building the answer for smaller suffixes first.

We define a DP state that answers:
**"What is the minimum edit distance between `word1[i:]` and `word2[j:]`?"**

By filling a table from the end of the strings toward the beginning, every subproblem we need is already solved when we reach it.

```cpp
class Solution {
public:
    int minDistance(string word1, string word2) {
        vector<vector<int>> dp(word1.length() + 1,
                               vector<int>(word2.length() + 1, 0));

        for (int j = 0; j <= word2.length(); j++) {
            dp[word1.length()][j] = word2.length() - j;
        }
        for (int i = 0; i <= word1.length(); i++) {
            dp[i][word2.length()] = word1.length() - i;
        }

        for (int i = word1.length() - 1; i >= 0; i--) {
            for (int j = word2.length() - 1; j >= 0; j--) {
                if (word1[i] == word2[j]) {
                    dp[i][j] = dp[i + 1][j + 1];
                } else {
                    dp[i][j] = 1 + min(dp[i + 1][j],
                                   min(dp[i][j + 1], dp[i + 1][j + 1]));
                }
            }
        }
        return dp[0][0];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the length of $word1$ and $n$ is the length of $word2$.

## 4. Dynamic Programming (Space Optimized)

We want the minimum number of edits (insert, delete, replace) to convert `word1` into `word2`.

In the 2D DP solution, we used `dp[i][j]` to represent the answer for `word1[i:]` and `word2[j:]`.
But notice that each cell `dp[i][j]` depends only on:

- `dp[i + 1][j]` (delete)
- `dp[i][j + 1]` (insert)
- `dp[i + 1][j + 1]` (replace / match)

So when filling the table from bottom to top, we only need:

- the **next row** (`i + 1`) and
- the **current row** being built (`i`)

That means we can optimize space by keeping just two 1D arrays:

- `dp` for the next row
- `nextDp` for the current row

To reduce memory even more, we also ensure the 1D arrays are based on the **shorter string** (swap if needed).

```cpp
class Solution {
public:
    int minDistance(string word1, string word2) {
        int m = word1.size(), n = word2.size();
        if (m < n) {
            swap(m, n);
            swap(word1, word2);
        }

        vector<int> dp(n + 1), nextDp(n + 1);

        for (int j = 0; j <= n; ++j) {
            dp[j] = n - j;
        }

        for (int i = m - 1; i >= 0; --i) {
            nextDp[n] = m - i;
            for (int j = n - 1; j >= 0; --j) {
                if (word1[i] == word2[j]) {
                    nextDp[j] = dp[j + 1];
                } else {
                    nextDp[j] = 1 + min({dp[j], nextDp[j + 1], dp[j + 1]});
                }
            }
            dp = nextDp;
        }
        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(min(m, n))$

> Where $m$ is the length of $word1$ and $n$ is the length of $word2$.

## 5. Dynamic Programming (Optimal)

We want the minimum number of edits (insert, delete, replace) needed to convert `word1` into `word2`.

The classic DP idea is:

- `dp[i][j]` = minimum operations to convert `word1[i:]` into `word2[j:]`

But to compute `dp[i][j]`, we only need three neighboring states:

- `dp[i + 1][j]` (delete from `word1`)
- `dp[i][j + 1]` (insert into `word1`)
- `dp[i + 1][j + 1]` (replace, or match if characters are equal)

That means we don't need the full 2D table. We can compress it into a single 1D array `dp`, and update it row-by-row (from the end of the strings to the start).

The tricky part of in-place updates is that `dp[i + 1][j + 1]` (the diagonal value) would get overwritten.
So we carry that diagonal value using one extra variable (`nextDp`), and another temporary variable to shift it correctly while moving left.

We also swap the strings if needed so the DP array is based on the shorter word, keeping memory minimal.

```cpp
class Solution {
public:
    int minDistance(string word1, string word2) {
        int m = word1.size(), n = word2.size();
        if (m < n) {
            swap(m, n);
            swap(word1, word2);
        }

        vector<int> dp(n + 1);
        for (int i = 0; i <= n; i++) dp[i] = n - i;

        for (int i = m - 1; i >= 0; i--) {
            int nextDp = dp[n];
            dp[n] = m - i;
            for (int j = n - 1; j >= 0; j--) {
                int temp = dp[j];
                if (word1[i] == word2[j]) {
                    dp[j] = nextDp;
                } else {
                    dp[j] = 1 + min({dp[j], dp[j + 1], nextDp});
                }
                nextDp = temp;
            }
        }
        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(min(m, n))$

> Where $m$ is the length of $word1$ and $n$ is the length of $word2$.

## Standalone solution file (`cpp/0072-edit-distance.cpp` in the NeetCode repo)

```cpp
/*
    Given 2 strings, return minimum number of operations to convert word1 to word2

    Naive: check all possible edit sequences & choose shortest one
    Optimal: DP, if chars at i & j same, no operations needed, else 3 cases:
    (1) replace (i - 1, j - 1), (2) delete (i - 1, j), (3) insert (i, j - 1)

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    int minDistance(string word1, string word2) {
        if (word1.empty() && word2.empty()) {
            return 0;
        }
        if (word1.empty() || word2.empty()) {
            return 1;
        }
        
        int m = word1.size();
        int n = word2.size();
        
        vector<vector<int>> dp(m + 1, vector<int>(n + 1));
        
        // base cases (convert to empty string w/ deletions), dist is just length
        for (int i = 1; i <= m; i++) {
            dp[i][0] = i;
        }
        for (int j = 1; j <= n; j++) {
            dp[0][j] = j;
        }
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (word1[i - 1] == word2[j - 1]) {
                    // no operation needed, same char
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    // min(replace, delete, insert) + 1 <-- since an op was needed
                    dp[i][j] = min(dp[i - 1][j - 1], min(dp[i - 1][j], dp[i][j - 1])) + 1;
                }
            }
        }
        
        return dp[m][n];
    }
};

// Since we only need at most dp[i - 1][j - 1], can space optimize to O(n)
// class Solution {
// public:
//     int minDistance(string word1, string word2) {
//         int m = word1.size();
//         int n = word2.size();
//         int prev = 0;
//         vector<int> curr(n + 1);
//         for (int j = 1; j <= n; j++) {
//             curr[j] = j;
//         }
//         for (int i = 1; i <= m; i++) {
//             prev = curr[0];
//             curr[0] = i;
//             for (int j = 1; j <= n; j++) {
//                 int temp = curr[j];
//                 if (word1[i - 1] == word2[j - 1]) {
//                     curr[j] = prev;
//                 } else {
//                     curr[j] = min(prev, min(curr[j - 1], curr[j])) + 1;
//                 }
//                 prev = temp;
//             }
//         }
//         return curr[n];
//     }
// };
```
