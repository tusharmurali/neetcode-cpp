# 1269. Number of Ways to Stay in the Same Place After Some Steps

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-ways-to-stay-in-the-same-place-after-some-steps/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-ways-to-stay-in-the-same-place-after-some-steps>  
- **Video:** <https://www.youtube.com/watch?v=8YBGXG-8sRI>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

We need to count how many ways we can return to index 0 after exactly `steps` moves, where each move can go left, right, or stay in place. This is a classic decision tree problem where at each step we have three choices.

The key observation is that we can never move further than `steps` positions to the right, since we would need at least that many steps just to return. This lets us bound our search space to `min(steps, arrLen)` positions.

We use memoization to avoid recomputing the same subproblems. The state is defined by the current position `i` and remaining `steps`.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;
    vector<vector<int>> dp;

    int dfs(int i, int steps, int maxPos) {
        if (steps == 0) {
            return i == 0 ? 1 : 0;
        }
        if (dp[i][steps] != -1) {
            return dp[i][steps];
        }

        int res = dfs(i, steps - 1, maxPos);
        if (i > 0) {
            res = (res + dfs(i - 1, steps - 1, maxPos)) % MOD;
        }
        if (i < maxPos - 1) {
            res = (res + dfs(i + 1, steps - 1, maxPos)) % MOD;
        }

        dp[i][steps] = res;
        return res;
    }

public:
    int numWays(int steps, int arrLen) {
        int maxPos = min(steps, arrLen);
        dp.assign(maxPos + 1, vector<int>(steps + 1, -1));
        return dfs(0, steps, maxPos);
    }
};
```

**Complexity**

- Time complexity: $O(n * min(n, m))$
- Space complexity: $O(n * min(n, m))$

> Where $n$ is the number of steps and $m$ is the size of the array.

## 2. Dynamic Programming (Bottom-Up)

Instead of thinking recursively from the end state backward, we can build up the solution iteratively. We start from the base case (0 steps taken, standing at index 0) and compute how many ways there are to be at each position after 1 step, then 2 steps, and so on.

At each step, the number of ways to reach position `i` is the sum of ways to reach `i` from `i-1` (moving right), from `i` (staying), and from `i+1` (moving left) in the previous step.

```cpp
class Solution {
public:
    int numWays(int steps, int arrLen) {
        const int MOD = 1e9 + 7;
        arrLen = min(arrLen, steps);
        vector<vector<int>> dp(steps + 1, vector<int>(arrLen + 1, 0));
        dp[0][0] = 1;

        for (int step = 1; step <= steps; step++) {
            for (int i = 0; i < arrLen; i++) {
                int res = dp[step - 1][i];
                if (i > 0) {
                    res = (res + dp[step - 1][i - 1]) % MOD;
                }
                if (i < arrLen - 1) {
                    res = (res + dp[step - 1][i + 1]) % MOD;
                }
                dp[step][i] = res;
            }
        }

        return dp[steps][0];
    }
};
```

**Complexity**

- Time complexity: $O(n * min(n, m))$
- Space complexity: $O(n * min(n, m))$

> Where $n$ is the number of steps and $m$ is the size of the array.

## 3. Dynamic Programming (Space Optimized)

Looking at the bottom-up solution, we notice that computing the values for step `k` only requires values from step `k-1`. We do not need the entire history of all steps.

This means we can reduce space from O(steps \* positions) to O(positions) by keeping only two arrays: one for the current step and one for the previous step.

```cpp
class Solution {
public:
    int numWays(int steps, int arrLen) {
        const int MOD = 1e9 + 7;
        arrLen = min(steps, arrLen);
        vector<int> dp(arrLen, 0);
        dp[0] = 1;

        for (int step = 0; step < steps; step++) {
            vector<int> nextDp(arrLen, 0);
            for (int i = 0; i < arrLen; i++) {
                nextDp[i] = dp[i];
                if (i > 0) {
                    nextDp[i] = (nextDp[i] + dp[i - 1]) % MOD;
                }
                if (i < arrLen - 1) {
                    nextDp[i] = (nextDp[i] + dp[i + 1]) % MOD;
                }
            }
            dp = nextDp;
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n * min(n, m))$
- Space complexity: $O(min(n, m))$

> Where $n$ is the number of steps and $m$ is the size of the array.

## 4. Dynamic Programming (Optimal)

We can push the space optimization even further. Instead of using two separate arrays, we can update the DP array in place if we are careful about the order of updates.

The trick is to process positions from left to right while keeping track of the previous value before it gets overwritten. This way, when we update `dp[i]`, we still have access to the old `dp[i-1]` (saved in a temporary variable) and the old `dp[i+1]` (not yet updated).

```cpp
class Solution {
public:
    int numWays(int steps, int arrLen) {
        const int MOD = 1e9 + 7;
        arrLen = min(steps, arrLen);
        vector<int> dp(arrLen, 0);
        dp[0] = 1;

        for (int step = 0; step < steps; step++) {
            int prev = 0;
            for (int i = 0; i < arrLen; i++) {
                int cur = dp[i];
                if (i > 0) {
                    dp[i] = (dp[i] + prev) % MOD;
                }
                if (i < arrLen - 1) {
                    dp[i] = (dp[i] + dp[i + 1]) % MOD;
                }
                prev = cur;
            }
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n * min(n, m))$
- Space complexity: $O(min(n, m))$

> Where $n$ is the number of steps and $m$ is the size of the array.
