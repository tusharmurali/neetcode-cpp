# 1137. N-th Tribonacci Number

- **Difficulty:** Easy  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/n-th-tribonacci-number/>  
- **NeetCode:** <https://neetcode.io/problems/n-th-tribonacci-number>  
- **Video:** <https://www.youtube.com/watch?v=3lpNp5Ojvrw>  

[← Back to index](../INDEX.md)

## 1. Recursion

The tribonacci sequence is defined similarly to Fibonacci, but instead of summing the previous two numbers, we sum the previous three. The base cases are T(0) = 0, T(1) = 1, and T(2) = 1. For any n >= 3, we compute T(n) = T(n-1) + T(n-2) + T(n-3).

A straightforward recursive approach directly implements this definition. However, this leads to exponential time complexity because we recompute the same subproblems many times. Each call branches into three more calls, creating a tree with many redundant calculations.

```cpp
class Solution {
public:
    int tribonacci(int n) {
        if (n <= 2) {
            return n == 0 ? 0 : 1;
        }
        return tribonacci(n - 1) + tribonacci(n - 2) + tribonacci(n - 3);
    }
};
```

**Complexity**

- Time complexity: $O(3 ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down)

The recursive solution wastes time by recomputing the same values over and over. We can fix this with memoization: store each computed result in a cache. Before computing T(n), check if it already exists in the cache. If so, return the cached value immediately. This transforms our exponential algorithm into a linear one, since each unique subproblem is solved only once.

```cpp
class Solution {
    unordered_map<int, int> dp;

public:
    int tribonacci(int n) {
        if (n <= 2) {
            return n == 0 ? 0 : 1;
        }
        if (dp.count(n)) return dp[n];

        dp[n] = tribonacci(n - 1) + tribonacci(n - 2) + tribonacci(n - 3);
        return dp[n];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

Instead of working backwards from n and relying on recursion, we can build up the solution from the base cases. Start with the known values T(0), T(1), and T(2), then iteratively compute each subsequent value until we reach T(n). This eliminates recursion overhead and makes the computation straightforward.

```cpp
class Solution {
public:
    int tribonacci(int n) {
        if (n <= 2) {
            return n == 0 ? 0 : 1;
        }

        vector<int> dp(n + 1, 0);
        dp[1] = dp[2] = 1;
        for (int i = 3; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2] + dp[i - 3];
        }
        return dp[n];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized)

Notice that to compute T(n), we only need the three most recent values: T(n-1), T(n-2), and T(n-3). We do not need to store the entire history. By keeping just three variables (or a small fixed-size array), we can reduce space complexity from O(n) to O(1).

A clever trick uses an array of size 3 and the modulo operator. At iteration i, we store the new value at index i % 3, which naturally overwrites the oldest value we no longer need.

```cpp
class Solution {
public:
    int tribonacci(int n) {
        int t[] = {0, 1, 1};
        if (n < 3) return t[n];

        for (int i = 3; i <= n; ++i) {
            t[i % 3] = t[0] + t[1] + t[2];
        }
        return t[n % 3];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/1137-n-th-tribonacci-number.cpp` in the NeetCode repo)

```cpp
// Time: O(n)
// Space: O(1)

class Solution {
public:
    int tribonacci(int n) {
        int t[] = {0, 1, 1};
        if (n < 3) {
            return t[n];
        }
        for (int i = 3; i <= n; i++) {
            int sum_t = t[0] + t[1] + t[2];
            t[0] = t[1];
            t[1] = t[2];
            t[2] = sum_t;
        }
        return t[2];
    }
};
```
