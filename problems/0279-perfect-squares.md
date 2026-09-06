# 279. Perfect Squares

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/perfect-squares/>  
- **NeetCode:** <https://neetcode.io/problems/perfect-squares>  
- **Video:** <https://www.youtube.com/watch?v=HLZLwjzIVGo>  

[← Back to index](../INDEX.md)

## 1. Recursion

We want to express `n` as a sum of the fewest perfect squares. At each step, we can subtract any perfect square that fits, then recursively solve for the remainder. By trying all possible perfect squares and taking the minimum, we find the optimal answer. This brute-force approach explores all combinations but results in repeated subproblems.

```cpp
class Solution {
public:
    int numSquares(int n) {
        return dfs(n);
    }

private:
    int dfs(int target) {
        if (target == 0) {
            return 0;
        }

        int res = target;
        for (int i = 1; i * i <= target; i++) {
            res = min(res, 1 + dfs(target - i * i));
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ {\sqrt {n}})$
- Space complexity: $O(n)$ for recursion stack.

## 2. Dynamic Programming (Top-Down)

The recursive solution recomputes the same subproblems many times. By caching results in a memoization table, we avoid redundant work. Each unique target value is solved once, and subsequent calls return the cached result. This transforms the exponential time complexity into polynomial.

```cpp
class Solution {
public:
    unordered_map<int, int> memo;

    int dfs(int target) {
        if (target == 0) return 0;
        if (memo.count(target)) return memo[target];

        int res = target;
        for (int i = 1; i * i <= target; i++) {
            res = min(res, 1 + dfs(target - i * i));
        }

        return memo[target] = res;
    }

    int numSquares(int n) {
        return dfs(n);
    }
};
```

**Complexity**

- Time complexity: $O(n * \sqrt {n})$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

Instead of solving top-down with recursion, we can build the solution bottom-up. We compute the minimum number of squares for every value from `1` to `n`, using previously computed results. For each target, we try subtracting every perfect square and take the minimum result plus one.

```cpp
class Solution {
public:
    int numSquares(int n) {
        vector<int> dp(n + 1, n);
        dp[0] = 0;

        for (int target = 1; target <= n; target++) {
            for (int s = 1; s * s <= target; s++) {
                dp[target] = min(dp[target], 1 + dp[target - s * s]);
            }
        }

        return dp[n];
    }
};
```

**Complexity**

- Time complexity: $O(n * \sqrt {n})$
- Space complexity: $O(n)$

## 4. Breadth First Search

We can view this as a shortest path problem. Starting from `0`, each step adds a perfect square. BFS explores all sums reachable with `1` square, then `2` squares, and so on. The first time we reach `n`, we have found the minimum number of squares. Using a set to track visited values prevents processing the same sum multiple times.

```cpp
class Solution {
public:
    int numSquares(int n) {
        queue<int> q;
        unordered_set<int> seen;

        int res = 0;
        q.push(0);
        while (!q.empty()) {
            res++;
            for (int i = q.size(); i > 0; i--) {
                int cur = q.front(); q.pop();
                for (int s = 1; s * s + cur <= n; s++) {
                    int next = cur + s * s;
                    if (next == n) return res;
                    if (seen.find(next) == seen.end()) {
                        q.push(next);
                        seen.insert(next);
                    }
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * \sqrt {n})$
- Space complexity: $O(n)$

## 5. Math

Lagrange's four square theorem states that every positive integer can be expressed as the sum of at most four perfect squares. Using additional number theory, we can determine the exact answer in constant time. If `n` is a perfect square, the answer is `1`. If `n` can be written as the sum of two squares, the answer is `2`. If `n` is of the form `4^k(8m+7)`, the answer is `4`. Otherwise, the answer is `3`.

```cpp
class Solution {
public:
    int numSquares(int n) {
        while (n % 4 == 0) {
            n /= 4;
        }

        if (n % 8 == 7) {
            return 4;
        }

        if (isSquareNum(n)) {
            return 1;
        }

        for (int i = 1; i * i <= n; i++) {
            if (isSquareNum(n - i * i)) {
                return 2;
            }
        }

        return 3;
    }

private:
    bool isSquareNum(int num) {
        int s = (int) sqrt(num);
        return s * s == num;
    }
};
```

**Complexity**

- Time complexity: $O(\sqrt {n})$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0279-perfect-squares.cpp` in the NeetCode repo)

```cpp
#include <iostream>
#include <vector>
using namespace std;

/*
    problem link: https://leetcode.com/problems/perfect-squares/description/
    Given an integer n, return the least number of perfect square numbers that sum to n.

    A perfect square is an integer that is the square of an integer; in other words, it is the
    product of some integer with itself. For example, 1, 4, 9, and 16 are perfect squares while 3
    and 11 are not.

    Example 1:

    Input: n = 12
    Output: 3
    Explanation: 12 = 4 + 4 + 4.

    Example 2:

    Input: n = 13
    Output: 2
    Explanation: 13 = 4 + 9.
*/

class Solution {
public:
    // Similar to Coin Change problem
    int numSquares(int n) {
        // Create the dp array to eliminate the cache
        vector<int> dp(n + 1);
        // Initialize the firest element of dp as 0
        dp[0] = 0;
        for (int i = 1; i <= n; i++)
        {
            // Biggest is when all square is 1^2 that is when dp[i] = i
            dp[i] = i;
            for (int j = 1; j * j <= i; j++) {
                // Update the value of dp[i]
                dp[i] = min(dp[i], dp[i - j * j] + 1);
            }
        }
        // Return the value of dp[n]
        return dp[n];
    }
};
```
