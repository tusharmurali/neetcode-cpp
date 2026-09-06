# 518. Coin Change II

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/coin-change-ii/>  
- **NeetCode:** <https://neetcode.io/problems/coin-change-ii>  
- **Video:** <https://www.youtube.com/watch?v=Mjy4hd2xgrs>  

[← Back to index](../INDEX.md)

## 1. Recursion

This problem asks us to find the number of different ways to make up a given amount using unlimited coins of given denominations.

At every step, we make a choice for the current coin:

- **skip the coin** and move to the next one
- **use the coin** and reduce the remaining amount

Recursion is a natural fit here because each choice leads to a smaller subproblem.  
The recursive function represents:  
**“How many ways can we form amount `a` using coins starting from index `i`?”**

By sorting the coins and always moving forward in the list, we avoid counting the same combination in different orders.

```cpp
class Solution {
public:
    int change(int amount, vector<int>& coins) {
        sort(coins.begin(), coins.end());
        return dfs(coins, 0, amount);
    }

private:
    int dfs(const vector<int>& coins, int i, int a) {
        if (a == 0) {
            return 1;
        }
        if (i >= coins.size()) {
            return 0;
        }

        int res = 0;
        if (a >= coins[i]) {
            res = dfs(coins, i + 1, a);
            res += dfs(coins, i, a - coins[i]);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ {max(n, \frac{a}{m})})$
- Space complexity: $O(max(n, \frac{a}{m}))$

> Where $n$ is the number of coins, $a$ is the given amount and $m$ is the minimum value among all the coins.

## 2. Dynamic Programming (Top-Down)

This problem is about counting how many **different combinations** of coins can make up a given amount, where each coin can be used **any number of times**.

The pure recursive solution works, but it recomputes the same subproblems again and again. To optimize this, we use **top-down dynamic programming (memoization)**.

Each state is uniquely defined by:

- the current coin index `i`
- the remaining amount `a`

The function answers the question:  
**“How many ways can we form amount `a` using coins starting from index `i`?”**

By storing results for each state, we avoid repeated calculations and greatly improve efficiency.

```cpp
class Solution {
public:
    int change(int amount, vector<int>& coins) {
        sort(coins.begin(), coins.end());
        vector<vector<int>> memo(coins.size() + 1,
                            vector<int>(amount + 1, -1));

        return dfs(0, amount, coins, memo);
    }

    int dfs(int i, int a, vector<int>& coins, vector<vector<int>>& memo) {
        if (a == 0) return 1;
        if (i >= coins.size()) return 0;
        if (memo[i][a] != -1) return memo[i][a];

        int res = 0;
        if (a >= coins[i]) {
            res = dfs(i + 1, a, coins, memo);
            res += dfs(i, a - coins[i], coins, memo);
        }
        memo[i][a] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * a)$
- Space complexity: $O(n * a)$

> Where $n$ is the number of coins and $a$ is the given amount.

## 3. Dynamic Programming (Bottom-Up)

This problem asks for the number of different ways to make up a given amount using unlimited coins, where **order does not matter**.

Instead of using recursion, we can solve this using **bottom-up dynamic programming**, where we build the answer step by step using a table.

The key idea is to define a state that represents:

- how many ways we can form a certain amount
- using coins starting from a particular index

By filling the DP table from the base cases upward, we ensure that all required subproblems are already solved when needed.

```cpp
class Solution {
public:
    int change(int amount, vector<int>& coins) {
        int n = coins.size();
        sort(coins.begin(), coins.end());
        vector<vector<uint>> dp(n + 1, vector<uint>(amount + 1, 0));

        for (int i = 0; i <= n; i++) {
            dp[i][0] = 1;
        }

        for (int i = n - 1; i >= 0; i--) {
            for (int a = 0; a <= amount; a++) {
                if (a >= coins[i]) {
                    dp[i][a] = dp[i + 1][a];
                    dp[i][a] += dp[i][a - coins[i]];
                }
            }
        }

        return dp[0][amount];
    }
};
```

**Complexity**

- Time complexity: $O(n * a)$
- Space complexity: $O(n * a)$

> Where $n$ is the number of coins and $a$ is the given amount.

## 4. Dynamic Programming (Space Optimized)

This problem asks for the number of different combinations of coins that can make up a given amount, where each coin can be used unlimited times and the order of coins does not matter.

In the bottom-up dynamic programming approach, we used a 2D table to store results for each coin index and amount. However, each row only depends on:

- the row below it (skipping the coin)
- the current row itself (using the same coin)

Because of this, we can **optimize the space** and store only one 1D array at a time, updating it carefully to preserve correctness.

```cpp
class Solution {
public:
    int change(int amount, vector<int>& coins) {
        vector<uint> dp(amount + 1, 0);
        dp[0] = 1;
        for (int i = coins.size() - 1; i >= 0; i--) {
            vector<uint> nextDP(amount + 1, 0);
            nextDP[0] = 1;

            for (int a = 1; a <= amount; a++) {
                nextDP[a] = dp[a];
                if (a - coins[i] >= 0) {
                    nextDP[a] += nextDP[a - coins[i]];
                }
            }
            dp = nextDP;
        }
        return dp[amount];
    }
};
```

**Complexity**

- Time complexity: $O(n * a)$
- Space complexity: $O(a)$

> Where $n$ is the number of coins and $a$ is the given amount.

## 5. Dynamic Programming (Optimal)

We need to count how many **different combinations** of coins can make up a given amount, where:

- each coin can be used unlimited times
- the order of coins does **not** matter

From earlier dynamic programming approaches, we observe that for each coin, the number of ways to form an amount only depends on:

- the number of ways to form the same amount without using the coin
- the number of ways to form a smaller amount using the current coin

Because of this, we can use a **single 1D DP array** and update it in place, achieving the most space-efficient solution.

The DP array always represents the number of ways to form each amount using the coins processed so far.

```cpp
class Solution {
public:
    int change(int amount, vector<int>& coins) {
        vector<uint> dp(amount + 1, 0);
        dp[0] = 1;
        for (int i = coins.size() - 1; i >= 0; i--) {
            for (int a = 1; a <= amount; a++) {
                dp[a] = dp[a] + (coins[i] <= a ? dp[a - coins[i]] : 0);
            }
        }
        return dp[amount];
    }
};
```

**Complexity**

- Time complexity: $O(n * a)$
- Space complexity: $O(a)$

> Where $n$ is the number of coins and $a$ is the given amount.

## Standalone solution file (`cpp/0518-coin-change-ii.cpp` in the NeetCode repo)

```cpp
/*
    Given array of coins & an amount, return # of combos that make up this amount
    Ex. amount = 5, coins = [1,2,5] -> 4 (5, 2+2+1, 2+1+1+1, 1+1+1+1+1)

    DFS + memo, 2 choices: either try coin & stay at idx, or don't try & proceed

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    int change(int amount, vector<int>& coins) {
        return dfs(amount, coins, 0, 0);
    }
private:
    // {(index, sum) -> # of combos that make up this amount}
    map<pair<int, int>, int> dp;
    
    int dfs(int amount, vector<int>& coins, int i, int sum) {
        if (sum == amount) {
            return 1;
        }
        if (sum > amount) {
            return 0;
        }
        if (i == coins.size()) {
            return 0;
        }
        if (dp.find({i, sum}) != dp.end()) {
            return dp[{i, sum}];
        }
        
        dp[{i, sum}] = dfs(amount, coins, i, sum + coins[i])
                     + dfs(amount, coins, i + 1, sum);
        
        return dp[{i, sum}];
    }
};
```
