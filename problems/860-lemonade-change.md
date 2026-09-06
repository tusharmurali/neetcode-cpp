# 860. Lemonade Change

- **Difficulty:** Easy  
- **Pattern:** Greedy  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/lemonade-change/>  
- **NeetCode:** <https://neetcode.io/problems/lemonade-change>  
- **Video:** <https://www.youtube.com/watch?v=mSVAw0AUZgA>  

[← Back to index](../INDEX.md)

## 1. Iteration - I

Each lemonade costs `$5`, so we need to give back the difference when customers pay with `$10` or `$20` bills. The key observation is that `$5` bills are more versatile than `$10` bills since they can be used for both `$5` and `$15` change. When giving `$15` change, we should prefer using one `$10` and one `$5` rather than three `$5`s to preserve our flexibility for future transactions.

```cpp
class Solution {
public:
    bool lemonadeChange(vector<int>& bills) {
        int five = 0, ten = 0;
        for (int b : bills) {
            if (b == 5) {
                five++;
            } else if (b == 10) {
                ten++;
                if (five > 0) {
                    five--;
                } else {
                    return false;
                }
            } else {
                if (five > 0 && ten > 0) {
                    five--;
                    ten--;
                } else if (five >= 3) {
                    five -= 3;
                } else {
                    return false;
                }
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 2. Iteration - II

This is a cleaner version of the same greedy approach. Instead of checking conditions before decrementing, we optimistically make the change and then verify if the `$5` count went negative. This simplifies the code by deferring the validity check to a single condition after each transaction.

```cpp
class Solution {
public:
    bool lemonadeChange(vector<int>& bills) {
        int five = 0, ten = 0;
        for (int b : bills) {
            if (b == 5) {
                five++;
            } else if (b == 10) {
                five--;
                ten++;
            } else if (ten > 0) {
                five--;
                ten--;
            } else {
                five -= 3;
            }
            if (five < 0) {
                return false;
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
