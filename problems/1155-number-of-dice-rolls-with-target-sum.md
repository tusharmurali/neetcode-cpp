# 1155. Number of Dice Rolls with Target Sum

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-dice-rolls-with-target-sum/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-dice-rolls-with-target-sum>  
- **Video:** <https://www.youtube.com/watch?v=hfUxjdjVQN4>  

[← Back to index](../INDEX.md)

## 1. Recursion

This is a counting problem where we need to find all ways to roll `n` dice (each with `k` faces) to get a sum of `target`. For each die, we can roll any value from 1 to `k`, and we need to count how many combinations lead to the `target`. This naturally leads to a recursive approach: for each die roll, we try all possible face values and recursively count the ways to achieve the remaining `target` with the remaining dice.

```cpp
class Solution {
private:
    const int MOD = 1e9 + 7;

public:
    int numRollsToTarget(int n, int k, int target) {
        return count(n, target, k);
    }

private:
    int count(int n, int target, int k) {
        if (n == 0) {
            return target == 0 ? 1 : 0;
        }
        if (target < 0) {
            return 0;
        }

        int res = 0;
        for (int val = 1; val <= k; val++) {
            res = (res + count(n - 1, target - val, k)) % MOD;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(k ^ n)$
- Space complexity: $O(n)$

> Where $n$ is the number of dices, $k$ is the number of faces each dice have, and $t$ is the target value.

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems. For example, reaching `target` 10 with 3 dice might be computed multiple times through different paths. By caching results in a memoization table, we avoid redundant calculations. The state is defined by two variables: the number of dice remaining and the current target sum.

```cpp
class Solution {
private:
    const int MOD = 1e9 + 7;
    vector<vector<int>> dp;

public:
    int numRollsToTarget(int n, int k, int target) {
        dp = vector<vector<int>>(n + 1, vector<int>(target + 1, -1));
        return count(n, target, k);
    }

private:
    int count(int n, int target, int k) {
        if (n == 0) {
            return target == 0 ? 1 : 0;
        }
        if (target < 0) {
            return 0;
        }
        if (dp[n][target] != -1) {
            return dp[n][target];
        }

        int res = 0;
        for (int val = 1; val <= k; val++) {
            if (target - val >= 0) {
                res = (res + count(n - 1, target - val, k)) % MOD;
            }
        }
        dp[n][target] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * t * k)$
- Space complexity: $O(n * t)$

> Where $n$ is the number of dices, $k$ is the number of faces each dice have, and $t$ is the target value.

## 3. Dynamic Programming (Bottom-Up)

Instead of recursion with memoization, we can build the solution iteratively from the ground up. We use a 2D DP table where `dp[i][t]` represents the number of ways to achieve sum `t` using exactly `i` dice. We fill this table by considering each die one at a time and each possible face value.

```cpp
class Solution {
public:
    int numRollsToTarget(int n, int k, int target) {
        const int MOD = 1e9 + 7;
        vector<vector<int>> dp(n + 1, vector<int>(target + 1, 0));
        dp[0][0] = 1;

        for (int i = 1; i <= n; i++) {
            for (int val = 1; val <= k; val++) {
                for (int t = val; t <= target; t++) {
                    dp[i][t] = (dp[i][t] + dp[i - 1][t - val]) % MOD;
                }
            }
        }

        return dp[n][target];
    }
};
```

**Complexity**

- Time complexity: $O(n * t * k)$
- Space complexity: $O(n * t)$

> Where $n$ is the number of dices, $k$ is the number of faces each dice have, and $t$ is the target value.

## 4. Dynamic Programming (Space Optimized)

In the bottom-up approach, we only need the previous row to compute the current row. This observation allows us to reduce space from O(n \* target) to O(target) by using two 1D arrays: one for the current state and one for the next state. After processing each die, we swap the arrays.

```cpp
class Solution {
public:
    int numRollsToTarget(int n, int k, int target) {
        const int MOD = 1e9 + 7;
        vector<int> dp(target + 1, 0);
        dp[0] = 1;

        for (int dice = 0; dice < n; dice++) {
            vector<int> nextDp(target + 1, 0);
            for (int val = 1; val <= k; val++) {
                for (int total = val; total <= target; total++) {
                    nextDp[total] = (nextDp[total] + dp[total - val]) % MOD;
                }
            }
            dp = nextDp;
        }

        return dp[target];
    }
};
```

**Complexity**

- Time complexity: $O(n * t * k)$
- Space complexity: $O(t)$

> Where $n$ is the number of dices, $k$ is the number of faces each dice have, and $t$ is the target value.

## 5. Dynamic Programming (Optimal)

We can use a single array and iterate backwards to avoid overwriting values we still need. By processing sums in reverse order and resetting values before adding new contributions, we achieve the same result with a single array. This approach also skips positions with zero ways, providing a minor optimization.

```cpp
class Solution {
public:
    int numRollsToTarget(int n, int k, int target) {
        const int MOD = 1e9 + 7;
        vector<int> dp(target + 1, 0);
        dp[0] = 1;

        for (int dice = 0; dice < n; dice++) {
            for (int t = target; t >= 0; t--) {
                int ways = dp[t];
                dp[t] = 0;
                if (ways > 0) {
                    for (int val = 1; val <= min(k, target - t); val++) {
                        dp[t + val] = (dp[t + val] + ways) % MOD;
                    }
                }
            }
        }

        return dp[target];
    }
};
```

**Complexity**

- Time complexity: $O(n * t * k)$
- Space complexity: $O(t)$

> Where $n$ is the number of dices, $k$ is the number of faces each dice have, and $t$ is the target value.
