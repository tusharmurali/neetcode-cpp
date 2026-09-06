# 931. Minimum Falling Path Sum

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-falling-path-sum/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-falling-path-sum>  
- **Video:** <https://www.youtube.com/watch?v=b_F3mz9l-uQ>  

[← Back to index](../INDEX.md)

## 1. Recursion

A falling path starts at any cell in the first row and moves to an adjacent cell in the next row (directly below, diagonally left, or diagonally right). We want to find the path with the minimum sum. For each starting column in the first row, we recursively explore all valid paths and track the minimum total. This brute force approach considers all possible paths, leading to exponential time complexity.

```cpp
class Solution {
private:
    int dfs(int r, int c, vector<vector<int>>& matrix, int N) {
        if (r == N) return 0;
        if (c < 0 || c >= N) return INT_MAX;
        return matrix[r][c] + min({
            dfs(r + 1, c - 1, matrix, N),
            dfs(r + 1, c, matrix, N),
            dfs(r + 1, c + 1, matrix, N)
        });
    }

public:
    int minFallingPathSum(vector<vector<int>>& matrix) {
        int N = matrix.size();
        int res = INT_MAX;
        for (int c = 0; c < N; c++) {
            res = min(res, dfs(0, c, matrix, N));
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(3 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems: the same `(r, c)` state is computed multiple times. By caching results in a `memoization` table, we avoid redundant calculations. Each unique `(r, c)` pair is computed only once, reducing time complexity from exponential to polynomial.

```cpp
class Solution {
private:
    vector<vector<int>> cache;

    int dfs(int r, int c, vector<vector<int>>& matrix, int N) {
        if (r == N) return 0;
        if (c < 0 || c >= N) return INT_MAX;
        if (cache[r][c] != INT_MIN) return cache[r][c];

        cache[r][c] = matrix[r][c] + min({
            dfs(r + 1, c - 1, matrix, N),
            dfs(r + 1, c, matrix, N),
            dfs(r + 1, c + 1, matrix, N)
        });
        return cache[r][c];
    }

public:
    int minFallingPathSum(vector<vector<int>>& matrix) {
        int N = matrix.size();
        cache = vector<vector<int>>(N, vector<int>(N, INT_MIN));

        int res = INT_MAX;
        for (int c = 0; c < N; c++) {
            res = min(res, dfs(0, c, matrix, N));
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * n)$
- Space complexity: $O(n * n)$

## 3. Dynamic Programming (Bottom-Up)

We can solve this iteratively by building up solutions row by row. For each cell, the minimum path sum to reach it equals its value plus the minimum of the three cells above it that could lead here. By processing rows from top to bottom and only keeping the previous row's values, we achieve `O(n)` space complexity.

```cpp
class Solution {
public:
    int minFallingPathSum(vector<vector<int>>& matrix) {
        int N = matrix.size();
        vector<int> dp(N);

        for (int c = 0; c < N; c++) {
            dp[c] = matrix[0][c];
        }

        for (int r = 1; r < N; r++) {
            int leftUp = INT_MAX;
            for (int c = 0; c < N; c++) {
                int midUp = dp[c];
                int rightUp = (c < N - 1) ? dp[c + 1] : INT_MAX;
                dp[c] = matrix[r][c] + min(midUp, min(leftUp, rightUp));
                leftUp = midUp;
            }
        }

        int ans = INT_MAX;
        for (int val : dp) {
            ans = min(ans, val);
        }
        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (In-Place)

If we are allowed to modify the input matrix, we can avoid using any extra space for DP. We update each cell in place to store the minimum path sum to reach that cell. This is the most space-efficient approach, using only `O(1)` extra space beyond the input.

```cpp
class Solution {
public:
    int minFallingPathSum(vector<vector<int>>& matrix) {
        int N = matrix.size();

        for (int r = 1; r < N; r++) {
            for (int c = 0; c < N; c++) {
                int mid = matrix[r - 1][c];
                int left = (c > 0) ? matrix[r - 1][c - 1] : INT_MAX;
                int right = (c < N - 1) ? matrix[r - 1][c + 1] : INT_MAX;
                matrix[r][c] = matrix[r][c] + min({mid, left, right});
            }
        }

        return *min_element(matrix[N - 1].begin(), matrix[N - 1].end());
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.
