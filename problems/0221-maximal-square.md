# 221. Maximal Square

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximal-square/>  
- **NeetCode:** <https://neetcode.io/problems/maximal-square>  
- **Video:** <https://www.youtube.com/watch?v=6X7Ha2PrDmM>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each cell containing a `'1'`, we can try to expand a square outward as far as possible. Starting with a 1x1 square, we incrementally check if we can form a 2x2, 3x3, and so on. For each size, we only need to verify the new rightmost column and bottommost row that would be added. If any cell in those edges is `'0'`, we cannot expand further. This approach checks all potential squares explicitly.

```cpp
class Solution {
public:
    int maximalSquare(vector<vector<char>>& matrix) {
        int m = matrix.size(), n = matrix[0].size();
        int res = 0;

        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (matrix[r][c] == '0') {
                    continue;
                }
                int k = 1;
                while (true) {
                    if (r + k > m || c + k > n) {
                        break;
                    }
                    bool flag = true;

                    for (int i = r; i < r + k; i++) {
                        if (matrix[i][c + k - 1] == '0') {
                            flag = false;
                            break;
                        }
                    }
                    for (int j = c; j < c + k; j++) {
                        if (matrix[r + k - 1][j] == '0') {
                            flag = false;
                            break;
                        }
                    }

                    if (!flag) {
                        break;
                    }
                    res = max(res, k * k);
                    k++;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O((m * n) ^ 2)$
- Space complexity: $O(1)$

> Where $m$ is the number of rows and $n$ is the number columns.

## 2. Dynamic Programming (Top-Down)

We can define a recursive function where `dp(r, c)` returns the side length of the largest square whose top-left corner is at `(r, c)`. For a cell with `'1'`, the answer depends on how far we can extend to the right, down, and diagonally. The limiting factor is the minimum of these three directions. We memoize results to avoid redundant computation, then scan all cells to find the maximum value.

```cpp
class Solution {
private:
    vector<vector<int>> dp;

public:
    int maximalSquare(vector<vector<char>>& matrix) {
        int ROWS = matrix.size(), COLS = matrix[0].size();
        dp = vector<vector<int>>(ROWS, vector<int>(COLS, -1));

        dfs(0, 0, matrix);
        int maxSquare = 0;
        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                maxSquare = max(maxSquare, dp[r][c]);
            }
        }
        return maxSquare * maxSquare;
    }

    int dfs(int r, int c, vector<vector<char>>& matrix) {
        if (r >= matrix.size() || c >= matrix[0].size()) {
            return 0;
        }
        if (dp[r][c] != -1) {
            return dp[r][c];
        }
        int down = dfs(r + 1, c, matrix);
        int right = dfs(r, c + 1, matrix);
        int diag = dfs(r + 1, c + 1, matrix);
        dp[r][c] = 0;
        if (matrix[r][c] == '1') {
            dp[r][c] = 1 + min(down, min(right, diag));
        }
        return dp[r][c];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number columns.

## 3. Dynamic Programming (Bottom-Up)

Instead of recursion, we can fill the DP table iteratively from bottom-right to top-left. For each `'1'` cell, the largest square ending there (as the bottom-right corner) is determined by the minimum of the squares ending at its right, bottom, and diagonal neighbors, plus one. This builds up from smaller subproblems to larger ones and avoids recursion overhead.

```cpp
class Solution {
public:
    int maximalSquare(vector<vector<char>>& matrix) {
        int m = matrix.size(), n = matrix[0].size();
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        int maxSquare = 0;

        for (int r = m - 1; r >= 0; r--) {
            for (int c = n - 1; c >= 0; c--) {
                if (matrix[r][c] == '1') {
                    dp[r][c] = 1 + min({dp[r + 1][c], dp[r][c + 1], dp[r + 1][c + 1]});
                    maxSquare = max(maxSquare, dp[r][c]);
                }
            }
        }

        return maxSquare * maxSquare;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number columns.

## 4. Dynamic Programming (Space Optimized)

The bottom-up DP only needs the current row and the next row to compute values. We can reduce space by using a single 1D array. As we process each row from right to left, we keep track of the previous diagonal value in a variable `prev`. This allows us to update the array in place while still having access to all three neighbors needed for the recurrence.

```cpp
class Solution {
public:
    int maximalSquare(vector<vector<char>>& matrix) {
        int m = matrix.size(), n = matrix[0].size();
        vector<int> dp(n + 1, 0);
        int maxSquare = 0;

        for (int r = m - 1; r >= 0; r--) {
            int prev = 0;
            for (int c = n - 1; c >= 0; c--) {
                int temp = dp[c];
                if (matrix[r][c] == '1') {
                    dp[c] = 1 + min({dp[c], dp[c + 1], prev});
                    maxSquare = max(maxSquare, dp[c]);
                } else {
                    dp[c] = 0;
                }
                prev = temp;
            }
        }

        return maxSquare * maxSquare;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(n)$

> Where $m$ is the number of rows and $n$ is the number columns.

## Standalone solution file (`cpp/0221-maximal-square.cpp` in the NeetCode repo)

```cpp
/*
  Given an m x n binary matrix filled with 0's and 1's, find the largest square containing only 1's and return its area.

  Ex. Input: matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]
      Output: 4

  Time  : O(m*n)
  Space : O(m*n)
*/

class Solution {
public:
    int maximalSquare(vector<vector<char>>& matrix) {
        int rows = matrix.size(), cols = matrix[0].size();

        vector<vector<int>> dp (rows+1, vector<int>(cols+1, 0));
        int maxi = 0;
        for(int i = rows-1 ; i >= 0; --i) {
            for(int j = cols-1 ; j >=0 ; --j) {
                if(matrix[i][j] == '1') {
                    int right = dp[i][j+1], dia = dp[i+1][j+1], bottom = dp[i+1][j];
                    
                    dp[i][j] = 1 + min(right, min(dia, bottom));
                    maxi = max(maxi, dp[i][j]);
                }
                else {
                    dp[i][j] = 0;
                }
            }
        }
        return maxi*maxi;
    }
};
```
