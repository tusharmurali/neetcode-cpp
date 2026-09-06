# 322. Coin Change

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/coin-change/>  
- **NeetCode:** <https://neetcode.io/problems/coin-change>  
- **Video:** <https://www.youtube.com/watch?v=H9bfqozjoqs>  
- **Video approach:** 3. Dynamic Programming (Bottom-Up)  

[← Back to index](../INDEX.md)

## 1. Recursion

This is the **pure recursive brute-force approach**.

For a given `amount`, we try **every coin**:

- Pick one coin
- Solve the remaining subproblem `amount - coin`
- Take the minimum coins needed among all choices

We explore **all possible combinations**, which leads to many repeated subproblems and exponential time — this solution is correct but inefficient.

If no combination reaches exactly `0`, we treat it as invalid using a very large number.

```cpp
class Solution {
public:
    int dfs(vector<int>& coins, int amount) {
        if (amount == 0) return 0;

        int res = 1e9;
        for (int coin : coins) {
            if (amount - coin >= 0) {
                res = min(res,
                      1 + dfs(coins, amount - coin));
            }
        }
        return res;
    }

    int coinChange(vector<int>& coins, int amount) {
        int minCoins = dfs(coins, amount);
        return (minCoins >= 1e9) ? -1 : minCoins;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ t)$
- Space complexity: $O(t)$

> Where $n$ is the length of the array $coins$ and $t$ is the given $amount$.

## 2. Dynamic Programming (Top-Down)

This is the **optimized version of the brute-force recursion** using **memoization**.

The key observation is that the same `amount` gets solved **multiple times** in recursion.  
So instead of recomputing it, we **store the result** the first time and reuse it.

Each `amount` represents a subproblem:

> _Minimum coins needed to make this amount_

```cpp
class Solution {
public:
    unordered_map<int, int> memo;
    int dfs(int amount, vector<int>& coins) {
        if (amount == 0) return 0;
        if (memo.find(amount) != memo.end())
            return memo[amount];

        int res = INT_MAX;
        for (int coin : coins) {
            if (amount - coin >= 0) {
                int result = dfs(amount - coin, coins);
                if (result != INT_MAX) {
                    res = min(res, 1 + result);
                }
            }
        }

        memo[amount] = res;
        return res;
    }

    int coinChange(vector<int>& coins, int amount) {
        int minCoins = dfs(amount, coins);
        return minCoins == INT_MAX ? -1 : minCoins;
    }
};
```

**Complexity**

- Time complexity: $O(n * t)$
- Space complexity: $O(t)$

> Where $n$ is the length of the array $coins$ and $t$ is the given $amount$.

## 3. Dynamic Programming (Bottom-Up) ▶ video

This is the **bottom-up DP version** of Coin Change.

Instead of asking _“how many coins to make this amount?”_ recursively, we **build answers from smaller amounts to larger ones**.

Key idea:

- If we know the minimum coins to make `a - coin`,
- then we can make `a` using **1 extra coin**.

So each amount depends on **previously solved smaller amounts**.

```cpp
class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        vector<int> dp(amount + 1, amount + 1);
        dp[0] = 0;
        for (int i = 1; i <= amount; i++) {
            for (int j = 0; j < coins.size(); j++) {
                if (coins[j] <= i) {
                    dp[i] = min(dp[i], dp[i - coins[j]] + 1);
                }
            }
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }
};
```

**Complexity**

- Time complexity: $O(n * t)$
- Space complexity: $O(t)$

> Where $n$ is the length of the array $coins$ and $t$ is the given $amount$.

## 4. Breadth First Search

Think of each **amount** as a node in a graph.

- From a current amount `x`, you can go to `x + coin` for every coin.
- Each edge represents **using one coin**.
- We want the **minimum number of coins**, which means the **shortest path** from `0` to `amount`.

This makes the problem a **shortest path in an unweighted graph**, so **Breadth First Search (BFS)** is a natural fit.

BFS explores level by level:

- Level 1 → amounts reachable using 1 coin
- Level 2 → amounts reachable using 2 coins
- First time we reach `amount`, we've used the minimum coins.

```cpp
class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        if (amount == 0) return 0;

        queue<int> q;
        q.push(0);
        vector<bool> seen(amount + 1, false);
        seen[0] = true;
        int res = 0;

        while (!q.empty()) {
            res++;
            int size = q.size();
            for (int i = 0; i < size; i++) {
                int cur = q.front();
                q.pop();
                for (int coin : coins) {
                    int nxt = cur + coin;
                    if (nxt == amount) return res;
                    if (nxt > amount || seen[nxt]) continue;
                    seen[nxt] = true;
                    q.push(nxt);
                }
            }
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n * t)$
- Space complexity: $O(t)$

> Where $n$ is the length of the array $coins$ and $t$ is the given $amount$.

## Standalone solution file (`cpp/0322-coin-change.cpp` in the NeetCode repo)

```cpp
/*
    Given array of coins & an amount, return fewest coins to make that amount
    Ex. coins = [1,2,5], amount = 11 -> 3, $11 = $5 + $5 + $1

    Compute all min counts for amounts up to i, "simulate" use of a coin

    Time: O(m x n) -> m = # of coins, n = amount
    Space: O(n)
*/

class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        vector<int> dp(amount + 1, amount + 1);
        dp[0] = 0;
        
        for (int i = 1; i < amount + 1; i++) {
            for (int j = 0; j < coins.size(); j++) {
                if (i - coins[j] >= 0) {
                    dp[i] = min(dp[i], 1 + dp[i - coins[j]]);
                }
            }
        }
        
        if (dp[amount] == amount + 1) {
            return -1;
        }
        return dp[amount];
    }
};
```
