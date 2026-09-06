# 343. Integer Break

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/integer-break/>  
- **NeetCode:** <https://neetcode.io/problems/integer-break>  
- **Video:** <https://www.youtube.com/watch?v=in6QbUPMJ3I>  

[← Back to index](../INDEX.md)

## 1. Recursion (Brute Force)

To maximize the product, we can try all possible ways to split the integer. For each number, we consider breaking it into two parts and recursively computing the best product for each part. The key insight is that a subpart can either be broken further or kept as is, except for the original number which must be broken at least once.

```cpp
class Solution {
public:
    int integerBreak(int n) {
        return dfs(n, n);
    }

private:
    int dfs(int num, int original) {
        if (num == 1) return 1;

        int res = (num == original) ? 0 : num;
        for (int i = 1; i < num; i++) {
            int val = dfs(i, original) * dfs(num - i, original);
            res = max(res, val);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Recursion

Instead of trying all pairs of splits, we can think of this as a bounded knapsack problem where we repeatedly subtract values from the number. We pick a value `i` (from 1 to n-1) and multiply it with the optimal product of the remaining. By allowing repeated use of the same value, we explore all combinations more efficiently.

```cpp
class Solution {
public:
    int integerBreak(int n) {
        return dfs(n, n - 1);
    }

private:
    int dfs(int num, int i) {
        if (min(num, i) == 0) {
            return 1;
        }

        if (i > num) {
            return dfs(num, num);
        }

        return max(i * dfs(num - i, i), dfs(num, i - 1));
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$ for recursion stack.

## 3. Dynamic Programming (Top-Down) - I

The brute force recursion recalculates the same subproblems many times. By storing the results in a memoization table, we avoid redundant work. Each unique value of `num` is computed only once, then reused.

```cpp
class Solution {
    unordered_map<int, int> dp;

public:
    int integerBreak(int n) {
        dp[1] = 1;
        return dfs(n, n);
    }

private:
    int dfs(int num, int n) {
        if (dp.find(num) != dp.end()) {
            return dp[num];
        }

        int res = (num == n) ? 0 : num;
        for (int i = 1; i < num; i++) {
            int val = dfs(i, n) * dfs(num - i, n);
            res = max(res, val);
        }

        dp[num] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Top-Down) - II

This memoizes the bounded knapsack formulation. We cache results based on both the remaining sum and the current maximum factor being considered. This avoids recomputing identical states across different recursion paths.

```cpp
class Solution {
    vector<vector<int>> dp;

public:
    int integerBreak(int n) {
        dp.assign(n + 1, vector<int>(n, -1));
        return dfs(n, n - 1);
    }

private:
    int dfs(int num, int i) {
        if (min(num, i) == 0) {
            return 1;
        }
        if (dp[num][i] != -1) {
            return dp[num][i];
        }
        if (i > num) {
            dp[num][i] = dfs(num, num);
            return dp[num][i];
        }
        dp[num][i] = max(i * dfs(num - i, i), dfs(num, i - 1));
        return dp[num][i];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 5. Dynamic Programming (Bottom-Up)

We can solve this iteratively by building up solutions from smaller numbers. For each number from 2 to n, we compute the best product by trying all ways to split it and combining previously computed results.

```cpp
class Solution {
public:
    int integerBreak(int n) {
        vector<int> dp(n + 1, 0);
        dp[1] = 1;

        for (int num = 2; num <= n; num++) {
            dp[num] = (num == n) ? 0 : num;
            for (int i = 1; i < num; i++) {
                dp[num] = max(dp[num], dp[i] * dp[num - i]);
            }
        }

        return dp[n];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 6. Math

A mathematical analysis reveals that the optimal strategy is to break the number into as many 3s as possible. This is because 3 maximizes the product per unit. We avoid leaving a remainder of 1 since `3 + 1 = 4` and `2 * 2 > 3 * 1`. For small values (`n <= 3`), we handle them as special cases.

```cpp
class Solution {
public:
    int integerBreak(int n) {
        if (n <= 3) return n - 1;

        int res = 1;
        while (n > 4) {
            res *= 3;
            n -= 3;
        }
        return res * n;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 7. Math (Optimal)

We can compute the result directly using the count of 3s. If `n % 3 == 0`, the answer is `3^(n/3)`. If `n % 3 == 1`, we should use one fewer 3 and multiply by `4` instead (since `2 * 2 > 3 * 1`). If `n % 3 == 2`, we multiply the power of 3 by `2`.

```cpp
class Solution {
public:
    int integerBreak(int n) {
        if (n <= 3) {
            return n - 1;
        }

        int res = pow(3, n / 3);
        if (n % 3 == 1) {
            return (res / 3) * 4;
        }

        return res * max(1, n % 3);
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0343-integer-break.cpp` in the NeetCode repo)

```cpp
/*
Given an integer n, break it into the sum of k positive integers, where k >= 2, and maximize the product of those integers.
Return the maximum product that we can get.

Example. For n = 10, we can break it as 10 = 3 + 3 + 4. Product of these integers is 3 x 3 x 4 = 36, which is the maximum product that
	 we can get in this case. So we return 36 as the answer. 


Time: O(n^2)
Space: O(n)

*/

class Solution {
public:
    int integerBreak(int n) {
        vector<int> dp(n+1, INT_MIN);
        dp[0] = 1, dp[1] = 1;
        for(int ind=2; ind<=n; ind++) {
            for(int i=ind-1; i>=1; i--) {
                dp[ind] = max(dp[ind], i * dp[ind - i]);
            }
            if(ind < n) dp[ind] = max(dp[ind], ind);
        }
        return dp[n];
    }
};
```
