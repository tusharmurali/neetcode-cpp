# 97. Interleaving String

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/interleaving-string/>  
- **NeetCode:** <https://neetcode.io/problems/interleaving-string>  
- **Video:** <https://www.youtube.com/watch?v=3Rw3p9LrgvE>  
- **Video approach:** 3. Dynamic Programming (Bottom-Up)  

[← Back to index](../INDEX.md)

## 1. Recursion

This problem asks whether the string `s3` can be formed by **interleaving** characters from `s1` and `s2`, while keeping the relative order of characters from each string.

At any position in `s3`, we have at most two choices:

- take the next character from `s1`
- take the next character from `s2`

Using recursion, we try all valid ways of building `s3` character by character.  
The recursive function represents:  
**“Can we form `s3` starting from index `k`, using characters from `s1` starting at `i` and `s2` starting at `j`?”**

If we successfully consume all characters of `s3` and also reach the end of both `s1` and `s2`, then `s3` is a valid interleaving.

```cpp
class Solution {
public:
    bool isInterleave(string s1, string s2, string s3) {
        return dfs(0, 0, 0, s1, s2, s3);
    }

    bool dfs(int i, int j, int k, string& s1, string& s2, string& s3) {
        if (k == s3.length()) {
            return (i == s1.length()) && (j == s2.length());
        }

        if (i < s1.length() && s1[i] == s3[k]) {
            if (dfs(i + 1, j, k + 1, s1, s2, s3)) {
                return true;
            }
        }

        if (j < s2.length() && s2[j] == s3[k]) {
            if (dfs(i, j + 1, k + 1, s1, s2, s3)) {
                return true;
            }
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ {m + n})$
- Space complexity: $O(m + n)$

> Where $m$ is the length of the string $s1$ and $n$ is the length of the string $s2$.

## 2. Dynamic Programming (Top-Down)

This problem asks whether the string `s3` can be formed by interleaving characters from `s1` and `s2` while preserving the relative order of characters in both strings.

The recursive approach explores all possible interleavings, but many states repeat. To make it efficient, we use **top-down dynamic programming (memoization)**.

A key observation is that the position in `s3` is always determined by how many characters we have already taken from `s1` and `s2`.  
So the state can be defined using just:

- index `i` in `s1`
- index `j` in `s2`

The recursive function answers:  
**“Can we form the rest of `s3` using `s1[i:]` and `s2[j:]`?”**

```cpp
class Solution {
    vector<vector<int>> dp;

public:
    bool isInterleave(string s1, string s2, string s3) {
        int m = s1.length(), n = s2.length();
        if (m + n != s3.length()) return false;
        dp = vector<vector<int>>(m + 1, vector<int>(n + 1, -1));
        return dfs(0, 0, 0, s1, s2, s3);
    }

    bool dfs(int i, int j, int k, string& s1, string& s2, string& s3) {
        if (k == s3.length()) {
            return (i == s1.length()) && (j == s2.length());
        }
        if (dp[i][j] != -1) {
            return dp[i][j];
        }

        bool res = false;
        if (i < s1.length() && s1[i] == s3[k]) {
            res = dfs(i + 1, j, k + 1, s1, s2, s3);
        }
        if (!res && j < s2.length() && s2[j] == s3[k]) {
            res = dfs(i, j + 1, k + 1, s1, s2, s3);
        }

        dp[i][j] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the length of the string $s1$ and $n$ is the length of the string $s2$.

## 3. Dynamic Programming (Bottom-Up) ▶ video

We need to check whether the string `s3` can be formed by interleaving `s1` and `s2`, while keeping the relative order of characters from both strings.

Instead of recursion, we can solve this using **bottom-up dynamic programming**.  
The idea is to determine, for every possible pair of positions `(i, j)`, whether it is possible to form the suffix of `s3` starting at position `i + j` using:

- the substring `s1[i:]`
- the substring `s2[j:]`

If either taking the next character from `s1` or from `s2` leads to a valid state, then the current state is also valid.

```cpp
class Solution {
public:
    bool isInterleave(string s1, string s2, string s3) {
        int m = s1.length(), n = s2.length();
        if (m + n != s3.length()) {
            return false;
        }

        vector<vector<bool>> dp(m + 1, vector<bool>(n + 1, false));
        dp[m][n] = true;

        for (int i = m; i >= 0; i--) {
            for (int j = n; j >= 0; j--) {
                if (i < m && s1[i] == s3[i + j] && dp[i + 1][j]) {
                    dp[i][j] = true;
                }
                if (j < n && s2[j] == s3[i + j] && dp[i][j + 1]) {
                    dp[i][j] = true;
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

> Where $m$ is the length of the string $s1$ and $n$ is the length of the string $s2$.

## 4. Dynamic Programming (Space Optimized)

We want to know if `s3` can be built by interleaving `s1` and `s2` while keeping the order of characters from each string.

In the 2D DP solution, we used a table `dp[i][j]` to represent whether `s3[i + j:]` can be formed using `s1[i:]` and `s2[j:]`.  
But notice something important: to compute row `i`, we only need information from:

- the row below (`i + 1`) and
- the current row as we move across columns

So we do not need the full 2D table. We can compress it and keep only **one row at a time**, which reduces memory usage.

To make this even more efficient, we ensure that `s2` is the longer string so the 1D array stays as small as possible.

```cpp
class Solution {
public:
    bool isInterleave(string s1, string s2, string s3) {
        int m = s1.size(), n = s2.size();
        if (m + n != s3.size()) return false;
        if (n < m) {
            swap(s1, s2);
            swap(m, n);
        }

        vector<bool> dp(n + 1);
        dp[n] = true;
        for (int i = m; i >= 0; --i) {
            vector<bool> nextDp(n + 1);
            if (i == m) nextDp[n] = true;
            for (int j = n; j >= 0; --j) {
                if (i < m && s1[i] == s3[i + j] && dp[j]) {
                    nextDp[j] = true;
                }
                if (j < n && s2[j] == s3[i + j] && nextDp[j + 1]) {
                    nextDp[j] = true;
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

> Where $m$ is the length of the string $s1$ and $n$ is the length of the string $s2$.

## 5. Dynamic Programming (Optimal)

We want to check if `s3` can be formed by interleaving `s1` and `s2` while keeping the order of characters from both strings.

A common DP idea is:

- at positions `(i, j)`, we have used `i` characters from `s1` and `j` characters from `s2`
- so the next character we must match in `s3` is at index `i + j`

From this state, we can move forward in two ways:

- take `s1[i]` if it matches `s3[i + j]`
- take `s2[j]` if it matches `s3[i + j]`

The 2D DP solution stores this for every `(i, j)`, but we can do better:

- each DP row only depends on the row below and the current row being built
- so we can reuse a single 1D array
- and instead of building a separate `next` array, we can update the 1D array in-place using one extra variable that tracks the “right neighbor” value

We also swap strings so that `s2` is the longer one, keeping the DP array as small as possible.

```cpp
class Solution {
public:
    bool isInterleave(string s1, string s2, string s3) {
        int m = s1.size(), n = s2.size();
        if (m + n != s3.size()) return false;
        if (n < m) {
            swap(s1, s2);
            swap(m, n);
        }

        vector<bool> dp(n + 1, false);
        dp[n] = true;
        for (int i = m; i >= 0; i--) {
            bool nextDp = (i == m ? true : false);
            for (int j = n; j >= 0; j--) {
                bool res = (j < n ? false : nextDp);
                if (i < m && s1[i] == s3[i + j] && dp[j]) {
                    res = true;
                }
                if (j < n && s2[j] == s3[i + j] && nextDp) {
                    res = true;
                }
                dp[j] = res;
                nextDp = dp[j];
            }
        }
        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(min(m, n))$

> Where $m$ is the length of the string $s1$ and $n$ is the length of the string $s2$.

## Standalone solution file (`cpp/0097-interleaving-string.cpp` in the NeetCode repo)

```cpp
/*
    Given 3 strings, find if s3 is formed by interleaving of s1 & s2
    Ex. s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac" -> true

    DFS + memo, cache on s1 & s2 indices i & j
    2 choices: either take s1 & iterate i, or take s2 & iterate j

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    bool isInterleave(string s1, string s2, string s3) {
        if (s3.size() != s1.size() + s2.size()) {
            return false;
        }
        return dfs(s1, s2, s3, 0, 0);
    }
private:
    map<pair<int, int>, bool> dp;
    
    bool dfs(string s1, string s2, string s3, int i, int j) {
        if (i == s1.size() && j == s2.size()) {
            return true;
        }
        if (dp.find({i, j}) != dp.end()) {
            return dp[{i, j}];
        }
        
        if (i < s1.size() && s1[i] == s3[i + j] && dfs(s1, s2, s3, i + 1, j)) {
            return true;
        }
        if (j < s2.size() && s2[j] == s3[i + j] && dfs(s1, s2, s3, i, j + 1)) {
            return true;
        }
        
        dp[{i, j}] = false;
        return dp[{i, j}];
    }
};
```
