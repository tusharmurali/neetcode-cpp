# 935. Knight Dialer

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/knight-dialer/>  
- **NeetCode:** <https://neetcode.io/problems/knight-dialer>  
- **Video:** <https://www.youtube.com/watch?v=vlsUUm_qqsY>  

[← Back to index](../INDEX.md)

## 1. Recursion

A knight on a phone dial pad can only jump to specific digits based on its L-shaped movement. For example, from digit 1, the knight can reach 6 or 8. We can precompute these valid jumps for each digit. To count all n-digit numbers, we try starting from each digit and recursively count how many paths of length n exist. This explores all possibilities but leads to massive redundant computation.

```cpp
class Solution {
private:
    static constexpr int MOD = 1000000007;
    const vector<vector<int>> jumps = {
        {4, 6}, {6, 8}, {7, 9}, {4, 8}, {0, 3, 9},
        {}, {0, 1, 7}, {2, 6}, {1, 3}, {2, 4}
    };

public:
    int knightDialer(int n) {
        if (n == 1) return 10;
        int res = 0;

        for (int d = 0; d < 10; d++) {
            res = (res + dfs(n - 1, d)) % MOD;
        }
        return res;
    }

private:
    int dfs(int n, int d) {
        if (n == 0) return 1;

        int res = 0;
        for (int next : jumps[d]) {
            res = (res + dfs(n - 1, next)) % MOD;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(3 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Dynamic Programming (Top-Down)

The recursive solution recalculates the same subproblems many times. For instance, the count of paths from digit `4` with `5` remaining steps is computed repeatedly. By memoizing results in a 2D array indexed by `(digit, remaining steps)`, we avoid redundant work. Each unique state is computed only once.

```cpp
class Solution {
private:
    static constexpr int MOD = 1000000007;
    vector<vector<int>> jumps = {
        {4, 6}, {6, 8}, {7, 9}, {4, 8}, {0, 3, 9},
        {}, {0, 1, 7}, {2, 6}, {1, 3}, {2, 4}
    };
    vector<vector<int>> dp;

public:
    int knightDialer(int n) {
        if (n == 1) return 10;
        dp.assign(10, vector<int>(n + 1, -1));

        int res = 0;
        for (int d = 0; d < 10; d++) {
            res = (res + dfs(n - 1, d)) % MOD;
        }
        return res;
    }

private:
    int dfs(int n, int d) {
        if (n == 0) return 1;
        if (dp[d][n] != -1) return dp[d][n];

        dp[d][n] = 0;
        for (int next : jumps[d]) {
            dp[d][n] = (dp[d][n] + dfs(n - 1, next)) % MOD;
        }
        return dp[d][n];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

Instead of recursing from the top, we can build up from the base case. Starting with step `0` (each digit has exactly 1 way to form a 1-digit number), we iteratively compute the counts for step `1`, step `2`, and so on up to step `n-1`. At each step, the count for a digit equals the sum of counts from all digits that can jump to it.

```cpp
class Solution {
private:
    static constexpr int MOD = 1000000007;
    vector<vector<int>> jumps = {
        {4, 6}, {6, 8}, {7, 9}, {4, 8}, {0, 3, 9},
        {}, {0, 1, 7}, {2, 6}, {1, 3}, {2, 4}
    };

public:
    int knightDialer(int n) {
        if (n == 1) return 10;

        vector<vector<int>> dp(10, vector<int>(n + 1, 0));
        for (int d = 0; d < 10; d++) {
            dp[d][0] = 1;
        }

        for (int step = 1; step < n; step++) {
            for (int d = 0; d < 10; d++) {
                for (int j : jumps[d]) {
                    dp[d][step] = (dp[d][step] + dp[j][step - 1]) % MOD;
                }
            }
        }

        int res = 0;
        for (int d = 0; d < 10; d++) {
            res = (res + dp[d][n - 1]) % MOD;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Space Optimized)

Since each step only depends on the previous step, we don't need to store the entire DP table. We can use two 1D arrays (or swap between them) to track counts for the current and previous steps. This reduces space from `O(10 * n)` to `O(10)`, which is effectively `O(1)`.

```cpp
class Solution {
private:
    static constexpr int MOD = 1000000007;
    vector<vector<int>> jumps = {
        {4, 6}, {6, 8}, {7, 9}, {4, 8}, {0, 3, 9},
        {}, {0, 1, 7}, {2, 6}, {1, 3}, {2, 4}
    };

public:
    int knightDialer(int n) {
        if (n == 1) return 10;

        vector<int> dp(10, 1);

        for (int step = 0; step < n - 1; step++) {
            vector<int> nextDp(10, 0);
            for (int d = 0; d < 10; d++) {
                for (int j : jumps[d]) {
                    nextDp[j] = (nextDp[j] + dp[d]) % MOD;
                }
            }
            dp = nextDp;
        }

        int res = 0;
        for (int d : dp) {
            res = (res + d) % MOD;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 5. Dynamic Programming (Optimal)

We can exploit the symmetry in the phone dial pad. Due to the knight's movement pattern, several digits behave identically: digits `1`, `3`, `7`, `9` form one group (corners), digits `2` and `8` form another (top and bottom), digits `4` and `6` another (left and right), and digit `0` is alone. By grouping these, we reduce the state space to just 4 values, leading to constant-time transitions per step.

```cpp
class Solution {
public:
    int knightDialer(int n) {
        if (n == 1) return 10;

        const int MOD = 1000000007;
        vector<long long> jumps = {1, 4, 2, 2}; // [D, A, B, C]

        for (int i = 0; i < n - 1; i++) {
            vector<long long> tmp(4);
            tmp[0] = jumps[3];
            tmp[1] = (2 * jumps[2] + 2 * jumps[3]) % MOD;
            tmp[2] = jumps[1];
            tmp[3] = (2 * jumps[0] + jumps[1]) % MOD;
            jumps = tmp;
        }

        return (jumps[0] + jumps[1] + jumps[2] + jumps[3]) % MOD;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 6. Matrix Exponentiation

The transition from one step to the next can be represented as a matrix multiplication. If we encode the adjacency of knight jumps in a 10x10 matrix, then raising this matrix to the power `n-1` gives us the count of paths of length `n`. Matrix exponentiation allows us to compute the result in `O(log n)` time, making this approach extremely efficient for very large `n`.

```cpp
class Matrix {
public:
    vector<vector<int>> a;
    int size;
    static const int MOD = 1'000'000'007;

    Matrix(int n) : size(n) {
        a.assign(n, vector<int>(n, 0));
    }

    Matrix operator*(const Matrix &other) const {
        Matrix product(size);
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                for (int k = 0; k < size; k++) {
                    product.a[i][k] = (product.a[i][k] + 1LL * a[i][j] * other.a[j][k]) % MOD;
                }
            }
        }
        return product;
    }
};

Matrix matpow(Matrix mat, int n, int size) {
    Matrix res(size);
    for (int i = 0; i < size; i++) {
        res.a[i][i] = 1; // Identity matrix
    }

    while (n > 0) {
        if (n & 1) res = res * mat;
        mat = mat * mat;
        n >>= 1;
    }
    return res;
}

class Solution {
public:
    int knightDialer(int n) {
        if (n == 1) return 10;

        vector<vector<int>> jumps = {
            {4, 6}, {6, 8}, {7, 9}, {4, 8}, {0, 3, 9},
            {}, {0, 1, 7}, {2, 6}, {1, 3}, {2, 4}
        };

        Matrix mat(10);
        for (int i = 0; i < 10; i++) {
            for (int j : jumps[i]) {
                mat.a[i][j] = 1;
            }
        }

        Matrix res = matpow(mat, n - 1, 10);

        int ans = 0;
        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 10; j++) {
                ans = (ans + res.a[i][j]) % Matrix::MOD;
            }
        }
        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$
