# 1866. Number of Ways to Rearrange Sticks With K Sticks Visible

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-ways-to-rearrange-sticks-with-k-sticks-visible/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-ways-to-rearrange-sticks-with-k-sticks-visible>  
- **Video:** <https://www.youtube.com/watch?v=O761YBjGxGA>  

[← Back to index](../INDEX.md)

## 1. Recursion

Consider placing sticks from tallest to shortest. The tallest stick must be visible. For the remaining sticks, we decide where to place each one relative to previously placed sticks. If a stick is placed at the leftmost available position, it becomes visible. Otherwise, it hides behind a taller stick already placed to its left.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;

    int dfs(int N, int K) {
        if (N == K) return 1;
        if (N == 0 || K == 0) return 0;
        return (dfs(N - 1, K - 1) + (long long)(N - 1) * dfs(N - 1, K) % MOD) % MOD;
    }

public:
    int rearrangeSticks(int n, int k) {
        return dfs(n, k);
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems. By caching results in a 2D table, we avoid redundant computation.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;
    vector<vector<int>> dp;

    int dfs(int N, int K) {
        if (N == K) return 1;
        if (N == 0 || K == 0) return 0;
        if (dp[N][K] != -1) return dp[N][K];
        dp[N][K] = (dfs(N - 1, K - 1) + (long long)(N - 1) * dfs(N - 1, K) % MOD) % MOD;
        return dp[N][K];
    }

public:
    int rearrangeSticks(int n, int k) {
        dp = vector<vector<int>>(n + 1, vector<int>(k + 1, -1));
        return dfs(n, k);
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(n * k)$

> Where $n$ represents the total number of sticks, and $k$ denotes the number of sticks that must be visible from the left side.

## 3. Dynamic Programming (Bottom-Up)

We fill the DP table iteratively from smaller subproblems to larger ones. `dp[N][K]` represents the number of ways to arrange `N` sticks with exactly `K` visible.

```cpp
class Solution {
public:
    int rearrangeSticks(int n, int k) {
        const int MOD = 1e9 + 7;
        vector<vector<int>> dp(n + 1, vector<int>(k + 1, 0));
        dp[1][1] = 1;

        for (int N = 2; N <= n; N++) {
            for (int K = 1; K <= k; K++) {
                dp[N][K] = (dp[N - 1][K - 1] + (N - 1) * 1LL * dp[N - 1][K]) % MOD;
            }
        }

        return dp[n][k];
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(n * k)$

> Where $n$ represents the total number of sticks, and $k$ denotes the number of sticks that must be visible from the left side.

## 4. Dynamic Programming (Space Optimized)

Each row only depends on the previous row, so we can use a 1D array and update it carefully to avoid overwriting values we still need.

```cpp
class Solution {
public:
    int rearrangeSticks(int n, int k) {
        const int MOD = 1e9 + 7;
        vector<int> dp(k + 1);
        dp[1] = 1;

        for (int N = 2; N <= n; N++) {
            int prev = 0;
            for (int K = 1; K <= k; K++) {
                int tmp = dp[K];
                dp[K] = (prev + (N - 1) * 1LL * dp[K]) % MOD;
                prev = tmp;
            }
        }

        return dp[k];
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(k)$

> Where $n$ represents the total number of sticks, and $k$ denotes the number of sticks that must be visible from the left side.
