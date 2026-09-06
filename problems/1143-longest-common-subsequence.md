# 1143. Longest Common Subsequence

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/longest-common-subsequence/>  
- **NeetCode:** <https://neetcode.io/problems/longest-common-subsequence>  
- **Video:** <https://www.youtube.com/watch?v=Ua0GhsJSlWM>  
- **Video approach:** 3. Dynamic Programming (Bottom-Up)  

[← Back to index](../INDEX.md)

## 1. Recursion

A subsequence is a sequence derived by deleting some or no characters without changing the order of the remaining elements. To find the longest common subsequence (LCS) of two strings, we compare characters one by one. If the current characters match, they contribute to the LCS, and we move both pointers forward. If they don't match, we try skipping a character from either string and take the best result. This naturally leads to a recursive approach that explores all possibilities.

```cpp
class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        return dfs(text1, text2, 0, 0);
    }

private:
    int dfs(const string& text1, const string& text2, int i, int j) {
        if (i == text1.size() || j == text2.size()) {
            return 0;
        }
        if (text1[i] == text2[j]) {
            return 1 + dfs(text1, text2, i + 1, j + 1);
        }
        return max(dfs(text1, text2, i + 1, j),
                   dfs(text1, text2, i, j + 1));
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ {m + n})$
- Space complexity: $O(m + n)$

> Where $m$ is the length of the string $text1$ and $n$ is the length of the string $text2$.

## 2. Dynamic Programming (Top-Down)

The recursive solution recalculates the same subproblems many times. For example, `dfs(2, 3)` might be called from multiple branches. By storing results in a memo table, we avoid redundant work. This transforms the exponential solution into a polynomial one.

```cpp
class Solution {
public:
    vector<vector<int>> memo;

    int longestCommonSubsequence(string text1, string text2) {
        int m = text1.size(), n = text2.size();
        memo.assign(m, vector<int>(n, -1));
        return dfs(text1, text2, 0, 0);
    }

    int dfs(string& text1, string& text2, int i, int j) {
        if (i == text1.size() || j == text2.size()) {
            return 0;
        }
        if (memo[i][j] != -1) {
            return memo[i][j];
        }
        if (text1[i] == text2[j]) {
            memo[i][j] = 1 + dfs(text1, text2, i + 1, j + 1);
        } else {
            memo[i][j] = max(dfs(text1, text2, i + 1, j),
                             dfs(text1, text2, i, j + 1));
        }
        return memo[i][j];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the length of the string $text1$ and $n$ is the length of the string $text2$.

## 3. Dynamic Programming (Bottom-Up) ▶ video

Instead of starting from the beginning and recursing forward, we can fill a 2D table iteratively from the end. The value `dp[i][j]` represents the LCS length for substrings `text1[i:]` and `text2[j:]`. By processing indices in reverse order, we ensure that when we compute `dp[i][j]`, the values we depend on (`dp[i+1][j+1]`, `dp[i+1][j]`, `dp[i][j+1]`) are already computed.

```cpp
class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        vector<vector<int>> dp(text1.size() + 1,
                               vector<int>(text2.size() + 1));

        for (int i = text1.size() - 1; i >= 0; i--) {
            for (int j = text2.size() - 1; j >= 0; j--) {
                if (text1[i] == text2[j]) {
                    dp[i][j] = 1 + dp[i + 1][j + 1];
                } else {
                    dp[i][j] = max(dp[i][j + 1], dp[i + 1][j]);
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

> Where $m$ is the length of the string $text1$ and $n$ is the length of the string $text2$.

## 4. Dynamic Programming (Space Optimized)

Looking at the bottom-up recurrence, each cell `dp[i][j]` only depends on the current row and the next row. We don't need the entire 2D table; two 1D arrays suffice. We keep a `prev` array for the next row and a `curr` array for the current row, swapping them after each row is processed.

```cpp
class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        if (text1.size() < text2.size()) {
            swap(text1, text2);
        }

        vector<int> prev(text2.size() + 1, 0);
        vector<int> curr(text2.size() + 1, 0);

        for (int i = text1.size() - 1; i >= 0; --i) {
            for (int j = text2.size() - 1; j >= 0; --j) {
                if (text1[i] == text2[j]) {
                    curr[j] = 1 + prev[j + 1];
                } else {
                    curr[j] = max(curr[j + 1], prev[j]);
                }
            }
            swap(prev, curr);
        }

        return prev[0];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(min(m, n))$

> Where $m$ is the length of the string $text1$ and $n$ is the length of the string $text2$.

## 5. Dynamic Programming (Optimal)

We can reduce space further by using a single array and a temporary variable. When iterating right to left within a row, we need the old value at position `j` (which becomes `dp[i+1][j]` in 2D terms) before overwriting it. We store this in a variable `prev` before the update, then use it for the diagonal reference in the next iteration.

```cpp
class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        if (text1.size() < text2.size()) {
            swap(text1, text2);
        }

        vector<int> dp(text2.size() + 1, 0);

        for (int i = text1.size() - 1; i >= 0; --i) {
            int prev = 0;
            for (int j = text2.size() - 1; j >= 0; --j) {
                int temp = dp[j];
                if (text1[i] == text2[j]) {
                    dp[j] = 1 + prev;
                } else {
                    dp[j] = max(dp[j], dp[j + 1]);
                }
                prev = temp;
            }
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(min(m, n))$

> Where $m$ is the length of the string $text1$ and $n$ is the length of the string $text2$.

## Standalone solution file (`cpp/1143-longest-common-subsequence.cpp` in the NeetCode repo)

```cpp
/*
    Given 2 strings, return length of longest common subsequence
    Ex. text1 = "abcde", text2 = "ace" -> 3, "ace" is LCS

                j
            a   c   e
        a   3
        b       2     --> visualization of below, build DP bottom-up
    i   c       2
        d           1
        e           1

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        int m = text1.size();
        int n = text2.size();
        
        vector<vector<int>> dp(m + 1, vector<int>(n + 1));
        
        for (int i = m - 1; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                if (text1[i] == text2[j]) {
                    dp[i][j] = 1 + dp[i + 1][j + 1];
                } else {
                    dp[i][j] = max(dp[i + 1][j], dp[i][j + 1]);
                }
            }
        }
        
        return dp[0][0];
    }
};
```
