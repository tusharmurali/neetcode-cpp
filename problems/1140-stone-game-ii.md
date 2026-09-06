# 1140. Stone Game II

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/stone-game-ii/>  
- **NeetCode:** <https://neetcode.io/problems/stone-game-ii>  
- **Video:** <https://www.youtube.com/watch?v=I-z-u0zfQtg>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

This is a two-player game where Alice and Bob take turns picking piles from the front. The key insight is that both players play optimally, meaning Alice tries to maximize her score while Bob tries to minimize Alice's score. We can model this using recursion with memoization, tracking whose turn it is, the current index, and the value of `M`. When it's Alice's turn, she picks the option that maximizes her total; when it's Bob's turn, he picks the option that minimizes Alice's total.

```cpp
class Solution {
private:
    vector<vector<vector<int>>> dp;

public:
    int stoneGameII(vector<int>& piles) {
        int n = piles.size();
        dp.resize(2, vector<vector<int>>(n, vector<int>(n + 1, -1)));
        return dfs(1, 0, 1, piles);
    }

private:
    int dfs(int alice, int i, int M, vector<int>& piles) {
        if (i == piles.size()) return 0;
        if (dp[alice][i][M] != -1) return dp[alice][i][M];

        int res = alice == 1 ? 0 : INT_MAX;
        int total = 0;

        for (int X = 1; X <= 2 * M; X++) {
            if (i + X > piles.size()) break;
            total += piles[i + X - 1];
            if (alice == 1) {
                res = max(res, total + dfs(0, i + X, max(M, X), piles));
            } else {
                res = min(res, dfs(1, i + X, max(M, X), piles));
            }
        }

        dp[alice][i][M] = res;
        return dp[alice][i][M];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(n ^ 2)$

## 2. Dynamic Programming (Top-Down) + Suffix Sum

Instead of tracking both players separately, we can simplify by focusing on a single player's perspective. At each position, the current player wants to maximize their own score. The trick is that whatever stones remain after the current player's turn will be split optimally by the opponent. Using suffix sums, if the current player takes some stones, their score equals those stones plus whatever remains minus the opponent's optimal result from the remaining position.

```cpp
class Solution {
private:
    vector<vector<int>> dp;
    vector<int> suffixSum;

public:
    int stoneGameII(vector<int>& piles) {
        int n = piles.size();
        dp.resize(n, vector<int>(n + 1, -1));

        suffixSum.resize(n);
        suffixSum[n - 1] = piles[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            suffixSum[i] = piles[i] + suffixSum[i + 1];
        }

        return dfs(0, 1, piles);
    }

private:
    int dfs(int i, int M, vector<int>& piles) {
        if (i == suffixSum.size()) return 0;
        if (dp[i][M] != -1) return dp[i][M];

        int res = 0;
        for (int X = 1; X <= 2 * M; X++) {
            if (i + X > suffixSum.size()) break;
            res = max(res, suffixSum[i] - dfs(i + X, max(M, X), piles));
        }

        return dp[i][M] = res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(n ^ 2)$

## 3. Dynamic Programming (Bottom-Up)

We can convert the top-down approach to bottom-up by filling the DP table from the end of the piles array backward. At each position, we compute the optimal result for both Alice and Bob, considering all possible moves. Working backward ensures that when we compute a state, all states it depends on have already been computed.

```cpp
class Solution {
public:
    int stoneGameII(vector<int>& piles) {
        int n = piles.size();
        vector<vector<vector<int>>> dp(2, vector<vector<int>>(n + 1, vector<int>(n + 1, 0)));

        for (int i = n - 1; i >= 0; i--) {
            for (int M = 1; M <= n; M++) {
                int total = 0;
                dp[1][i][M] = 0;
                dp[0][i][M] = INT_MAX;

                for (int X = 1; X <= 2 * M; X++) {
                    if (i + X > n) break;
                    total += piles[i + X - 1];

                    dp[1][i][M] = max(dp[1][i][M], total + dp[0][i + X][max(M, X)]);
                    dp[0][i][M] = min(dp[0][i][M], dp[1][i + X][max(M, X)]);
                }
            }
        }

        return dp[1][0][1];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(n ^ 2)$

## 4. Dynamic Programming (Bottom-Up) + Suffix Sum

Combining the bottom-up approach with the suffix sum optimization gives us a cleaner solution. Since we treat both players symmetrically (each maximizes their own score), we only need a 2D DP table. The suffix sum lets us compute how many stones the current player gets by subtracting the opponent's optimal result from the remaining total.

```cpp
class Solution {
public:
    int stoneGameII(vector<int>& piles) {
        int n = piles.size();

        vector<int> suffixSum(n, 0);
        suffixSum[n - 1] = piles[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            suffixSum[i] = piles[i] + suffixSum[i + 1];
        }

        vector<vector<int>> dp(n + 1, vector<int>(n + 1, 0));

        for (int i = n - 1; i >= 0; i--) {
            for (int M = 1; M <= n; M++) {
                for (int X = 1; X <= 2 * M; X++) {
                    if (i + X > n) break;
                    dp[i][M] = max(dp[i][M], suffixSum[i] - dp[i + X][max(M, X)]);
                }
            }
        }

        return dp[0][1];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(n ^ 2)$
