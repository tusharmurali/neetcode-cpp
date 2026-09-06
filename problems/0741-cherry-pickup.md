# 741. Cherry Pickup

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/cherry-pickup/>  
- **NeetCode:** <https://neetcode.io/problems/cherry-pickup>  

[← Back to index](../INDEX.md)

## 1. Recursion

Instead of thinking about one person going from the top-left to the bottom-right and then back, we can simulate two people starting from the top-left and moving simultaneously toward the bottom-right. Since both paths must eventually reach the destination, we track their positions using four variables `(r1, c1)` and `(r2, c2)`. At each step, both move either down or right, giving us 4 combinations of moves. When they land on the same cell, we only count the cherries once to avoid double counting.

```cpp
class Solution {
public:
    int cherryPickup(vector<vector<int>>& grid) {
        int n = grid.size();
        return max(0, dfs(0, 0, 0, 0, grid, n));
    }

    int dfs(int r1, int c1, int r2, int c2, vector<vector<int>>& grid, int n) {
        if (r1 >= n || c1 >= n || r2 >= n || c2 >= n || grid[r1][c1] == -1 || grid[r2][c2] == -1)
            return -1000;

        if (r1 == n - 1 && c1 == n - 1 && r2 == n - 1 && c2 == n - 1)
            return grid[r1][c1];

        int res = dfs(r1 + 1, c1, r2 + 1, c2, grid, n);
        res = max(res, dfs(r1 + 1, c1, r2, c2 + 1, grid, n));
        res = max(res, dfs(r1, c1 + 1, r2 + 1, c2, grid, n));
        res = max(res, dfs(r1, c1 + 1, r2, c2 + 1, grid, n));
        res += grid[r1][c1] + grid[r2][c2];
        if (r1 == r2 && c1 == c2) res -= grid[r1][c1];
        return res;
    }
};
```

**Complexity**

* Time complexity: $O(16 ^ n)$
* Space complexity: $O(n)$ for recursion stack.

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems since the same combination of positions can be reached through different paths. By storing the results of each state `(r1, c1, r2, c2)` in a 4D memoization table, we avoid redundant calculations. This transforms the exponential time complexity into polynomial time.

```cpp
class Solution {
public:
    int n;
    vector<vector<vector<vector<int>>>> dp;
    vector<vector<int>> grid;

    int cherryPickup(vector<vector<int>>& grid) {
        this->n = grid.size();
        this->grid = grid;
        dp = vector(n, vector(n, vector(n, vector<int>(n, INT_MIN))));
        return max(0, dfs(0, 0, 0, 0));
    }

    int dfs(int r1, int c1, int r2, int c2) {
        if (r1 >= n || c1 >= n || r2 >= n || c2 >= n ||
            grid[r1][c1] == -1 || grid[r2][c2] == -1) {
            return -1000;
        }
        if (r1 == n - 1 && c1 == n - 1 && r2 == n - 1 && c2 == n - 1) {
            return grid[r1][c1];
        }
        if (dp[r1][c1][r2][c2] != INT_MIN) {
            return dp[r1][c1][r2][c2];
        }
        int res = dfs(r1 + 1, c1, r2 + 1, c2);
        res = max(res, dfs(r1 + 1, c1, r2, c2 + 1));
        res = max(res, dfs(r1, c1 + 1, r2 + 1, c2));
        res = max(res, dfs(r1, c1 + 1, r2, c2 + 1));
        res += grid[r1][c1] + grid[r2][c2];
        if (r1 == r2 && c1 == c2) res -= grid[r1][c1];
        return dp[r1][c1][r2][c2] = res;
    }
};
```

**Complexity**

* Time complexity: $O(n ^ 4)$
* Space complexity: $O(n ^ 4)$

## 3. Dynamic Programming (Top-Down) Optimized

We can reduce the state space by observing that both people always take the same number of steps. If person 1 is at `(r1, c1)`, then they have taken `r1 + c1` steps. Since person 2 has also taken the same number of steps, if we know `r2`, we can derive `c2` as `(r1 + c1 - r2)`. This reduces our state from 4 dimensions to 3 dimensions.

```cpp
class Solution {
    vector<vector<vector<int>>> dp;
    vector<vector<int>> grid;
    int n;

public:
    int cherryPickup(vector<vector<int>>& grid) {
        this->n = grid.size();
        this->grid = grid;
        dp.assign(n, vector<vector<int>>(n, vector<int>(n, INT_MIN)));
        return max(0, dfs(0, 0, 0));
    }

    int dfs(int r1, int c1, int r2) {
        int c2 = r1 + c1 - r2;
        if (r1 >= n || c1 >= n || r2 >= n || c2 >= n || grid[r1][c1] == -1 || grid[r2][c2] == -1)
            return -1000;

        if (r1 == n - 1 && c1 == n - 1)
            return grid[r1][c1];

        if (dp[r1][c1][r2] != INT_MIN)
            return dp[r1][c1][r2];

        int res = dfs(r1 + 1, c1, r2 + 1);
        res = max(res, dfs(r1 + 1, c1, r2));
        res = max(res, dfs(r1, c1 + 1, r2 + 1));
        res = max(res, dfs(r1, c1 + 1, r2));

        res += grid[r1][c1];
        if (!(r1 == r2 && c1 == c2)) res += grid[r2][c2];

        return dp[r1][c1][r2] = res;
    }
};
```

**Complexity**

* Time complexity: $O(n ^ 3)$
* Space complexity: $O(n ^ 3)$

## 4. Dynamic Programming (Bottom-Up)

Instead of recursion with memoization, we can fill the DP table iteratively starting from the destination and working backward to the start. We iterate through all valid combinations of `(r1, c1, r2)` in reverse order, computing `c2` from the constraint, and build up the solution from smaller subproblems.

```cpp
class Solution {
public:
    int cherryPickup(vector<vector<int>>& grid) {
        int n = grid.size();
        vector<vector<vector<int>>> dp(n, vector<vector<int>>(n, vector<int>(n, -1000000000)));

        for (int r1 = n - 1; r1 >= 0; r1--) {
            for (int c1 = n - 1; c1 >= 0; c1--) {
                for (int r2 = n - 1; r2 >= 0; r2--) {
                    int c2 = r1 + c1 - r2;
                    if (c2 < 0 || c2 >= n) continue;
                    if (grid[r1][c1] == -1 || grid[r2][c2] == -1) continue;

                    if (r1 == n - 1 && c1 == n - 1) {
                        dp[r1][c1][r2] = grid[r1][c1];
                    } else {
                        int res = -1000000000;
                        if (r1 + 1 < n && r2 + 1 < n) res = max(res, dp[r1 + 1][c1][r2 + 1]);
                        if (r1 + 1 < n) res = max(res, dp[r1 + 1][c1][r2]);
                        if (c1 + 1 < n && r2 + 1 < n) res = max(res, dp[r1][c1 + 1][r2 + 1]);
                        if (c1 + 1 < n) res = max(res, dp[r1][c1 + 1][r2]);
                        if (res == -1000000000) continue;
                        res += grid[r1][c1];
                        if (r1 != r2 || c1 != c2) res += grid[r2][c2];
                        dp[r1][c1][r2] = res;
                    }
                }
            }
        }
        return max(0, dp[0][0][0]);
    }
};
```

**Complexity**

* Time complexity: $O(n ^ 3)$
* Space complexity: $O(n ^ 3)$

## 5. Dynamic Programming (Space Optimized)

Since we process states by the total number of steps `k = r1 + c1 = r2 + c2`, and each state only depends on states from the previous step count, we only need to keep track of the previous layer. This reduces space from `O(n^3)` to `O(n^2)` by using two 2D arrays that alternate between the current and previous step.

```cpp
class Solution {
public:
    int cherryPickup(vector<vector<int>>& grid) {
        int n = grid.size();
        vector<vector<int>> prev(n, vector<int>(n, INT_MIN));
        prev[0][0] = grid[0][0];

        for (int k = 1; k < 2 * n - 1; k++) {
            vector<vector<int>> dp(n, vector<int>(n, INT_MIN));
            for (int r1 = max(0, k - (n - 1)); r1 <= min(n - 1, k); r1++) {
                int c1 = k - r1;
                if (c1 >= n || grid[r1][c1] == -1) continue;
                for (int r2 = max(0, k - (n - 1)); r2 <= min(n - 1, k); r2++) {
                    int c2 = k - r2;
                    if (c2 >= n || grid[r2][c2] == -1) continue;
                    int val = prev[r1][r2];
                    if (r1 > 0) val = max(val, prev[r1 - 1][r2]);
                    if (r2 > 0) val = max(val, prev[r1][r2 - 1]);
                    if (r1 > 0 && r2 > 0) val = max(val, prev[r1 - 1][r2 - 1]);
                    if (val < 0) continue;
                    val += grid[r1][c1];
                    if (r1 != r2) val += grid[r2][c2];
                    dp[r1][r2] = val;
                }
            }
            prev = dp;
        }

        return max(0, prev[n - 1][n - 1]);
    }
};
```

**Complexity**

* Time complexity: $O(n ^ 3)$
* Space complexity: $O(n ^ 2)$
