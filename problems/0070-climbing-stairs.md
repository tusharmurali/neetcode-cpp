# 70. Climbing Stairs

- **Difficulty:** Easy  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/climbing-stairs/>  
- **NeetCode:** <https://neetcode.io/problems/climbing-stairs>  
- **Video:** <https://www.youtube.com/watch?v=Y0lT9Fck7qI>  
- **Video approach:** 4. Dynamic Programming (Space Optimized)  

[← Back to index](../INDEX.md)

## 1. Recursion

At every step, you have **two choices**:
- climb **1 step**
- climb **2 steps**

So from any step `i`, the number of ways to reach the top is:
- ways from `i + 1`
- plus ways from `i + 2`

This naturally forms a **binary recursion tree** where we try all possible paths.
- If we land **exactly on step `n`**, that path counts as **1 valid way**
- If we cross `n`, it’s an **invalid path**

This is a classic example of **exploring all possibilities** using recursion.

```cpp
class Solution {
public:
    int climbStairs(int n) {
        return dfs(n, 0);
    }

    int dfs(int n, int i) {
        if (i >= n) return i == n;
        return dfs(n, i + 1) + dfs(n, i + 2);
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down)

This is the **optimized version of the recursive solution**.

The key observation is:
- While exploring choices (1 step or 2 steps), the same subproblems repeat many times.
- For example, the number of ways from step `i` is always the same whenever we reach `i`.

So instead of recomputing, we **store the result** the first time we compute it and reuse it later.
This is exactly what **Top-Down Dynamic Programming (Memoization)** does.

We still think recursively, but we avoid redundant work.

```cpp
class Solution {
public:
    vector<int> cache;
    int climbStairs(int n) {
        cache.resize(n, -1);
        return dfs(n, 0);
    }

    int dfs(int n, int i) {
        if (i >= n) return i == n;
        if (cache[i] != -1) return cache[i];
        return cache[i] = dfs(n, i + 1) + dfs(n, i + 2);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

To reach step `i`, you can only come from:
- step `i - 1` (1 step)
- step `i - 2` (2 steps)

So the total ways to reach step `i` is the **sum of ways to reach the previous two steps**.  
This forms a **Fibonacci-like pattern**.

```cpp
class Solution {
public:
    int climbStairs(int n) {
        if (n <= 2) {
            return n;
        }
        vector<int> dp(n + 1);
        dp[1] = 1;
        dp[2] = 2;
        for (int i = 3; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        return dp[n];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized) ▶ video

At any step, the number of ways depends only on the **previous two steps**.  
So instead of storing all values in a DP array, we can just keep **two variables** that represent:
- ways to reach the previous step
- ways to reach the step before that

This is the same Fibonacci idea, but optimized to use constant space.

```cpp
class Solution {
public:
    int climbStairs(int n) {
        int one = 1, two = 1;

        for (int i = 0; i < n - 1; i++) {
            int temp = one;
            one = one + two;
            two = temp;
        }

        return one;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 5. Matrix Exponentiation

The number of ways to climb stairs follows the **Fibonacci sequence**:
- To reach step `n`, you can come from `n-1` or `n-2`
- So, `ways(n) = ways(n-1) + ways(n-2)`

Fibonacci numbers can be computed efficiently using **matrix exponentiation**, which reduces the time from linear to logarithmic.

```cpp
class Solution {
public:
    int climbStairs(int n) {
        if (n == 1) return 1;

        vector<vector<int>> M = {{1, 1}, {1, 0}};
        vector<vector<int>> result = matrixPow(M, n);

        return result[0][0];
    }

private:
    vector<vector<int>> matrixMult(vector<vector<int>>& A, vector<vector<int>>& B) {
        return {{A[0][0] * B[0][0] + A[0][1] * B[1][0],
                 A[0][0] * B[0][1] + A[0][1] * B[1][1]},
                {A[1][0] * B[0][0] + A[1][1] * B[1][0],
                 A[1][0] * B[0][1] + A[1][1] * B[1][1]}};
    }

    vector<vector<int>> matrixPow(vector<vector<int>>& M, int p) {
        vector<vector<int>> result = {{1, 0}, {0, 1}};
        vector<vector<int>> base = M;

        while (p > 0) {
            if (p % 2 == 1) {
                result = matrixMult(result, base);
            }
            base = matrixMult(base, base);
            p /= 2;
        }

        return result;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 6. Math

The number of ways to climb stairs follows the **Fibonacci sequence**.  
There is a **closed-form mathematical formula** (called **Binet’s Formula**) that directly computes the nth Fibonacci number using powers and square roots, without loops or recursion.

This works because Fibonacci numbers can be expressed using two constants derived from the golden ratio.

```cpp
class Solution {
public:
    int climbStairs(int n) {
        double sqrt5 = sqrt(5);
        double phi = (1 + sqrt5) / 2;
        double psi = (1 - sqrt5) / 2;
        n++;
        return round((pow(phi, n) - pow(psi, n)) / sqrt5);
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0070-climbing-stairs.cpp` in the NeetCode repo)

```cpp
/*
    Climbing stairs, either 1 or 2 steps, distinct ways to reach top
    Ex. n = 2 -> 2 (1 + 1, 2), n = 3 -> 3 (1 + 1 + 1, 1 + 2, 2 + 1)

    Recursion w/ memoization -> DP, why DP? Optimal substructure
    Recurrence relation: dp[i] = dp[i - 1] + dp[i - 2]
    Reach ith step in 2 ways: 1) 1 step from i-1, 2) 2 steps from i-2

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int climbStairs(int n) {
        if (n == 1) {
            return 1;
        }
        if (n == 2) {
            return 2;
        }
        
        int first = 1;
        int second = 2;
        
        int result = 0;
        
        for (int i = 2; i < n; i++) {
            result = first + second;
            first = second;
            second = result;
        }
        
        return result;
    }
};
```
