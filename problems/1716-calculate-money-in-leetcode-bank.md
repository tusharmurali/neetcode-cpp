# 1716. Calculate Money in Leetcode Bank

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/calculate-money-in-leetcode-bank/>  
- **NeetCode:** <https://neetcode.io/problems/calculate-money-in-leetcode-bank>  
- **Video:** <https://www.youtube.com/watch?v=tKK7gvPCQfs>  

[← Back to index](../INDEX.md)

## 1. Simulation

The deposit pattern follows a simple rule: each day we deposit one more dollar than the previous day, but every Monday we reset to deposit one more dollar than we did on the previous Monday. We can simulate this process day by day, tracking when each week ends to reset the starting deposit for the new week.

```cpp
class Solution {
public:
    int totalMoney(int n) {
        int day = 0, deposit = 1, res = 0;

        while (day < n) {
            res += deposit;
            deposit++;
            day++;

            if (day % 7 == 0) {
                deposit = 1 + day / 7;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Math

Instead of simulating each day, we can use arithmetic series formulas. Each complete week deposits a fixed sum: week 1 deposits 1+2+3+4+5+6+7=28, week 2 deposits 2+3+4+5+6+7+8=35, and so on. The weekly sums form an arithmetic sequence with common difference 7. For the remaining days after complete weeks, we just add the deposits for those partial days.

```cpp
class Solution {
public:
    int totalMoney(int n) {
        int weeks = n / 7;
        int low = 28;
        int high = 28 + 7 * (weeks - 1);
        int res = weeks * (low + high) / 2;

        int monday = weeks + 1;
        for (int i = 0; i < n % 7; i++) {
            res += i + monday;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 3. Math (Optimal)

We can derive a closed-form formula using the sum of first `k` natural numbers: `SUM(k) = k*(k+1)/2`. Each week's extra contribution above the base week follows a pattern, and the remaining days also follow an arithmetic progression. This eliminates the loop needed for remaining days in the previous approach.

```cpp
class Solution {
public:
    int totalMoney(int n) {
        auto SUM = [](int x) { return (x * (x + 1)) / 2; };

        int weeks = n / 7;
        int res = SUM(weeks - 1) * 7 + weeks * SUM(7);
        res += SUM(n % 7) + weeks * (n % 7);
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$
