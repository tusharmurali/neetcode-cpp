# 879. Profitable Schemes

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/profitable-schemes/>  
- **NeetCode:** <https://neetcode.io/problems/profitable-schemes>  
- **Video:** <https://www.youtube.com/watch?v=CcLKQLKvOl8>  

[← Back to index](../INDEX.md)

## 1. Recursion

This is a variation of the 0/1 knapsack problem with two constraints: number of members and minimum profit. For each crime, we decide whether to include it or skip it. If we include a crime, we use its required members and gain its profit. At the end, we count paths where total profit meets the threshold and total members used does not exceed the limit.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;

public:
    int profitableSchemes(int n, int minProfit, vector<int>& group, vector<int>& profit) {
        return dfs(0, n, 0, group, profit, minProfit);
    }

private:
    int dfs(int i, int n, int p, const vector<int>& group, const vector<int>& profit, int minProfit) {
        if (i == group.size()) {
            return p >= minProfit ? 1 : 0;
        }

        int res = dfs(i + 1, n, p, group, profit, minProfit);
        if (n - group[i] >= 0) {
            res = (res + dfs(i + 1, n - group[i], p + profit[i], group, profit, minProfit)) % MOD;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ N)$
- Space complexity: $O(N)$

> Where $N$ is the size of the $group$ array.

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems because the same state (crime index, remaining members, current profit) can be reached through different paths. By memoizing results, we avoid redundant computation. We also cap profit at `minProfit` since any profit beyond the threshold is equivalent for counting purposes.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;
    vector<vector<vector<int>>> dp;

public:
    int profitableSchemes(int n, int minProfit, vector<int>& group, vector<int>& profit) {
        dp = vector<vector<vector<int>>>(group.size(), vector<vector<int>>(n + 1, vector<int>(minProfit + 1, -1)));
        return dfs(0, n, 0, group, profit, minProfit);
    }

private:
    int dfs(int i, int n, int p, vector<int>& group, vector<int>& profit, int minProfit) {
        if (i == group.size()) {
            return p >= minProfit ? 1 : 0;
        }
        if (dp[i][n][p] != -1) {
            return dp[i][n][p];
        }

        int res = dfs(i + 1, n, p, group, profit, minProfit);
        if (n >= group[i]) {
            int nxtP = min(p + profit[i], minProfit);
            res = (res + dfs(i + 1, n - group[i], nxtP, group, profit, minProfit)) % MOD;
        }

        dp[i][n][p] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(N * m * n)$
- Space complexity: $O(N * m * n)$

> Where $N$ is the size of the $group$ array, $m$ is the given minimum profit, and $n$ is the number of group members.

## 3. Dynamic Programming (Bottom-Up)

We can convert the top-down solution to bottom-up by iterating through crimes in reverse order. We build up the answer by considering what happens if we include or exclude each crime, starting from the last crime and working backward to the first.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;

public:
    int profitableSchemes(int n, int minProfit, vector<int>& group, vector<int>& profit) {
        int N = group.size();
        vector<vector<vector<int>>> dp(N + 1, vector<vector<int>>(n + 2, vector<int>(minProfit + 1, 0)));

        for (int j = 0; j <= n; j++) {
            dp[N][j][minProfit] = 1;
        }

        for (int i = N - 1; i >= 0; i--) {
            for (int j = 0; j <= n; j++) {
                for (int p = 0; p <= minProfit; p++) {
                    int res = dp[i + 1][j][p];
                    if (j >= group[i]) {
                        int nxtP = min(profit[i] + p, minProfit);
                        res = (res + dp[i + 1][j - group[i]][nxtP]) % MOD;
                    }
                    dp[i][j][p] = res;
                }
            }
        }

        return dp[0][n][0];
    }
};
```

**Complexity**

- Time complexity: $O(N * m * n)$
- Space complexity: $O(N * m * n)$

> Where $N$ is the size of the $group$ array, $m$ is the given minimum profit, and $n$ is the number of group members.

## 4. Dynamic Programming (Space Optimized)

Since each crime's DP state only depends on the next crime's state, we can reduce the 3D table to 2D. We iterate through crimes and update the table in-place. By processing member counts in reverse order, we ensure we use the previous iteration's values before overwriting them.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;

public:
    int profitableSchemes(int n, int minProfit, vector<int>& group, vector<int>& profit) {
        int N = group.size();
        vector<vector<int>> dp(n + 2, vector<int>(minProfit + 1, 0));

        for (int j = 0; j <= n; j++) {
            dp[j][minProfit] = 1;
        }

        for (int i = N - 1; i >= 0; i--) {
            for (int j = n; j >= 0; j--) {
                for (int p = 0; p <= minProfit; p++) {
                    int res = dp[j][p];
                    if (j >= group[i]) {
                        int nxtP = min(profit[i] + p, minProfit);
                        res = (res + dp[j - group[i]][nxtP]) % MOD;
                    }
                    dp[j][p] = res;
                }
            }
        }

        return dp[n][0];
    }
};
```

**Complexity**

- Time complexity: $O(N * m * n)$
- Space complexity: $O(m * n)$

> Where $N$ is the size of the $group$ array, $m$ is the given minimum profit, and $n$ is the number of group members.
