# 2370. Longest Ideal Subsequence

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/longest-ideal-subsequence/>  
- **NeetCode:** <https://neetcode.io/problems/longest-ideal-subsequence>  
- **Video:** <https://www.youtube.com/watch?v=gR1E2oLQYSY>  

[← Back to index](../INDEX.md)

## 1. Recursion

An "ideal" subsequence requires that consecutive characters differ by at most `k` in their alphabetical positions. For each character in the string, we have two choices: skip it or include it (if it satisfies the constraint with the previous character). This decision tree naturally maps to a recursive approach where we try both options and take the maximum.

```cpp
class Solution {
public:
    int longestIdealString(string s, int k) {
        return dfs(0, -1, s, k);
    }

private:
    int dfs(int i, int prev, const string &s, int k) {
        if (i == s.size()) {
            return 0;
        }
        int skip = dfs(i + 1, prev, s, k);
        int include = 0;
        if (prev == -1 || abs(s[i] - prev) <= k) {
            include = 1 + dfs(i + 1, s[i], s, k);
        }
        return max(skip, include);
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems since the same `(index, previous character)` pair can be reached through different paths. By caching results in a 2D table indexed by position and the previous character, we avoid redundant computation. Since there are only 26 possible previous characters (plus a "none" state), the state space is manageable.

```cpp
class Solution {
private:
    vector<vector<int>> dp;

public:
    int longestIdealString(string s, int k) {
        dp = vector<vector<int>>(s.size(), vector<int>(27, -1));
        return dfs(0, -1, s, k);
    }

private:
    int dfs(int i, int prev, const string &s, int k) {
        if (i == s.size()) {
            return 0;
        }
        if (dp[i][prev + 1] != -1) {
            return dp[i][prev + 1];
        }
        int skip = dfs(i + 1, prev, s, k);
        int include = 0;
        if (prev == -1 || abs(s[i] - ('a' + prev)) <= k) {
            include = 1 + dfs(i + 1, s[i] - 'a', s, k);
        }
        dp[i][prev + 1] = max(skip, include);
        return max(skip, include);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

We can fill a table iteratively instead of recursively. For each position `i` and each possible "last character" `prev`, we compute the longest ideal subsequence. We propagate values forward: either keep the previous state unchanged (skip current character) or extend it if the current character is within `k` of `prev`.

```cpp
class Solution {
public:
    int longestIdealString(string s, int k) {
        int n = s.size();
        vector<vector<int>> dp(n + 1, vector<int>(26, 0));

        for (int i = 1; i <= n; i++) {
            int curr = s[i - 1] - 'a';
            for (int prev = 0; prev < 26; prev++) {
                dp[i][prev] = max(dp[i][prev], dp[i - 1][prev]);
                if (abs(curr - prev) <= k) {
                    dp[i][curr] = max(dp[i][curr], 1 + dp[i - 1][prev]);
                }
            }
        }

        return *max_element(dp[n].begin(), dp[n].end());
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized)

Since we only need to know the longest subsequence ending at each character, we can use a single array of size 26. For each character in the string, we look at all characters within distance `k` and take the maximum length, then update the entry for the current character. This reduces space from O(n) to O(1) (constant 26 entries).

```cpp
class Solution {
public:
    int longestIdealString(string s, int k) {
        vector<int> dp(26, 0);

        for (char c : s) {
            int curr = c - 'a';
            int longest = 1;
            for (int prev = 0; prev < 26; prev++) {
                if (abs(curr - prev) <= k) {
                    longest = max(longest, 1 + dp[prev]);
                }
            }
            dp[curr] = max(dp[curr], longest);
        }

        return *max_element(dp.begin(), dp.end());
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we have at most 26 different characters.
