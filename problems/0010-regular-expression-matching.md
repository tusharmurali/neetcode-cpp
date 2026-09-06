# 10. Regular Expression Matching

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/regular-expression-matching/>  
- **NeetCode:** <https://neetcode.io/problems/regular-expression-matching>  
- **Video:** <https://www.youtube.com/watch?v=HAA8mgxlov8>  

[← Back to index](../INDEX.md)

## 1. Recursion

We need to check if the string `s` matches the pattern `p`, where:

- `.` matches any single character
- `*` means "zero or more of the previous character"

A recursive approach works because at each step we decide how to match the current part of the pattern with the current part of the string.

The function `dfs(i, j)` represents:
**"Can `s[i:]` be matched by `p[j:]`?"**

There are two main cases:

1. The next pattern character is NOT `*`
    - then the current characters must match (directly or via `.`), and we move both pointers forward.
2. The next pattern character IS `*`
    - then we have two choices:
        - **skip** the `x*` part entirely (use `*` as zero occurrences)
        - **use** the `x*` part to match one character from the string (if it matches), and stay on the same pattern index to potentially match more

```cpp
class Solution {
public:
    bool isMatch(string s, string p) {
        int m = s.size(), n = p.size();
        return dfs(0, 0, s, p, m, n);
    }

    bool dfs(int i, int j, const string& s, const string& p, int m, int n) {
        if (j == n) return i == m;

        bool match = (i < m && (s[i] == p[j] || p[j] == '.'));
        if (j + 1 < n && p[j + 1] == '*') {
            return dfs(i, j + 2, s, p, m, n) ||
                   (match && dfs(i + 1, j, s, p, m, n));
        }

        if (match) {
            return dfs(i + 1, j + 1, s, p, m, n);
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ {m + n})$
- Space complexity: $O(m + n)$

> Where $m$ is the length of the string $s$ and $n$ is the length of the string $p$.

## 2. Dynamic Programming (Top-Down)

We need to check if `s` matches pattern `p`, where:

- `.` matches any single character
- `*` means "zero or more of the previous character"

A recursive solution explores all matching possibilities, especially because `*` can represent many choices.
However, the same `(i, j)` states get recomputed multiple times, making plain recursion slow.

So we use **top-down dynamic programming (memoization)**.

We define `dfs(i, j)` as:
**"Can the substring `s[i:]` match the pattern `p[j:]`?"**

Whenever we compute the answer for a state `(i, j)`, we store it in a cache so future calls can reuse it instantly.

```cpp
class Solution {
    vector<vector<int>> dp;

public:
    bool isMatch(string s, string p) {
        int m = s.length(), n = p.length();
        dp.assign(m + 1, vector<int>(n + 1, -1));
        return dfs(0, 0, s, p, m, n);
    }

private:
    bool dfs(int i, int j, string& s, string& p, int m, int n) {
        if (j == n) {
            return i == m;
        }
        if (dp[i][j] != -1) {
            return dp[i][j];
        }
        bool match = i < m && (s[i] == p[j] || p[j] == '.');
        if (j + 1 < n && p[j + 1] == '*') {
            dp[i][j] = dfs(i, j + 2, s, p, m, n) ||
                       (match && dfs(i + 1, j, s, p, m, n));
        } else {
            dp[i][j] = match && dfs(i + 1, j + 1, s, p, m, n);
        }
        return dp[i][j];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the length of the string $s$ and $n$ is the length of the string $p$.

## 3. Dynamic Programming (Bottom-Up)

We want to check whether the string `s` matches the pattern `p`, where:

- `.` matches any single character
- `*` means "zero or more of the previous character"

Instead of recursion, we can solve this using **bottom-up dynamic programming** by building answers for smaller suffixes of the strings.

We define a DP state that answers:
**"Can the substring `s[i:]` be matched by the pattern `p[j:]`?"**

By filling a table from the end of both strings toward the beginning, we ensure that when we compute a state, all the states it depends on are already known.

```cpp
class Solution {
public:
    bool isMatch(string s, string p) {
        int m = s.length(), n = p.length();
        vector<vector<bool>> dp(m + 1, vector<bool>(n + 1, false));
        dp[m][n] = true;

        for (int i = m; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                bool match = i < m && (s[i] == p[j] || p[j] == '.');

                if ((j + 1) < n && p[j + 1] == '*') {
                    dp[i][j] = dp[i][j + 2];
                    if (match) {
                        dp[i][j] = dp[i + 1][j] || dp[i][j];
                    }
                } else if (match) {
                    dp[i][j] = dp[i + 1][j + 1];
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

> Where $m$ is the length of the string $s$ and $n$ is the length of the string $p$.

## 4. Dynamic Programming (Space Optimized)

We need to determine if string `s` matches pattern `p`, where:

- `.` matches any single character
- `*` means "zero or more of the previous character"

In the bottom-up DP solution, we used a 2D table `dp[i][j]` meaning:
**"Does `s[i:]` match `p[j:]`?"**

But each row `i` only depends on:

- the next row (`i + 1`)
- values within the current row while moving across `j`

So we don't need the full 2D table. We can compress it into:

- `dp` → represents the row for `i + 1`
- `nextDp` → represents the row for `i`

This keeps the same logic while using much less memory.

```cpp
class Solution {
public:
    bool isMatch(string s, string p) {
        vector<bool> dp(p.length() + 1, false);
        dp[p.length()] = true;

        for (int i = s.length(); i >= 0; i--) {
            vector<bool> nextDp(p.length() + 1, false);
            nextDp[p.length()] = (i == s.length());

            for (int j = p.length() - 1; j >= 0; j--) {
                bool match = i < s.length() &&
                             (s[i] == p[j] || p[j] == '.');

                if (j + 1 < p.length() && p[j + 1] == '*') {
                    nextDp[j] = nextDp[j + 2];
                    if (match) {
                        nextDp[j] = nextDp[j] || dp[j];
                    }
                } else if (match) {
                    nextDp[j] = dp[j + 1];
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

> Where $m$ is the length of the string $s$ and $n$ is the length of the string $p$.

## 5. Dynamic Programming (Optimal)

We want to check if `s` matches `p`, where:

- `.` matches any single character
- `*` means "zero or more of the previous character"

The usual bottom-up DP state is:
**`dp[i][j]` = does `s[i:]` match `p[j:]`?**

A 2D table works, and a 1D array also works if we update carefully.
This "optimal" version goes one step further: it updates the 1D array **in-place** without creating a second array.

The main challenge with in-place updates is that some transitions need the **diagonal value**:

- `dp[i + 1][j + 1]` (move both forward)

When we compress to 1D, that diagonal value would get overwritten while we move left through `j`.
To handle this, we keep one extra variable (`dp1`) that stores the previous diagonal value as we update the row.

So at each `(i, j)` we can still access:

- `dp[j]` → old value for `dp[i + 1][j]`
- `dp[j + 2]` → current row value for skipping `x*`
- `dp1` → old diagonal `dp[i + 1][j + 1]`

```cpp
class Solution {
public:
    bool isMatch(string s, string p) {
        vector<bool> dp(p.length() + 1, false);
        dp[p.length()] = true;

        for (int i = s.length(); i >= 0; i--) {
            bool dp1 = dp[p.length()];
            dp[p.length()] = (i == s.length());

            for (int j = p.length() - 1; j >= 0; j--) {
                bool match = i < s.length() &&
                             (s[i] == p[j] || p[j] == '.');
                bool res = false;
                if (j + 1 < p.length() && p[j + 1] == '*') {
                    res = dp[j + 2];
                    if (match) {
                        res = res || dp[j];
                    }
                } else if (match) {
                    res = dp1;
                }
                dp1 = dp[j];
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

> Where $m$ is the length of the string $s$ and $n$ is the length of the string $p$.

## Standalone solution file (`cpp/0010-regular-expression-matching.cpp` in the NeetCode repo)

```cpp
/*
    Given string & pattern, implement RegEx matching
    '.' -> matches any single character
    '*' -> matches zero or more of the preceding element
    Matching should cover the entire input string (not partial)
    Ex. s = "aa", p = "a" -> false, "a" doesn't match entire string "aa"

    DFS + memo, 2 choices at a *: either use it, or don't use it

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    bool isMatch(string s, string p) {
        return dfs(s, p, 0, 0);
    }
private:
    map<pair<int, int>, bool> dp;
    
    bool dfs(string& s, string& p, int i, int j) {
        if (dp.find({i, j}) != dp.end()) {
            return dp[{i, j}];
        }
        
        if (i >= s.size() && j >= p.size()) {
            return true;
        }
        if (j >= p.size()) {
            return false;
        }
        
        bool match = i < s.size() && (s[i] == p[j] || p[j] == '.');
        if (j + 1 < p.size() && p[j + 1] == '*') {
            // choices: either (1) don't use *, or (2) use *
            dp[{i, j}] = dfs(s, p, i, j + 2) || (match && dfs(s, p, i + 1, j));
            return dp[{i, j}];
        }
        
        if (match) {
            dp[{i, j}] = dfs(s, p, i + 1, j + 1);
            return dp[{i, j}];
        }
        
        dp[{i, j}] = false;
        return dp[{i, j}];
    }
};
```
