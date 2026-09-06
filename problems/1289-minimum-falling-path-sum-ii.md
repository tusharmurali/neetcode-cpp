# 1289. Minimum Falling Path Sum II

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-falling-path-sum-ii/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-falling-path-sum-ii>  
- **Video:** <https://www.youtube.com/watch?v=_b8sptrsFEM>  

[← Back to index](../INDEX.md)

## 1. Recursion

Unlike the standard falling path problem where we can move to adjacent columns, here we must pick a different column in each row. For each cell in a row, we recursively try all columns in the next row except the current one. This constraint increases complexity since we need to consider more transitions. The brute force approach explores all valid paths.

```cpp
class Solution {
    int helper(vector<vector<int>>& grid, int r, int c) {
        int N = grid.size();
        if (r == N - 1) {
            return grid[r][c];
        }
        int res = INT_MAX;
        for (int nextCol = 0; nextCol < N; nextCol++) {
            if (c != nextCol) {
                res = min(res, grid[r][c] + helper(grid, r + 1, nextCol));
            }
        }
        return res;
    }

public:
    int minFallingPathSum(vector<vector<int>>& grid) {
        int N = grid.size();
        int res = INT_MAX;
        for (int c = 0; c < N; c++) {
            res = min(res, helper(grid, 0, c));
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Dynamic Programming (Top-Down)

The recursive solution recomputes the same `(r, c)` states multiple times. By storing computed results in a memoization table, we ensure each state is solved only once. This reduces time complexity from exponential to O(n^3), since for each of the n^2 cells, we may consider up to n transitions.

```cpp
class Solution {
    vector<vector<int>> memo;

    int helper(vector<vector<int>>& grid, int r, int c) {
        int N = grid.size();
        if (r == N - 1) {
            return grid[r][c];
        }
        if (memo[r][c] != INT_MIN) {
            return memo[r][c];
        }
        int res = INT_MAX;
        for (int nextCol = 0; nextCol < N; nextCol++) {
            if (c != nextCol) {
                res = min(res, grid[r][c] + helper(grid, r + 1, nextCol));
            }
        }
        memo[r][c] = res;
        return res;
    }

public:
    int minFallingPathSum(vector<vector<int>>& grid) {
        int N = grid.size();
        memo.assign(N, vector<int>(N, INT_MIN));
        int res = INT_MAX;
        for (int c = 0; c < N; c++) {
            res = min(res, helper(grid, 0, c));
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(n ^ 2)$

## 3. Dynamic Programming (Bottom-Up)

We can build the solution iteratively from the last row upward. For each cell, we compute the minimum path sum by considering all columns in the next row except the current one. This bottom-up approach fills a 2D DP table where `dp[r][c]` represents the minimum path sum from cell `(r, c)` to any cell in the last row.

```cpp
class Solution {
public:
    int minFallingPathSum(vector<vector<int>>& grid) {
        int N = grid.size();
        vector<vector<int>> dp(N, vector<int>(N, INT_MAX));

        for (int c = 0; c < N; c++) {
            dp[N - 1][c] = grid[N - 1][c];
        }

        for (int r = N - 2; r >= 0; r--) {
            for (int c = 0; c < N; c++) {
                dp[r][c] = INT_MAX;
                for (int nextCol = 0; nextCol < N; nextCol++) {
                    if (c != nextCol) {
                        dp[r][c] = min(dp[r][c], grid[r][c] + dp[r + 1][nextCol]);
                    }
                }
            }
        }

        int res = INT_MAX;
        for (int c = 0; c < N; c++) {
            res = min(res, dp[0][c]);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(n ^ 2)$

## 4. Dynamic Programming (Space Optimized)

Since each row only depends on the next row's values, we can reduce space from O(n^2) to O(n) by using a single 1D array. We process rows from top to bottom, updating the array for each row while referencing the values from the previous iteration.

```cpp
class Solution {
public:
    int minFallingPathSum(vector<vector<int>>& grid) {
        int N = grid.size();
        vector<int> dp = grid[0];

        for (int r = 1; r < N; r++) {
            vector<int> nextDp(N, INT_MAX);
            for (int currC = 0; currC < N; currC++) {
                for (int prevC = 0; prevC < N; prevC++) {
                    if (prevC != currC) {
                        nextDp[currC] = min(
                            nextDp[currC],
                            grid[r][currC] + dp[prevC]
                        );
                    }
                }
            }
            dp = nextDp;
        }

        return *min_element(dp.begin(), dp.end());
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(n)$

## 5. Dynamic Programming (Time Optimized)

The O(n^3) complexity comes from checking all `n` columns for each of `n^2` cells. We can optimize by observing that when transitioning to a cell, we usually want the minimum from the previous row, unless that minimum is in the same column. So we only need to track the two smallest values from each row: if the current column matches the smallest, use the second smallest; otherwise, use the smallest.

```cpp
class Solution {
public:
    int minFallingPathSum(vector<vector<int>>& grid) {
        int N = grid.size();

        auto getMinTwo = [](vector<pair<int, int>>& row) {
            vector<pair<int, int>> twoSmallest;
            for (auto& entry : row) {
                if (twoSmallest.size() < 2) {
                    twoSmallest.push_back(entry);
                } else if (twoSmallest[1].first > entry.first) {
                    twoSmallest.pop_back();
                    twoSmallest.push_back(entry);
                }
                sort(twoSmallest.begin(), twoSmallest.end());
            }
            return twoSmallest;
        };

        vector<pair<int, int>> firstRow;
        for (int i = 0; i < grid[0].size(); i++) {
            firstRow.push_back({grid[0][i], i});
        }

        vector<pair<int, int>> dp = getMinTwo(firstRow);

        for (int r = 1; r < N; r++) {
            vector<pair<int, int>> nextDp;
            for (int c = 0; c < grid[0].size(); c++) {
                int currVal = grid[r][c];
                int minVal = INT_MAX;
                for (auto& prev : dp) {
                    if (prev.second != c) {
                        minVal = min(minVal, currVal + prev.first);
                    }
                }
                nextDp.push_back({minVal, c});
            }
            dp = getMinTwo(nextDp);
        }

        int result = INT_MAX;
        for (auto& entry : dp) {
            result = min(result, entry.first);
        }
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 6. Dynamic Programming (Optimal)

We can further optimize by not storing an entire array of pairs. Instead, we only track four values: the index and value of the smallest element, and the index and value of the second smallest element from the previous row. For each cell in the current row, we add the appropriate previous minimum based on column matching. Then we update our tracked values for the next iteration. This achieves O(n^2) time with O(1) extra space.

```cpp
class Solution {
public:
    int minFallingPathSum(vector<vector<int>>& grid) {
        int n = grid.size();
        if (n == 1) {
            return grid[0][0];
        }

        int dpIdx1 = -1, dpIdx2 = -1;
        int dpVal1 = 0, dpVal2 = 0;

        for (int i = 1; i < n; i++) {
            int nextDpIdx1 = -1, nextDpIdx2 = -1;
            int nextDpVal1 = INT_MAX, nextDpVal2 = INT_MAX;

            for (int j = 0; j < n; j++) {
                int cur = (j != dpIdx1) ? dpVal1 : dpVal2;
                cur += grid[i][j];

                if (nextDpIdx1 == -1 || cur < nextDpVal1) {
                    nextDpIdx2 = nextDpIdx1;
                    nextDpVal2 = nextDpVal1;
                    nextDpIdx1 = j;
                    nextDpVal1 = cur;
                } else if (nextDpIdx2 == -1 || cur < nextDpVal2) {
                    nextDpIdx2 = j;
                    nextDpVal2 = cur;
                }
            }

            dpIdx1 = nextDpIdx1;
            dpIdx2 = nextDpIdx2;
            dpVal1 = nextDpVal1;
            dpVal2 = nextDpVal2;
        }

        return dpVal1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.
