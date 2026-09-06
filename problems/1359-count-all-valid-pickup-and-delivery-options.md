# 1359. Count all Valid Pickup and Delivery Options

- **Difficulty:** Hard  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/count-all-valid-pickup-and-delivery-options/>  
- **NeetCode:** <https://neetcode.io/problems/count-all-valid-pickup-and-delivery-options>  
- **Video:** <https://www.youtube.com/watch?v=OpgslsirW8s>  

[← Back to index](../INDEX.md)

## 1. Recursion

We need to count all valid orderings where each delivery happens after its corresponding pickup. At any point, we can either pick up a new order (if any remain) or deliver an order that has already been picked up. The number of choices at each step depends on how many orders are still available for pickup and how many are picked but not yet delivered.

```cpp
class Solution {
public:
    static const int MOD = 1'000'000'007;

    int countOrders(int n) {
        return dfs(0, 0, n);
    }

private:
    int dfs(int picked, int delivered, int n) {
        if (picked == n && delivered == n) {
            return 1;
        }

        int res = 0;
        if (picked < n) {
            res = (res + (n - picked) * 1LL * dfs(picked + 1, delivered, n)) % MOD;
        }
        if (delivered < picked) {
            res = (res + (picked - delivered) * 1LL * dfs(picked, delivered + 1, n)) % MOD;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Dynamic Programming (Top-Down)

The recursive solution recalculates the same states multiple times. For example, the state `(picked=2, delivered=1)` might be reached through different orderings. By caching these results, we avoid redundant computation.

```cpp
class Solution {
public:
    static const int MOD = 1'000'000'007;
    vector<vector<int>> dp;

    int countOrders(int n) {
        dp.assign(n + 1, vector<int>(n + 1, -1));
        dp[n][n] = 1;
        return dfs(0, 0, n);
    }

private:
    int dfs(int picked, int delivered, int n) {
        if (dp[picked][delivered] != -1) {
            return dp[picked][delivered];
        }

        int res = 0;
        if (picked < n) {
            res = (res + (n - picked) * 1LL * dfs(picked + 1, delivered, n)) % MOD;
        }
        if (delivered < picked) {
            res = (res + (picked - delivered) * 1LL * dfs(picked, delivered + 1, n)) % MOD;
        }

        return dp[picked][delivered] = res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Dynamic Programming (Bottom-Up)

Instead of recursing from `(0, 0)` and memoizing, we can build the solution iteratively. We start from the base case where no orders are processed and accumulate the number of ways to reach each state by considering all valid transitions.

```cpp
class Solution {
public:
    int countOrders(int n) {
        const int MOD = 1'000'000'007;
        vector<vector<int>> dp(n + 1, vector<int>(n + 1, 0));
        dp[0][0] = 1;

        for (int picked = 0; picked <= n; picked++) {
            for (int delivered = 0; delivered <= n; delivered++) {
                if (picked < n) {
                    dp[picked + 1][delivered] = (dp[picked + 1][delivered] +
                                                (n - picked) * 1LL * dp[picked][delivered]) % MOD;
                }
                if (delivered < picked) {
                    dp[picked][delivered + 1] = (dp[picked][delivered + 1] +
                                                (picked - delivered) * 1LL * dp[picked][delivered]) % MOD;
                }
            }
        }

        return dp[n][n];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 4. Dynamic Programming (Space Optimized)

In the bottom-up approach, when processing states for a given number of picked orders, we only need the current row of delivered counts. After processing all deliveries for the current picked count, we can transition to the next picked count and discard the old row.

```cpp
class Solution {
public:
    int countOrders(int n) {
        const int MOD = 1000000007;
        vector<int> dp(n + 1);
        dp[0] = 1;

        for (int picked = 0; picked <= n; picked++) {
            for (int delivered = 0; delivered < picked; delivered++) {
                dp[delivered + 1] = (int)((dp[delivered + 1] +
                                    (picked - delivered) * 1LL * dp[delivered]) % MOD);
            }
            if (picked < n) {
                vector<int> next_dp(n + 1);
                for (int delivered = 0; delivered <= picked; delivered++) {
                    next_dp[delivered] = (int)((next_dp[delivered] +
                                         (n - picked) * 1LL * dp[delivered]) % MOD);
                }
                dp = next_dp;
            }
        }

        return dp[n];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 5. Combinatorics

Think of placing pickup and delivery events into `2n` slots. For each order, we place its pickup first and then choose where to put the delivery among the remaining slots. When placing order `i`, there are `(2i - 1)` slots left, and we can place the delivery in any of the `(2i - 1) * 2i / 2` ways (choosing 2 slots for the pair where pickup comes first).

```cpp
class Solution {
public:
    int countOrders(int n) {
        const int MOD = 1000000007;
        long long slots = 2 * n, res = 1;

        while (slots > 0) {
            long long validChoices = slots * (slots - 1) / 2;
            res = (res * validChoices) % MOD;
            slots -= 2;
        }
        return (int) res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 6. Probability

The total number of arrangements of `2n` events is `(2n)!`. However, for each order, the delivery must come after the pickup, which has a `1/2` probability in a random arrangement. Since we have `n` independent orders, the valid arrangements are `(2n)! / 2^n`.

```cpp
class Solution {
public:
    int countOrders(int n) {
        const int MOD = 1000000007;
        long long res = 1;

        for (int slot = 1; slot <= 2 * n; slot++) {
            res *= slot;
            if (slot % 2 == 0) {
                res >>= 1;
            }
            res %= MOD;
        }
        return (int) res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
