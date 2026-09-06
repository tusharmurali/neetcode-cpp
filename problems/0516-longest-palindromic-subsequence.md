# 516. Longest Palindromic Subsequence

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/longest-palindromic-subsequence/>  
- **NeetCode:** <https://neetcode.io/problems/longest-palindromic-subsequence>  
- **Video:** <https://www.youtube.com/watch?v=bUr8cNWI09Q>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top Down)

A palindrome reads the same forwards and backwards, so we can think of building one by expanding outward from a center. For each possible center (single character for odd length, between two characters for even length), we try to extend the palindrome by checking if the characters on both sides match.

If the characters match, we include both in our subsequence and continue expanding. If they don't match, we have a choice: skip the left character or skip the right character, and take whichever gives a longer result. Memoization prevents us from recomputing the same subproblems.

```cpp
class Solution {
private:
    vector<vector<int>> dp;

public:
    int longestPalindromeSubseq(string s) {
        int n = s.size();
        dp.resize(n, vector<int>(n, -1));

        for (int i = 0; i < n; i++) {
            dfs(i, i, s);       // Odd length
            dfs(i, i + 1, s);   // Even length
        }

        int maxLength = 0;
        for (const auto& row : dp) {
            for (int val : row) {
                maxLength = max(maxLength, val);
            }
        }

        return maxLength;
    }

private:
    int dfs(int i, int j, const string& s) {
        if (i < 0 || j == s.size()) {
            return 0;
        }
        if (dp[i][j] != -1) {
            return dp[i][j];
        }

        if (s[i] == s[j]) {
            int length = (i == j) ? 1 : 2;
            dp[i][j] = length + dfs(i - 1, j + 1, s);
        } else {
            dp[i][j] = max(dfs(i - 1, j, s), dfs(i, j + 1, s));
        }

        return dp[i][j];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 2. Dynamic Programming (Top-Down Optimized)

Instead of expanding from centers, we can approach this problem by considering the entire string and shrinking inward. We define our subproblem as finding the longest palindromic subsequence within the substring from index `i` to index `j`.

When the first and last characters match, they can both be part of our palindrome, so we add 2 and solve for the inner substring. When they don't match, one of them must be excluded, so we try both options and take the better one.

```cpp
class Solution {
private:
    vector<vector<int>> dp;

public:
    int longestPalindromeSubseq(string s) {
        int n = s.size();
        dp.resize(n, vector<int>(n, -1));
        return dfs(0, n - 1, s);
    }

private:
    int dfs(int i, int j, const string& s) {
        if (i > j) {
            return 0;
        }
        if (i == j) {
            return 1;
        }
        if (dp[i][j] != -1) {
            return dp[i][j];
        }

        if (s[i] == s[j]) {
            dp[i][j] = dfs(i + 1, j - 1, s) + 2;
        } else {
            dp[i][j] = max(dfs(i + 1, j, s), dfs(i, j - 1, s));
        }

        return dp[i][j];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Dynamic Programming (Using LCS Idea)

A clever observation: the longest palindromic subsequence of a string is the same as the longest common subsequence (LCS) between the string and its reverse. Why? Any palindromic subsequence appears in the same order when read forwards or backwards, making it a common subsequence of both strings.

This transforms our problem into the classic LCS problem, which has a well-known dynamic programming solution.

```cpp
class Solution {
public:
    int longestPalindromeSubseq(string s) {
        string reversedS = s;
        reverse(reversedS.begin(), reversedS.end());
        return longestCommonSubsequence(s, reversedS);
    }

    int longestCommonSubsequence(const string& s1, const string& s2) {
        int N = s1.size(), M = s2.size();
        vector<vector<int>> dp(N + 1, vector<int>(M + 1, 0));

        for (int i = 0; i < N; i++) {
            for (int j = 0; j < M; j++) {
                if (s1[i] == s2[j]) {
                    dp[i + 1][j + 1] = 1 + dp[i][j];
                } else {
                    dp[i + 1][j + 1] = max(dp[i + 1][j], dp[i][j + 1]);
                }
            }
        }

        return dp[N][M];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 4. Dynamic Programming (Space Optimized)

The bottom-up DP approach can be optimized for space. When filling the DP table, each cell only depends on cells from the current and previous rows (or in this formulation, the current row and the previous diagonal value). By processing in the right order and keeping track of just the necessary values, we can reduce space from O(n^2) to O(n).

```cpp
class Solution {
public:
    int longestPalindromeSubseq(string s) {
        int n = s.size();
        vector<int> dp(n, 0);

        for (int i = n - 1; i >= 0; i--) {
            dp[i] = 1;
            int prev = 0;
            for (int j = i + 1; j < n; j++) {
                int temp = dp[j];

                if (s[i] == s[j]) {
                    dp[j] = prev + 2;
                } else {
                    dp[j] = max(dp[j], dp[j - 1]);
                }

                prev = temp;
            }
        }

        return dp[n - 1];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$
