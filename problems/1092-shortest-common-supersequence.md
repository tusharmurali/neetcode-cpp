# 1092. Shortest Common Supersequence

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/shortest-common-supersequence/>  
- **NeetCode:** <https://neetcode.io/problems/shortest-common-supersequence>  
- **Video:** <https://www.youtube.com/watch?v=JkjQNJSxXN0>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

A supersequence must contain both strings as subsequences. The shortest one minimizes redundancy by sharing as many characters as possible between the two strings. This is directly related to the Longest Common Subsequence (LCS) problem.

Using recursion with memoization, at each position we have a choice: if the characters match, we include it once and move both pointers. If they differ, we try including either character and pick the shorter result. The base case handles when one string is exhausted, requiring us to append the remainder of the other.

```cpp
class Solution {
public:
    string shortestCommonSupersequence(const string &str1, const string &str2) {
        n = str1.size();
        m = str2.size();
        cache.resize(n + 1, vector<string>(m + 1, ""));
        cacheUsed.resize(n + 1, vector<bool>(m + 1, false));

        string res = dfs(0, 0, str1, str2);
        reverse(res.begin(), res.end());
        return res;
    }

private:
    int n, m;
    vector<vector<string>> cache;
    vector<vector<bool>> cacheUsed;

    string dfs(int i, int j, const string &str1, const string &str2) {
        if (cacheUsed[i][j]) {
            return cache[i][j];
        }
        cacheUsed[i][j] = true;

        if (i == n) {
            string tail = str2.substr(j);
            reverse(tail.begin(), tail.end());
            cache[i][j] = tail;
            return tail;
        }
        if (j == m) {
            string tail = str1.substr(i);
            reverse(tail.begin(), tail.end());
            cache[i][j] = tail;
            return tail;
        }

        if (str1[i] == str2[j]) {
            string temp = dfs(i + 1, j + 1, str1, str2);
            temp.push_back(str1[i]);
            cache[i][j] = temp;
        } else {
            string s1 = dfs(i + 1, j, str1, str2);
            string s2 = dfs(i, j + 1, str1, str2);
            if (s1.size() < s2.size()) {
                s1.push_back(str1[i]);
                cache[i][j] = s1;
            } else {
                s2.push_back(str2[j]);
                cache[i][j] = s2;
            }
        }
        return cache[i][j];
    }
};
```

**Complexity**

- Time complexity: $O(n * m * min(n, m))$
- Space complexity: $O(n * m * min(n, m))$

> Where $n$ and $m$ are the lengths of the strings $str1$ and $str2$ respectively.

## 2. Dynamic Programming (Top-Down) + Tracing

Building the actual string during recursion can be expensive due to string concatenation overhead. A more efficient approach is to first compute only the lengths using DP, then reconstruct the string by tracing back through the DP table.

The DP table stores the length of the shortest supersequence from each state `(i, j)`. After filling the table, we trace from `(0, 0)` to the end, at each step deciding which character to include based on the DP values.

```cpp
class Solution {
private:
    vector<vector<int>> dp;
    int n, m;

    int dfs(int i, int j, const string& str1, const string& str2) {
        if (dp[i][j] != -1) return dp[i][j];
        if (i == n) return dp[i][j] = m - j;
        if (j == m) return dp[i][j] = n - i;

        if (str1[i] == str2[j]) {
            dp[i][j] = 1 + dfs(i + 1, j + 1, str1, str2);
        } else {
            dp[i][j] = 1 + min(dfs(i + 1, j, str1, str2), dfs(i, j + 1, str1, str2));
        }
        return dp[i][j];
    }

    string buildSCS(const string& str1, const string& str2) {
        string res;
        int i = 0, j = 0;

        while (i < n || j < m) {
            if (i == n) {
                res += str2.substr(j);
                break;
            }
            if (j == m) {
                res += str1.substr(i);
                break;
            }
            if (str1[i] == str2[j]) {
                res += str1[i];
                i++;
                j++;
            } else if (dp[i + 1][j] < dp[i][j + 1]) {
                res += str1[i];
                i++;
            } else {
                res += str2[j];
                j++;
            }
        }

        return res;
    }

public:
    string shortestCommonSupersequence(string str1, string str2) {
        n = str1.size();
        m = str2.size();
        dp = vector<vector<int>>(n + 1, vector<int>(m + 1, -1));

        dfs(0, 0, str1, str2);
        return buildSCS(str1, str2);
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$

> Where $n$ and $m$ are the lengths of the strings $str1$ and $str2$ respectively.

## 3. Dynamic Programming (Bottom-Up)

Instead of recursion, we can fill the DP table iteratively from smaller subproblems to larger ones. The entry `dp[i][j]` stores the actual shortest supersequence for the prefixes `str1[0..i-1]` and `str2[0..j-1]`.

The base cases initialize the first row and column with prefixes of each string. For each cell, we either extend by a common character or choose the shorter option when characters differ.

```cpp
class Solution {
public:
    string shortestCommonSupersequence(string str1, string str2) {
        int n = str1.size(), m = str2.size();
        vector<vector<string>> dp(n + 1, vector<string>(m + 1));

        for (int i = 0; i <= n; i++) {
            for (int j = 0; j <= m; j++) {
                if (i == 0) {
                    dp[i][j] = str2.substr(0, j);
                } else if (j == 0) {
                    dp[i][j] = str1.substr(0, i);
                } else if (str1[i - 1] == str2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1] + str1[i - 1];
                } else {
                    dp[i][j] = dp[i - 1][j].size() < dp[i][j - 1].size() ?
                               dp[i - 1][j] + str1[i - 1] :
                               dp[i][j - 1] + str2[j - 1];
                }
            }
        }

        return dp[n][m];
    }
};
```

**Complexity**

- Time complexity: $O(n * m * min(n, m))$
- Space complexity: $O(n * m * min(n, m))$

> Where $n$ and $m$ are the lengths of the strings $str1$ and $str2$ respectively.

## 4. Dynamic Programming (Bottom-Up) + Tracing

Storing full strings in the DP table is memory-intensive. A more space-efficient approach stores only the lengths, then reconstructs the string by tracing backward through the table.

This is the standard approach for the problem: compute the DP table of lengths bottom-up, then trace from `(n, m)` back to `(0, 0)`, building the result string in reverse.

```cpp
class Solution {
public:
    string shortestCommonSupersequence(string str1, string str2) {
        int n = str1.size(), m = str2.size();
        vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));

        for (int i = 0; i <= n; i++) {
            for (int j = 0; j <= m; j++) {
                if (i == 0) {
                    dp[i][j] = j;
                } else if (j == 0) {
                    dp[i][j] = i;
                } else if (str1[i - 1] == str2[j - 1]) {
                    dp[i][j] = 1 + dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }

        string res;
        int i = n, j = m;
        while (i > 0 && j > 0) {
            if (str1[i - 1] == str2[j - 1]) {
                res.push_back(str1[i - 1]);
                i--;
                j--;
            } else if (dp[i - 1][j] < dp[i][j - 1]) {
                res.push_back(str1[i - 1]);
                i--;
            } else {
                res.push_back(str2[j - 1]);
                j--;
            }
        }

        while (i > 0) {
            res.push_back(str1[i - 1]);
            i--;
        }

        while (j > 0) {
            res.push_back(str2[j - 1]);
            j--;
        }

        reverse(res.begin(), res.end());
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(n * m)$

> Where $n$ and $m$ are the lengths of the strings $str1$ and $str2$ respectively.
