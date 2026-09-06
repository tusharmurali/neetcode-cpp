# 309. Best Time to Buy And Sell Stock With Cooldown

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/>  
- **NeetCode:** <https://neetcode.io/problems/buy-and-sell-crypto-with-cooldown>  
- **Video:** <https://www.youtube.com/watch?v=I7j0F7AHpb8>  
- **Video approach:** 2. Dynamic Programming (Top-Down)  

[← Back to index](../INDEX.md)

## 1. Recursion

This problem is about deciding the best days to buy and sell a stock to maximize profit, with one important rule: **after selling a stock, you must wait one day before buying again (cooldown)**.

At every day, we have two possible states:

- we are **allowed to buy** (we are not holding a stock)
- we are **allowed to sell** (we are currently holding a stock)

Using recursion, we try **all possible decisions** starting from day `0` and choose the one that gives the maximum profit.
At each step, we either:

- take an action (buy or sell), or
- skip the day (cooldown)

The recursive function represents:
**"What is the maximum profit we can make starting from day `i`, given whether we are allowed to buy or not?"**

```cpp
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        return dfs(0, true, prices);
    }

private:
    int dfs(int i, bool buying, vector<int>& prices) {
        if (i >= prices.size()) {
            return 0;
        }

        int cooldown = dfs(i + 1, buying, prices);
        if (buying) {
            int buy = dfs(i + 1, false, prices) - prices[i];
            return max(buy, cooldown);
        } else {
            int sell = dfs(i + 2, true, prices) + prices[i];
            return max(sell, cooldown);
        }
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down) ▶ video

This problem asks for the maximum profit from buying and selling stocks, with the restriction that **after selling a stock, you must wait one day before buying again (cooldown)**.

The recursive solution tries all possible choices, but it repeats the same calculations many times. To make it efficient, we use **Dynamic Programming (Top-Down)** with memoization.

We define a state using:

- the current day `i`
- whether we are allowed to buy (`buying = true`) or must sell (`buying = false`)

For each state, we store the best profit we can achieve so that we never compute it again.

```cpp
class Solution {
public:
    unordered_map<string, int> dp;

    int maxProfit(vector<int>& prices) {
        return dfs(0, true, prices);
    }

private:
    int dfs(int i, bool buying, vector<int>& prices) {
        if (i >= prices.size()) {
            return 0;
        }

        string key = to_string(i) + "-" + to_string(buying);
        if (dp.find(key) != dp.end()) {
            return dp[key];
        }

        int cooldown = dfs(i + 1, buying, prices);
        if (buying) {
            int buy = dfs(i + 1, false, prices) - prices[i];
            dp[key] = max(buy, cooldown);
        } else {
            int sell = dfs(i + 2, true, prices) + prices[i];
            dp[key] = max(sell, cooldown);
        }

        return dp[key];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

This problem is about maximizing stock trading profit with a **cooldown rule**:  
after selling a stock, you must wait **one full day** before buying again.

Instead of using recursion, we solve this using **bottom-up dynamic programming**, where we build the solution starting from the **last day** and move backward to day `0`.

At every day, we only care about two possible states:

- **buying = true** → we do not own a stock and are allowed to buy
- **buying = false** → we currently own a stock and are allowed to sell

For each day and state, we compute the **maximum profit possible from that point onward** and store it in a table.  
This way, future decisions are already known when we process earlier days.

```cpp
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int n = prices.size();
        vector<vector<int>> dp(n + 1, vector<int>(2, 0));

        for (int i = n - 1; i >= 0; --i) {
            for (int buying = 1; buying >= 0; --buying) {
                if (buying == 1) {
                    int buy = dp[i + 1][0] - prices[i];
                    int cooldown = dp[i + 1][1];
                    dp[i][1] = max(buy, cooldown);
                } else {
                    int sell = (i + 2 < n) ? dp[i + 2][1] + prices[i] : prices[i];
                    int cooldown = dp[i + 1][0];
                    dp[i][0] = max(sell, cooldown);
                }
            }
        }

        return dp[0][1];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized)

This problem follows the same idea as the previous dynamic programming solutions:  
we want to maximize profit while respecting the **cooldown rule** (after selling, we must wait one day before buying again).

In the bottom-up DP approach, we only ever use values from the **next day** and the **day after next**. That means we do not need a full DP table — we can **compress the state** into a few variables.

Instead of storing results for every day, we keep track of:

- the best profit if we are allowed to buy on the next day
- the best profit if we are allowed to sell on the next day
- the best profit if we are allowed to buy two days ahead (needed for cooldown)

By updating these values while iterating backward, we achieve the same result using constant space.

```cpp
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int n = prices.size();
        int dp1_buy = 0, dp1_sell = 0;
        int dp2_buy = 0;

        for (int i = n - 1; i >= 0; --i) {
            int dp_buy = max(dp1_sell - prices[i], dp1_buy);
            int dp_sell = max(dp2_buy + prices[i], dp1_sell);
            dp2_buy = dp1_buy;
            dp1_buy = dp_buy;
            dp1_sell = dp_sell;
        }

        return dp1_buy;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0309-best-time-to-buy-and-sell-stock-with-cooldown.cpp` in the NeetCode repo)

```cpp
/*
    Array of stock prices, find max profit
    After a sell cooldown of 1 day, can't engage in multiple transactions
    Ex. prices = [1,2,3,0,2] -> 3, transactions = [buy,sell,cd,buy,sell]

    DP + state machine: held ---> sold ---> reset ---> held
                             sell      rest       buy

    Time: O(n)
    Space: O(1) -> optimized from O(n) since only need i - 1 prev state
*/

// class Solution {
// public:
//     int maxProfit(vector<int>& prices) {
//         int n = prices.size();
//         vector<int> s0(n, 0);
//         vector<int> s1(n, 0);
//         vector<int> s2(n, 0);
//         s0[0] = 0;
//         s1[0] = -prices[0];
//         s2[0] = INT_MIN;
//         for (int i = 1; i < n; i++) {
//             s0[i] = max(s0[i - 1], s2[i - 1]);
//             s1[i] = max(s1[i - 1], s0[i - 1] - prices[i]);
//             s2[i] = s1[i - 1] + prices[i];
//         }
//         return max(s0[n - 1], s2[n - 1]);
//     }
// };

class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int sold = 0;
        int hold = INT_MIN;
        int rest = 0;
        
        for (int i = 0; i < prices.size(); i++) {
            int prevSold = sold;
            sold = hold + prices[i];
            hold = max(hold, rest - prices[i]);
            rest = max(rest, prevSold);
        }
        
        return max(sold, rest);
    }
};
```
