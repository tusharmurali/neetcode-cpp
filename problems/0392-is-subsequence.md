# 392. Is Subsequence

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/is-subsequence/>  
- **NeetCode:** <https://neetcode.io/problems/is-subsequence>  
- **Video:** <https://www.youtube.com/watch?v=99RVfqklbCE>  

[← Back to index](../INDEX.md)

## 1. Recursion

To check if `s` is a subsequence of `t`, we need to find all characters of `s` in `t` in the same order, though not necessarily contiguous. Recursively, we compare the current characters of both strings: if they match, we advance both pointers; if they do not match, we only advance the pointer in `t` to continue searching. The base cases are reaching the end of `s` (success) or the end of `t` before finishing `s` (failure).

```cpp
class Solution {
public:
    bool isSubsequence(string s, string t) {
        return rec(s, t, 0, 0);
    }

private:
    bool rec(string& s, string& t, int i, int j) {
        if (i == s.size()) return true;
        if (j == t.size()) return false;
        if (s[i] == t[j]) {
            return rec(s, t, i + 1, j + 1);
        }
        return rec(s, t, i, j + 1);
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n)$

> Where $n$ is the length of the string $s$ and $m$ is the length of the string $t$.

## 2. Dynamic Programming (Top-Down)

The recursive solution may recompute the same subproblems multiple times. By adding memoization, we cache the result for each `(i, j)` state so that each pair is computed at most once. This transforms the exponential worst case into a polynomial time solution while keeping the recursive structure intact.

```cpp
class Solution {
public:
    bool isSubsequence(string s, string t) {
        int n = s.size(), m = t.size();
        vector<vector<int>> memo(n, vector<int>(m, -1));
        return rec(s, t, 0, 0, memo);
    }

private:
    bool rec(string& s, string& t, int i, int j, vector<vector<int>>& memo) {
        if (i == s.size()) return true;
        if (j == t.size()) return false;
        if (memo[i][j] != -1) return memo[i][j] == 1;
        if (s[i] == t[j]) {
            memo[i][j] = rec(s, t, i + 1, j + 1, memo) ? 1 : 0;
        } else {
            memo[i][j] = rec(s, t, i, j + 1, memo) ? 1 : 0;
        }
        return memo[i][j] == 1;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$

> Where $n$ is the length of the string $s$ and $m$ is the length of the string $t$.

## 3. Dynamic Programming (Bottom-Up)

Instead of recursion with memoization, we can fill a DP table iteratively from the end of both strings toward the beginning. The value `dp[i][j]` represents whether `s[i:]` is a subsequence of `t[j:]`. If the characters match, we look at `dp[i+1][j+1]`. Otherwise, we look at `dp[i][j+1]` (skip the character in `t`). The base case is that any suffix of `s` starting at `len(s)` is trivially a subsequence of anything (empty string).

```cpp
class Solution {
public:
    bool isSubsequence(string s, string t) {
        int n = s.size(), m = t.size();
        vector<vector<bool>> dp(n + 1, vector<bool>(m + 1, false));

        for (int j = 0; j <= m; ++j) {
            dp[n][j] = true;
        }

        for (int i = n - 1; i >= 0; --i) {
            for (int j = m - 1; j >= 0; --j) {
                if (s[i] == t[j]) {
                    dp[i][j] = dp[i + 1][j + 1];
                } else {
                    dp[i][j] = dp[i][j + 1];
                }
            }
        }

        return dp[0][0];
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$

> Where $n$ is the length of the string $s$ and $m$ is the length of the string $t$.

## 4. Two Pointers

The most efficient approach uses two pointers since we only need to make a single pass through both strings. Pointer `i` tracks our position in `s`, and pointer `j` tracks our position in `t`. We always advance `j`, but only advance `i` when we find a matching character. If we reach the end of `s`, all characters were found in order. This is optimal because each character in `t` is examined exactly once.

```cpp
class Solution {
public:
    bool isSubsequence(string s, string t) {
        int i = 0, j = 0;
        while (i < s.length() && j < t.length()) {
            if (s[i] == t[j]) {
                i++;
            }
            j++;
        }
        return i == s.length();
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(1)$

> Where $n$ is the length of the string $s$ and $m$ is the length of the string $t$.

## 5. Follow-Up Solution (Index Jumping)

When checking many strings against the same `t`, the two-pointer approach becomes inefficient because we scan `t` repeatedly. Instead, we precompute for each position in `t` the next occurrence of each character. This lets us jump directly to the next matching character rather than scanning. The preprocessing takes O(26 \* m) time and space, but each subsequence query then takes only O(n) time regardless of the length of `t`.

```cpp
class Solution {
public:
    bool isSubsequence(string s, string t) {
        int n = s.length(), m = t.length();
        if (m == 0) return n == 0;

        vector<vector<int>> store(m, vector<int>(26, m + 1));
        store[m - 1][t[m - 1] - 'a'] = m - 1;

        for (int i = m - 2; i >= 0; i--) {
            store[i] = store[i + 1];
            store[i][t[i] - 'a'] = i;
        }

        int i = 0, j = 0;
        while (i < n && j < m) {
            j = store[j][s[i] - 'a'] + 1;
            if (j > m) return false;
            i++;
        }

        return i == n;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(m)$

> Where $n$ is the length of the string $s$ and $m$ is the length of the string $t$.

## Standalone solution file (`cpp/0392-is-subsequence.cpp` in the NeetCode repo)

```cpp
// Time Complexity is O(N) where n is the size of the target string.
// Space Complexity is O(1)

class Solution {
public:
   bool isSubsequence(string s, string t) {
      int i = 0 , j = 0;
      while(j < s.size() && i < t.size())
      {
        if(s[j] == t[i])
          j++;
        
       i++;
      }
      
      if(j >= s.size()) return true;
      return false;
    }
};
```
