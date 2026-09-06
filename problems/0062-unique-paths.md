# 62. Unique Paths

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/unique-paths/>  
- **NeetCode:** <https://neetcode.io/problems/count-paths>  
- **Video:** <https://www.youtube.com/watch?v=IlEsdxuD4lY>  
- **Video approach:** 4. Dynamic Programming (Space Optimized)  

[← Back to index](../INDEX.md)

## 1. Recursion

This is the **pure recursive (brute force)** way to think about the problem.

From any cell `(i, j)` in the grid:

- You can only move **right** or **down**.
- The total number of paths from `(i, j)` is:
    > paths going right + paths going down

Base ideas:

- If you **reach the bottom-right cell**, you found **one valid path**.
- If you **go out of bounds**, that path is invalid (count = 0).

So the problem naturally breaks into **smaller subproblems**, making recursion a direct fit.

```cpp
class Solution {
public:
    int uniquePaths(int m, int n) {
        return dfs(0, 0, m, n);
    }

    int dfs(int i, int j, int m, int n) {
        if (i == (m - 1) && j == (n - 1)) {
            return 1;
        }
        if (i >= m || j >= n) return 0;
        return dfs(i, j + 1, m, n) +
               dfs(i + 1, j, m, n);
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ {m + n})$
- Space complexity: $O(m + n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 2. Dynamic Programming (Top-Down)

This is the **optimized version of recursion** using **memoization**.

In the brute-force approach, the same cell `(i, j)` is solved many times.  
But the number of paths from a cell **never changes**, so we can **store it once and reuse it**.

Think of it this way:

- Every cell `(i, j)` asks:  
  **“How many ways can I reach the destination from here?”**
- Once answered, we **cache** it so we never recompute it.

This turns an exponential recursion into a polynomial-time solution.

```cpp
class Solution {
public:
    vector<vector<int>> memo;
    int uniquePaths(int m, int n) {
        memo.resize(m, vector<int>(n, -1));
        return dfs(0, 0, m, n);
    }

    int dfs(int i, int j, int m, int n) {
        if (i == (m - 1) && j == (n - 1)) {
            return 1;
        }
        if (i >= m || j >= n) return 0;
        if (memo[i][j] != -1) {
            return memo[i][j];
        }
        return memo[i][j] = dfs(i, j + 1, m, n) +
                            dfs(i + 1, j, m, n);
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 3. Dynamic Programming (Bottom-Up)

Instead of starting from the top and recursing, we **build the answer from the destination backward**.

From any cell `(i, j)`, the number of unique paths to the destination is:

- paths from the **cell below** `(i+1, j)`
- plus paths from the **cell to the right** `(i, j+1)`

If we already know these values, we can compute the current cell directly.

So we:

- Set the destination cell to `1`
- Fill the grid **bottom-up**, **right-to-left**

```cpp
class Solution {
public:
    int uniquePaths(int m, int n) {
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        dp[m - 1][n - 1] = 1;

        for (int i = m - 1; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                dp[i][j] += dp[i + 1][j] + dp[i][j + 1];
            }
        }

        return dp[0][0];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 4. Dynamic Programming (Space Optimized) ▶ video

Each cell only depends on:

- the **cell to the right** (same row)
- the **cell below** (previous row)

So instead of storing the entire 2D grid, we can keep **just one row** at a time.
We update the row from **right to left**, using values from:

- the current row (`newRow[j + 1]`)
- the previous row (`row[j]`)

This reduces space while keeping the same logic.

```cpp
class Solution {
public:
    int uniquePaths(int m, int n) {
        vector<int> row(n, 1);

        for (int i = 0; i < m - 1; ++i) {
            vector<int> newRow(n, 1);
            for (int j = n - 2; j >= 0; --j) {
                newRow[j] = newRow[j + 1] + row[j];
            }
            row = newRow;
        }
        return row[0];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 5. Dynamic Programming (Optimal)

From any cell, you can reach the destination by moving:

- **right**
- **down**

The number of ways to reach a cell equals:

> ways from the cell **below** + ways from the cell **to the right**

Instead of using a full 2D table, we notice that:

- each row only depends on the row **below it**
- so a **single 1D array** is enough

We keep updating this array from **right to left**, accumulating paths.

```cpp
class Solution {
public:
    int uniquePaths(int m, int n) {
        vector<int> dp(n, 1);

        for (int i = m - 2; i >= 0; i--) {
            for (int j = n - 2; j >= 0; j--) {
                dp[j] += dp[j + 1];
            }
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 6. Math

To go from the top-left to the bottom-right of an `m x n` grid, you can only move **right** or **down**.

- You must move **down (m - 1)** times
- You must move **right (n - 1)** times

So overall, you make **(m + n - 2)** moves.

The problem becomes:

> In how many different ways can we arrange these right and down moves?

This is a **combinations** problem:

- Choose positions for the right moves (or down moves)

That gives:
$\binom{m+n-2}{n-1}$

```cpp
class Solution {
public:
    int uniquePaths(int m, int n) {
        if (m == 1 || n == 1) {
            return 1;
        }
        if (m < n) {
            swap(m, n);
        }

        long long res = 1;
        int j = 1;
        for (int i = m; i < m + n - 1; i++) {
            res *= i;
            res /= j;
            j++;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(min(m, n))$
- Space complexity: $O(1)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## Standalone solution file (`cpp/0062-unique-paths.cpp` in the NeetCode repo)

```cpp
/*
    Given grid, return # of unique paths from top-left to bottom-right
    Ex. m = 3, n = 2 -> 3 unique paths (R->D->D, D->D->R, D->R->D)

    DP: edges have 1 unique path, inner cells consider where it comes from
    Recurrence relation: grid[i][j] = grid[i-1][j] + grid[i][j-1]

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    int uniquePaths(int m, int n) {
        vector<vector<int>> grid(m, vector<int>(n, 0));
        
        for (int i = 0; i < m; i++) {
            grid[i][0] = 1;
        }
        for (int j = 0; j < n; j++) {
            grid[0][j] = 1;
        }
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                grid[i][j] = grid[i - 1][j] + grid[i][j - 1];
            }
        }
        
        return grid[m - 1][n - 1];
    }
};
```
