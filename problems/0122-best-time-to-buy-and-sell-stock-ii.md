# 122. Best Time to Buy And Sell Stock II

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/>  
- **NeetCode:** <https://neetcode.io/problems/best-time-to-buy-and-sell-stock-ii>  
- **Video:** <https://www.youtube.com/watch?v=3SJ3pUkPQMc>  
- **Video approach:** 5. Greedy  

[← Back to index](../INDEX.md)

## 1. Recursion

At each day, we have a choice: if we are not holding stock, we can either buy or skip. If we are holding stock, we can either sell or skip. We want to maximize profit by exploring all possible combinations of buy and sell decisions. This naturally leads to a recursive approach where we try both options at each step and return the maximum profit.

```cpp
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        return rec(prices, 0, false);
    }

private:
    int rec(vector<int>& prices, int i, bool bought) {
        if (i == prices.size()) {
            return 0;
        }
        int res = rec(prices, i + 1, bought);
        if (bought) {
            res = max(res, prices[i] + rec(prices, i + 1, false));
        } else {
            res = max(res, -prices[i] + rec(prices, i + 1, true));
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down)

The recursive solution recalculates the same states multiple times. For example, the state (day 3, not holding) might be reached through different paths. By storing computed results in a memoization table, we avoid redundant work. Each unique state (day, holding_status) is computed only once.

```cpp
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int n = prices.size();
        vector<vector<int>> dp(n, vector<int>(2, -1));
        return rec(prices, 0, 0, dp);
    }

private:
    int rec(vector<int>& prices, int i, int bought, vector<vector<int>>& dp) {
        if (i == prices.size()) {
            return 0;
        }
        if (dp[i][bought] != -1) {
            return dp[i][bought];
        }
        int res = rec(prices, i + 1, bought, dp);
        if (bought == 1) {
            res = max(res, prices[i] + rec(prices, i + 1, 0, dp));
        } else {
            res = max(res, -prices[i] + rec(prices, i + 1, 1, dp));
        }
        dp[i][bought] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

Instead of solving recursively from day `0` forward, we can build the solution iteratively from the last day backward. At each day, we compute the maximum profit for both states (holding and not holding stock) using the already-computed values for the next day. This eliminates recursion overhead.

```cpp
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int n = prices.size();
        vector<vector<int>> dp(n + 1, vector<int>(2, 0));

        for (int i = n - 1; i >= 0; i--) {
            dp[i][0] = max(dp[i + 1][0], -prices[i] + dp[i + 1][1]);
            dp[i][1] = max(dp[i + 1][1], prices[i] + dp[i + 1][0]);
        }

        return dp[0][0];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized)

Looking at the bottom-up solution, we notice that to compute the values for day `i`, we only need the values from day `i+1`. We do not need the entire `dp` array. This means we can reduce space from O(n) to O(1) by using just four variables to track the current and next day's states.

```cpp
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int nextBuy = 0, nextSell = 0;
        int curBuy = 0, curSell = 0;

        for (int i = prices.size() - 1; i >= 0; i--) {
            curBuy = max(nextBuy, -prices[i] + nextSell);
            curSell = max(nextSell, prices[i] + nextBuy);
            nextBuy = curBuy;
            nextSell = curSell;
        }

        return curBuy;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 5. Greedy ▶ video

The key insight is that we can capture every upward price movement. If the price goes up from day `i` to day `i+1`, we can always "buy" on day `i` and "sell" on day `i+1` to capture that profit. We do not need to track actual transactions because consecutive gains are equivalent to holding through multiple days. For example, buying at 1, holding through 3, 5, and selling at 6 gives the same profit as buying at 1, selling at 3, buying at 3, selling at 5, buying at 5, and selling at 6.

```cpp
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int profit = 0;
        for (int i = 1; i < prices.size(); i++) {
            if (prices[i] > prices[i - 1]) {
                profit += (prices[i] - prices[i - 1]);
            }
        }
        return profit;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0122-best-time-to-buy-and-sell-stock-ii.cpp` in the NeetCode repo)

```cpp
 /*
    Approach: 
    If stock price is going up tomorrow just buy it today and sell it tomorrow.
    
    Time complexity : O(n)
    Space complexity: O(1)

    n is number of days.
*/

class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int ans =0;
        
        // look into the next day and if you are making profit just buy it today.
        for(int i =1;i<prices.size();i++){
            if(prices[i]>prices[i-1]) ans += (prices[i]-prices[i-1]);
        }
        return ans;
    }
};
```
