# 1639. Number of Ways to Form a Target String Given a Dictionary

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-ways-to-form-a-target-string-given-a-dictionary/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-ways-to-form-a-target-string-given-a-dictionary>  
- **Video:** <https://www.youtube.com/watch?v=_GF-0T-YjW8>  

[← Back to index](../INDEX.md)

## 1. Recursion

We build the target string character by character. For each target character, we can pick it from any word at the current column position, then move to the next column. We can also skip columns without picking anything. The constraint is that once we use a column, we cannot go back to previous columns.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;

    int dfs(vector<string>& words, string target, int i, int k) {
        if (i == target.length()) return 1;
        if (k == words[0].length()) return 0;

        int res = dfs(words, target, i, k + 1);
        for (string& w : words) {
            if (w[k] != target[i]) {
                continue;
            }
            res = (int) (res + 0LL + dfs(words, target, i + 1, k + 1)) % MOD;
        }

        return res;
    }

public:
    int numWays(vector<string>& words, string target) {
        return dfs(words, target, 0, 0);
    }
};
```

**Complexity**

- Time complexity: $O(N ^ m)$
- Space complexity: $O(m)$

> Where $N$ is the number of words, $m$ is the length of each word, and $n$ is the length of the $target$ string.

## 2. Dynamic Programming (Top-Down)

The naive recursion is slow because we check every word at each step. We can precompute how many times each character appears at each column position. Then instead of iterating through all words, we simply multiply by the count of matching characters.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;
    vector<vector<int>> dp;
    vector<vector<int>> cnt;

public:
    int numWays(vector<string>& words, string target) {
        int n = target.size(), m = words[0].size();
        cnt = vector<vector<int>>(m, vector<int>(26, 0));

        for (const string& word : words) {
            for (int i = 0; i < word.size(); i++) {
                cnt[i][word[i] - 'a']++;
            }
        }

        dp = vector<vector<int>>(n + 1, vector<int>(m + 1, -1));
        return dfs(0, 0, target, n, m);
    }

private:
    int dfs(int i, int k, const string& target, int n, int m) {
        if (i == n) return 1;
        if (k == m) return 0;
        if (dp[i][k] != -1) return dp[i][k];

        int c = target[i] - 'a';
        dp[i][k] = dfs(i, k + 1, target, n, m);  // Skip k position
        dp[i][k] = (dp[i][k] + (long long) cnt[k][c] * dfs(i + 1, k + 1, target, n, m)) % MOD;
        return dp[i][k];
    }
};
```

**Complexity**

- Time complexity: $O(m * (n + N))$
- Space complexity: $O(n * m)$

> Where $N$ is the number of words, $m$ is the length of each word, and $n$ is the length of the $target$ string.

## 3. Dynamic Programming (Bottom-Up)

We can convert the memoized solution to a bottom-up DP. We fill a 2D table where `dp[i][k]` represents the number of ways to form `target[i:]` using columns `k` to `m-1`.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;

public:
    int numWays(vector<string>& words, string target) {
        int n = target.size(), m = words[0].size();

        vector<vector<int>> cnt(m, vector<int>(26, 0));
        for (const string& word : words) {
            for (int i = 0; i < word.size(); i++) {
                cnt[i][word[i] - 'a']++;
            }
        }

        vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
        dp[n][m] = 1;

        for (int i = n; i >= 0; i--) {
            for (int k = m - 1; k >= 0; k--) {
                dp[i][k] = dp[i][k + 1];
                if (i < n) {
                    int c = target[i] - 'a';
                    dp[i][k] = (dp[i][k] + (long long) cnt[k][c] * dp[i + 1][k + 1]) % MOD;
                }
            }
        }

        return dp[0][0];
    }
};
```

**Complexity**

- Time complexity: $O(m * (n + N))$
- Space complexity: $O(n * m)$

> Where $N$ is the number of words, $m$ is the length of each word, and $n$ is the length of the $target$ string.

## 4. Dynamic Programming (Space Optimized)

Since we only need the previous row of the DP table to compute the current row, we can reduce space by using a single 1D array.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;

public:
    int numWays(vector<string>& words, string target) {
        int n = target.size(), m = words[0].size();

        vector<vector<int>> cnt(m, vector<int>(26, 0));
        for (const string& word : words) {
            for (int i = 0; i < word.size(); i++) {
                cnt[i][word[i] - 'a']++;
            }
        }

        vector<int> dp(m + 1);
        dp[m] = 1;

        for (int i = n; i >= 0; i--) {
            int nxt = i == n - 1 ? 1 : 0;
            for (int k = m - 1; k >= 0; k--) {
                int cur = dp[k];
                dp[k] = dp[k + 1];
                if (i < n) {
                    int c = target[i] - 'a';
                    dp[k] = (dp[k] + (long long) cnt[k][c] * nxt) % MOD;
                }
                nxt = cur;
            }
            dp[m] = 0;
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(m * (n + N))$
- Space complexity: $O(m)$

> Where $N$ is the number of words, $m$ is the length of each word, and $n$ is the length of the $target$ string.
