# 115. Distinct Subsequences

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/distinct-subsequences/>  
- **NeetCode:** <https://neetcode.io/problems/count-subsequences>  
- **Video:** <https://www.youtube.com/watch?v=-RDzMJ33nx8>  

[← Back to index](../INDEX.md)

## 1. Recursion

This problem asks how many **distinct subsequences** of string `s` are equal to string `t`.

A subsequence is formed by deleting some characters from `s` without changing the order of the remaining characters.

At every position in `s`, we have a choice:

- **skip** the current character in `s`
- **use** the current character, but only if it matches the current character in `t`

The recursive function represents:  
**“How many ways can we form `t[j:]` using characters from `s[i:]`?”**

If we successfully match all characters of `t`, we have found one valid subsequence.

```cpp
class Solution {
public:
    int numDistinct(string s, string t) {
        if (t.length() > s.length()) {
            return 0;
        }
        return dfs(s, t, 0, 0);
    }

private:
    int dfs(const string &s, const string &t, int i, int j) {
        if (j == t.length()) {
            return 1;
        }
        if (i == s.length()) {
            return 0;
        }

        int res = dfs(s, t, i + 1, j);
        if (s[i] == t[j]) {
            res += dfs(s, t, i + 1, j + 1);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ m)$
- Space complexity: $O(m)$

> Where $m$ is the length of the string $s$.

## 2. Dynamic Programming (Top-Down)

This problem asks us to count how many **distinct subsequences** of string `s` are equal to string `t`.

The recursive solution works by trying all possibilities, but it repeats the same subproblems many times. To make it efficient, we use **top-down dynamic programming (memoization)**.

A state is uniquely identified by:

- `i`: the current index in `s`
- `j`: the current index in `t`

The recursive function answers the question:  
**“How many ways can we form `t[j:]` using characters from `s[i:]`?”**

By storing the result for each `(i, j)` pair, we avoid recomputing the same state again and again.

```cpp
class Solution {
    vector<vector<int>> dp;
public:
    int numDistinct(string s, string t) {
        int m = s.size(), n = t.size();
        if (n > m) return 0;
        dp.assign(m + 1, vector<int>(n + 1, -1));
        return dfs(s, t, 0, 0);
    }

private:
    int dfs(const string &s, const string &t, int i, int j) {
        if (j == t.size()) return 1;
        if (i == s.size()) return 0;
        if (dp[i][j] != -1) return dp[i][j];

        int res = dfs(s, t, i + 1, j);
        if (s[i] == t[j]) {
            res += dfs(s, t, i + 1, j + 1);
        }
        dp[i][j] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the length of the string $s$ and $n$ is the length of the string $t$.

## 3. Dynamic Programming (Bottom-Up)

We want to count how many **distinct subsequences** of string `s` are equal to string `t`.

A subsequence is formed by deleting characters from `s` without changing the order.  
So for every character in `s`, we have a choice:

- **skip** it
- **use** it (only if it matches the current character in `t`)

Instead of solving this recursively, we use **bottom-up dynamic programming** by building answers for smaller suffixes first.

We define a DP state that answers:  
**“How many ways can we form `t[j:]` using `s[i:]`?”**

By filling a DP table from the end of the strings toward the beginning, we ensure that all required subproblems are already solved.

```cpp
class Solution {
public:
    int numDistinct(string s, string t) {
        int m = s.length(), n = t.length();
        vector<vector<uint>> dp(m + 1, vector<uint>(n + 1, 0));

        for (int i = 0; i <= m; i++) {
            dp[i][n] = 1;
        }

        for (int i = m - 1; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                dp[i][j] = dp[i + 1][j];
                if (s[i] == t[j]) {
                    dp[i][j] += dp[i + 1][j + 1];
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

> Where $m$ is the length of the string $s$ and $n$ is the length of the string $t$.

## 4. Dynamic Programming (Space Optimized)

We want to count how many **distinct subsequences** of string `s` are equal to string `t`.

From the bottom-up DP approach, we know that:

- `dp[i][j]` depends only on values from the **next row** (`i + 1`)
- we never need older rows once a new row is computed

This means we can **optimize space** by keeping only two 1D arrays:

- one representing results for `i + 1`
- one representing results for the current `i`

The key idea stays the same:
At each position, we can either:

- skip the current character in `s`
- or use it if it matches the current character in `t`

```cpp
class Solution {
public:
    int numDistinct(string s, string t) {
        int m = s.size(), n = t.size();
        vector<uint> dp(n + 1, 0);
        vector<uint> nextDp(n + 1, 0);
        dp[n] = nextDp[n] = 1;

        for (int i = m - 1; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                nextDp[j] = dp[j];
                if (s[i] == t[j]) {
                    nextDp[j] += dp[j + 1];
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
- Space complexity: $O(n)$

> Where $m$ is the length of the string $s$ and $n$ is the length of the string $t$.

## 5. Dynamic Programming (Optimal)

We want to count how many **distinct subsequences** of `s` equal `t`.

From the classic DP idea:

- `dp[i][j]` = number of ways to form `t[j:]` using `s[i:]`
- Transition:
    - always can skip `s[i]` -> `dp[i+1][j]`
    - if `s[i] == t[j]`, we can also match them -> `dp[i+1][j+1]`

The space-optimized version uses a 1D array where `dp[j]` represents the values from the "next row" (`i+1`).
But when updating `dp[j]` in-place, we still need access to the old value of `dp[j+1]` (which corresponds to `dp[i+1][j+1]`).

To solve this without an extra array, we carry that needed diagonal value using a single variable (`prev`), which always holds the correct "old `dp[j+1]`" for the current update.

```cpp
class Solution {
public:
    int numDistinct(string s, string t) {
        int m = s.size(), n = t.size();
        vector<uint> dp(n + 1, 0);
        dp[n] = 1;

        for (int i = m - 1; i >= 0; i--) {
            int prev = 1;
            for (int j = n - 1; j >= 0; j--) {
                uint res = dp[j];
                if (s[i] == t[j]) {
                    res += prev;
                }

                prev = dp[j];
                dp[j] = res;
            }
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(n)$

> Where $m$ is the length of the string $s$ and $n$ is the length of the string $t$.

## Standalone solution file (`cpp/0115-distinct-subsequences.cpp` in the NeetCode repo)

```cpp
/*
    Given 2 strings s & t:
    Return # of distinct subsequences of s which equals t
    Ex. s = "rabbbit", t = "rabbit" -> 3, RABBbIT, RAbBBIT, RABbBIT

    DFS + memo, cache on i & j indices to the # of distinct subseq
    2 choices: if chars equal, look at remainder of both s & t
               if chars not equal, only look at remainder of s

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    int numDistinct(string s, string t) {
        return dfs(s, t, 0, 0);
    }
private:
    // {(i, j) -> # of distinct subsequences}
    map<pair<int, int>, int> dp;
    
    int dfs(string& s, string& t, int i, int j) {
        if (j == t.size()) {
            return 1;
        }
        if (i == s.size()) {
            return 0;
        }
        if (dp.find({i, j}) != dp.end()) {
            return dp[{i, j}];
        }
        
        if (s[i] == t[j]) {
            dp[{i, j}] = dfs(s, t, i + 1, j + 1) + dfs(s, t, i + 1, j);
        } else {
            dp[{i, j}] = dfs(s, t, i + 1, j);
        }
        return dp[{i, j}];
    }
};
```
