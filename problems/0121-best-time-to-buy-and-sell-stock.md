# 121. Best Time to Buy And Sell Stock

- **Difficulty:** Easy  
- **Pattern:** Sliding Window  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/best-time-to-buy-and-sell-stock/>  
- **NeetCode:** <https://neetcode.io/problems/buy-and-sell-crypto>  
- **Video:** <https://www.youtube.com/watch?v=1pkOgXD63yU>  
- **Video approach:** 3. Dynamic Programming  

[← Back to index](../INDEX.md)

## 1. Brute Force

The brute-force approach checks every possible buy–sell pair.  
For each day, we pretend to buy the stock, and then we look at all the future days to see what the best selling price would be.  
Among all these profits, we keep the highest one.

```cpp
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int res = 0;
        for (int i = 0; i < prices.size(); i++) {
            int buy = prices[i];
            for (int j = i + 1; j < prices.size(); j++) {
                int sell = prices[j];
                res = max(res, sell - buy);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Two Pointers

We want to buy at a low price and sell at a higher price that comes **after** it.  
Using two pointers helps us track this efficiently:

- `l` is the **buy day** (looking for the lowest price)
- `r` is the **sell day** (looking for a higher price)

If the price at `r` is higher than at `l`, we can make a profit — so we update the maximum.
If the price at `r` is lower, then `r` becomes the new `l` because a cheaper buying price is always better.

By moving the pointers this way, we scan the list once and always keep the best buying opportunity.

```cpp
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int l = 0, r = 1;
        int maxP = 0;

        while (r < prices.size()) {
            if (prices[l] < prices[r]) {
                int profit = prices[r] - prices[l];
                maxP = max(maxP, profit);
            } else {
                l = r;
            }
            r++;
        }
        return maxP;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 3. Dynamic Programming ▶ video

As we scan through the prices, we keep track of two things:

1. **The lowest price so far** → this is the best day to buy.
2. **The best profit so far** → selling today minus the lowest buy price seen earlier.

At each price, we imagine selling on that day.  
The profit would be:  
`current price – lowest price seen so far`

We then update:

- the maximum profit,
- and the lowest price if we find a cheaper one.

This way, we make the optimal buy–sell decision in one simple pass.

```cpp
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int maxP = 0;
        int minBuy = prices[0];

        for (int& sell : prices) {
            maxP = max(maxP, sell - minBuy);
            minBuy = min(minBuy, sell);
        }
        return maxP;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0121-best-time-to-buy-and-sell-stock.cpp` in the NeetCode repo)

```cpp
/*
    Given array prices, return max profit w/ 1 buy & 1 sell
    Ex. prices = [7,1,5,3,6,4] -> 5 (buy at $1, sell at $6)

    For each, get diff b/w that & min value before, store max

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int maxP = 0, l = 0, r = 0;
        while (r < prices.size()){
            if (prices[r] > prices[l])
                maxP = max(maxP, prices[r] - prices[l]);
            else
                l = r;
            ++r;
        }
        return maxP;
    }
};
```
