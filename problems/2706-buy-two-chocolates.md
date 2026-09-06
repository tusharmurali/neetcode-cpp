# 2706. Buy Two Chocolates

- **Difficulty:** Easy  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/buy-two-chocolates/>  
- **NeetCode:** <https://neetcode.io/problems/buy-two-chocolates>  
- **Video:** <https://www.youtube.com/watch?v=BTzNimiQdW4>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We want to buy two chocolates and maximize the leftover money, which means we should minimize the total cost of the two chocolates. The brute force approach tries every possible pair of chocolates and keeps track of the maximum leftover (or equivalently, the pair with minimum total cost that we can afford).

```cpp
class Solution {
public:
    int buyChoco(vector<int>& prices, int money) {
        int res = -1;
        for (int i = 0; i < prices.size(); i++) {
            for (int j = i + 1; j < prices.size(); j++) {
                if (prices[i] + prices[j] <= money) {
                    res = max(res, money - prices[i] - prices[j]);
                }
            }
        }
        return res == -1 ? money : res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 2. Sorting

To maximize leftover money, we need to buy the two cheapest chocolates. After sorting the prices, the two cheapest chocolates will be at the beginning of the array. We just need to check if we can afford them.

```cpp
class Solution {
public:
    int buyChoco(vector<int>& prices, int money) {
        sort(prices.begin(), prices.end());
        int buy = prices[0] + prices[1];
        return buy > money ? money : money - buy;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 3. Greedy

We can find the two cheapest chocolates in a single pass without sorting. As we iterate through the prices, we maintain the two smallest values seen so far. This gives us the optimal pair to buy.

```cpp
class Solution {
public:
    int buyChoco(vector<int>& prices, int money) {
        int min1 = INT_MAX, min2 = INT_MAX;

        for (int p : prices) {
            if (p < min1) {
                min2 = min1;
                min1 = p;
            } else if (p < min2) {
                min2 = p;
            }
        }

        int leftover = money - min1 - min2;
        return leftover >= 0 ? leftover : money;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
