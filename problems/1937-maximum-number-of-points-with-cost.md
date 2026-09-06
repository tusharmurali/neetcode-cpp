# 1937. Maximum Number of Points with Cost

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-number-of-points-with-cost/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-number-of-points-with-cost>  
- **Video:** <https://www.youtube.com/watch?v=ik1y7fz8AOc>  

[← Back to index](../INDEX.md)

## 1. Recursion

We need to pick one cell from each row such that the total points are maximized. The tricky part is the penalty: if we pick column `c` in row `r` and column `c'` in row `r+1`, we lose `|c - c'|` points.

A natural approach is to try all possibilities. For each starting column in the first row, we recursively explore all column choices in subsequent rows, subtracting the movement penalty and adding the cell value. We return the maximum sum found.

```cpp
class Solution {
public:
    int m, n;
    vector<vector<int>> points;

    long long dfs(int r, int c) {
        if (r == m - 1) return 0;
        long long res = 0;
        for (int col = 0; col < n; col++) {
            res = max(res, points[r + 1][col] - abs(col - c) + dfs(r + 1, col));
        }
        return res;
    }

    long long maxPoints(vector<vector<int>>& points) {
        this->points = points;
        m = points.size();
        n = points[0].size();
        long long ans = 0;
        for (int c = 0; c < n; c++) {
            ans = max(ans, points[0][c] + dfs(0, c));
        }
        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ m)$
- Space complexity: $O(m)$ for recursion stack.

> Where $m$ is the number of rows, and $n$ is the number of columns.

## 2. Dynamic Programming (Top-Down)

The recursive solution recalculates the same subproblems multiple times. For a given `(row, column)` pair, the maximum points from that position onward is always the same, regardless of how we got there.

By storing (memoizing) the result for each `(r, c)` pair, we avoid redundant computation. This transforms the exponential solution into a polynomial one.

```cpp
class Solution {
public:
    int m, n;
    vector<vector<int>> points;
    vector<vector<long long>> memo;

    long long dfs(int r, int c) {
        if (memo[r][c] != -1) return memo[r][c];
        if (r == m - 1) return 0;

        long long res = 0;
        for (int col = 0; col < n; col++) {
            res = max(res, (long long)points[r + 1][col] - abs(col - c) + dfs(r + 1, col));
        }
        return memo[r][c] = res;
    }

    long long maxPoints(vector<vector<int>>& points) {
        this->points = points;
        m = points.size();
        n = points[0].size();
        memo.assign(m, vector<long long>(n, -1));
        long long ans = 0;
        for (int c = 0; c < n; c++) {
            ans = max(ans, (long long)points[0][c] + dfs(0, c));
        }
        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(m * n ^ 2)$
- Space complexity: $O(n)$

> Where $m$ is the number of rows, and $n$ is the number of columns.

## 3. Dynamic Programming (Bottom-Up)

Computing `max(dp[c'] - |c - c'|)` for each column `c` normally takes `O(n)` time per cell, making the total `O(m * n^2)`. We can optimize this using prefix maximums.

The penalty `|c - c'|` splits into two cases:

- If `c' <= c`: the penalty is `c - c'`, so we want `max(dp[c'] + c')` for all `c' <= c`.
- If `c' > c`: the penalty is `c' - c`, so we want `max(dp[c'] - c')` for all `c' > c`.

By precomputing a `left` array (max of `dp[c'] + c'` from the left) and a `right` array (max of `dp[c'] - c'` from the right), we can answer each column's query in `O(1)` time.

```cpp
class Solution {
public:
    long long maxPoints(vector<vector<int>>& points) {
        int ROWS = points.size(), COLS = points[0].size();
        vector<long long> dp(points[0].begin(), points[0].end());

        for (int r = 1; r < ROWS; r++) {
            vector<long long> left(COLS), right(COLS);
            left[0] = dp[0];
            for (int c = 1; c < COLS; c++)
                left[c] = max(dp[c], left[c - 1] - 1);

            right[COLS - 1] = dp[COLS - 1];
            for (int c = COLS - 2; c >= 0; c--)
                right[c] = max(dp[c], right[c + 1] - 1);

            vector<long long> nextDp(COLS);
            for (int c = 0; c < COLS; c++)
                nextDp[c] = points[r][c] + max(left[c], right[c]);

            dp = move(nextDp);
        }

        return *max_element(dp.begin(), dp.end());
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(n)$

> Where $m$ is the number of rows, and $n$ is the number of columns.

## 4. Dynamic Programming (Space Optimized)

We can reduce memory usage by combining the left and right sweeps into a single pass. Instead of storing separate `left` and `right` arrays, we build the left maximum in a `cur` array during the left-to-right pass. Then, during the right-to-left pass, we update `cur[c]` by taking the max of the current left value and the running right maximum, adding the cell value as we go.

This avoids allocating a separate `right` array, reducing the constant factor in space usage.

```cpp
class Solution {
public:
    long long maxPoints(vector<vector<int>>& points) {
        int rows = points.size(), cols = points[0].size();
        vector<long long> prev(cols);
        for (int c = 0; c < cols; c++) prev[c] = points[0][c];

        for (int r = 1; r < rows; r++) {
            vector<long long> cur(cols);
            cur[0] = prev[0];
            for (int c = 1; c < cols; c++)
                cur[c] = max(prev[c], cur[c - 1] - 1);

            long long rightMax = prev[cols - 1];
            for (int c = cols - 2; c >= 0; c--) {
                rightMax = max(prev[c], rightMax - 1);
                cur[c] = max(cur[c], rightMax) + points[r][c];
            }
            cur[cols - 1] += points[r][cols - 1];
            prev = cur;
        }
        return *max_element(prev.begin(), prev.end());
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(n)$

> Where $m$ is the number of rows, and $n$ is the number of columns.
