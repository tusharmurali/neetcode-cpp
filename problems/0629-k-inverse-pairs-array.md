# 629. K Inverse Pairs Array

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/k-inverse-pairs-array/>  
- **NeetCode:** <https://neetcode.io/problems/k-inverse-pairs-array>  
- **Video:** <https://www.youtube.com/watch?v=dglwb30bUKI>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

When placing the number `n` into a permutation of `n - 1` elements, we can create `0` to `n - 1` new inverse pairs depending on its position. Placing `n` at the end creates `0` new pairs, while placing it at the start creates `n - 1` pairs since `n` is larger than all other elements. This gives us a recurrence: the count for `(n, k)` equals the sum of counts for `(n - 1, k)`, `(n - 1, k - 1)`, ..., `(n - 1, k - (n - 1))`.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;
    vector<vector<int>> dp;

    int count(int n, int k) {
        if (n == 0) {
            return k == 0 ? 1 : 0;
        }
        if (k < 0) {
            return 0;
        }
        if (dp[n][k] != -1) {
            return dp[n][k];
        }

        int res = 0;
        for (int i = 0; i < n; ++i) {
            res = (res + count(n - 1, k - i)) % MOD;
        }
        dp[n][k] = res;
        return res;
    }

public:
    int kInversePairs(int n, int k) {
        dp.assign(n + 1, vector<int>(k + 1, -1));
        return count(n, k);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * k)$
- Space complexity: $O(n * k)$

> Where $n$ is the size of the permutation and $k$ is the number of inverse pairs in the permutation.

## 2. Dynamic Programming (Top-Down Optimized)

The basic recurrence sums up to `n` terms. We can optimize using the relationship: `count(n, k) = count(n, k - 1) + count(n - 1, k) - count(n - 1, k - n)`. This comes from observing that `count(n, k)` and `count(n, k - 1)` share most terms, differing only at the boundaries. We also add early termination when `k` exceeds the maximum possible inverse pairs for `n` elements, which is `n * (n - 1) / 2`.

```cpp
class Solution {
private:
    static const int MOD = 1e9 + 7;
    vector<vector<int>> dp;

    int count(int n, int k) {
        if (k == 0) return 1;
        if (n == 1) return 0;
        if (n * (n - 1) / 2 < k) return 0;
        if (n * (n - 1) / 2 == k) return 1;
        if (dp[n][k] != -1) return dp[n][k];

        long long res = count(n, k - 1);
        if (k >= n) {
            res -= count(n - 1, k - n);
        }
        res = (res + count(n - 1, k) + MOD) % MOD;

        dp[n][k] = int(res);
        return dp[n][k];
    }

public:
    int kInversePairs(int n, int k) {
        dp.assign(n + 1, vector<int>(k + 1, -1));
        return count(n, k);
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(n * k)$

> Where $n$ is the size of the permutation and $k$ is the number of inverse pairs in the permutation.

## 3. Dynamic Programming (Bottom-Up)

We build up the solution starting from smaller values of `n`. For each `(N, K)` state, we sum contributions from placing element `N` at different positions, each creating a different number of new inverse pairs. This iterative approach avoids recursion overhead and naturally fills the DP table row by row.

```cpp
class Solution {
public:
    int kInversePairs(int n, int k) {
        const int MOD = 1e9 + 7;
        vector<vector<int>> dp(n + 1, vector<int>(k + 1, 0));
        dp[0][0] = 1;

        for (int N = 1; N <= n; N++) {
            for (int K = 0; K <= k; K++) {
                for (int pairs = 0; pairs < N; pairs++) {
                    if (K - pairs >= 0) {
                        dp[N][K] = (dp[N][K] + dp[N - 1][K - pairs]) % MOD;
                    }
                }
            }
        }

        return dp[n][k];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * k)$
- Space complexity: $O(n * k)$

> Where $n$ is the size of the permutation and $k$ is the number of inverse pairs in the permutation.

## 4. Dynamic Programming (Bottom-Up Optimized)

Rather than summing `N` terms for each cell, we use the sliding window observation from the top-down optimized approach. The value at `dp[N][K]` builds on `dp[N][K - 1]` by adding `dp[N - 1][K]` (the new term entering the window) and subtracting `dp[N - 1][K - N]` (the term leaving the window). This reduces each cell computation to constant time.

```cpp
class Solution {
public:
    int kInversePairs(int n, int k) {
        const int MOD = 1e9 + 7;
        vector<vector<int>> dp(n + 1, vector<int>(k + 1, 0));
        dp[0][0] = 1;

        for (int N = 1; N <= n; N++) {
            for (int K = 0; K <= k; K++) {
                dp[N][K] = dp[N - 1][K];
                if (K > 0) {
                    dp[N][K] = (dp[N][K] + dp[N][K - 1]) % MOD;
                }
                if (K >= N) {
                    dp[N][K] = (dp[N][K] - dp[N - 1][K - N] + MOD) % MOD;
                }
            }
        }

        return dp[n][k];
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(n * k)$

> Where $n$ is the size of the permutation and $k$ is the number of inverse pairs in the permutation.

## 5. Dynamic Programming (Space Optimized)

Since each row only depends on the previous row, we only need to keep two 1D arrays instead of the full 2D table. We maintain a running total that acts as a prefix sum, adding new values and subtracting values that fall outside the window of size `N`.

```cpp
class Solution {
public:
    int kInversePairs(int n, int k) {
        const int MOD = 1e9 + 7;
        vector<int> prev(k + 1, 0);
        prev[0] = 1;

        for (int N = 1; N <= n; N++) {
            vector<int> cur(k + 1, 0);
            int total = 0;
            for (int K = 0; K <= k; K++) {
                total = (total + prev[K]) % MOD;
                if (K >= N) {
                    total = (total - prev[K - N] + MOD) % MOD;
                }
                cur[K] = total;
            }
            prev = cur;
        }

        return prev[k];
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(k)$

> Where $n$ is the size of the permutation and $k$ is the number of inverse pairs in the permutation.
