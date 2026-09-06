# 64. Minimum Path Sum

- **Difficulty:** Medium  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/minimum-path-sum/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-path-sum>  
- **Video:** <https://www.youtube.com/watch?v=pGMsrvt0fpk>  

[← Back to index](../INDEX.md)

## 1. Recursion

From any cell, we can only move right or down. To find the minimum path sum to the bottom-right corner, we consider both choices and take the minimum. At the destination cell, we simply return its value. This naturally leads to a recursive solution where we explore all possible paths by branching at each cell.

```cpp
class Solution {
public:
    int minPathSum(vector<vector<int>>& grid) {
        return dfs(0, 0, grid);
    }

    int dfs(int r, int c, vector<vector<int>>& grid) {
        if (r == grid.size() - 1 && c == grid[0].size() - 1) {
            return grid[r][c];
        }
        if (r == grid.size() || c == grid[0].size()) {
            return INT_MAX;
        }
        return grid[r][c] + min(dfs(r + 1, c, grid), dfs(r, c + 1, grid));
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ {m + n})$
- Space complexity: $O(m + n)$ for recursion stack.

> Where $m$ is the number of rows and $n$ is the number of columns.

## 2. Dynamic Programming (Top-Down)

The plain recursive solution recalculates the same cells many times. For instance, both `dfs(0,1)` and `dfs(1,0)` might call `dfs(1,1)`. By caching (memoizing) results for each cell, we ensure each subproblem is solved only once. This transforms exponential time into polynomial time.

```cpp
class Solution {
private:
    vector<vector<int>> dp;

public:
    int minPathSum(vector<vector<int>>& grid) {
        int m = grid.size(), n = grid[0].size();
        dp = vector<vector<int>>(m, vector<int>(n, -1));
        return dfs(0, 0, grid);
    }

    int dfs(int r, int c, vector<vector<int>>& grid) {
        if (r == grid.size() - 1 && c == grid[0].size() - 1) {
            return grid[r][c];
        }
        if (r == grid.size() || c == grid[0].size()) {
            return INT_MAX;
        }
        if (dp[r][c] != -1) {
            return dp[r][c];
        }

        dp[r][c] = grid[r][c] + min(dfs(r + 1, c, grid), dfs(r, c + 1, grid));
        return dp[r][c];
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns.

## 3. Dynamic Programming (Bottom-Up)

Instead of recursing from top-left to bottom-right, we can fill a DP table starting from the bottom-right corner. For each cell, we know the minimum path sum to reach the destination from the cell below and from the cell to the right. We take the minimum of these two and add the current cell value. This iterative approach avoids recursion overhead.

```cpp
class Solution {
public:
    int minPathSum(vector<vector<int>>& grid) {
        int ROWS = grid.size(), COLS = grid[0].size();
        vector<vector<int>> dp(ROWS + 1, vector<int>(COLS + 1, INT_MAX));
        dp[ROWS - 1][COLS] = 0;

        for (int r = ROWS - 1; r >= 0; r--) {
            for (int c = COLS - 1; c >= 0; c--) {
                dp[r][c] = grid[r][c] + min(dp[r + 1][c], dp[r][c + 1]);
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

## 4. Dynamic Programming (Space Optimized)

When filling the DP table row by row (from bottom to top), we only need the current row and the row below. In fact, since we process columns right to left, we can overwrite the same 1D array. The value at `dp[c]` represents the minimum path sum from `(r+1, c)`, and `dp[c+1]` represents the path from `(r, c+1)`. After updating, `dp[c]` will hold the result for `(r, c)`.

```cpp
class Solution {
public:
    int minPathSum(vector<vector<int>>& grid) {
        int ROWS = grid.size(), COLS = grid[0].size();
        vector<int> dp(COLS + 1, INT_MAX);
        dp[COLS - 1] = 0;

        for (int r = ROWS - 1; r >= 0; r--) {
            for (int c = COLS - 1; c >= 0; c--) {
                dp[c] = grid[r][c] + min(dp[c], dp[c + 1]);
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

## Standalone solution file (`cpp/0064-minimum-path-sum.cpp` in the NeetCode repo)

```cpp
class Solution{
    public:    
        void Helper(vector<vector<int>> & grid, vector<vector<int>> & dp, int i, int k){            
            int X = grid.size();            
            int Y = grid[0].size();            
            for(int i = 0; i < X; i++){                
                for(k = 0; k < Y; k++){                    
                    if((i - 1 >= 0) && (k - 1 >= 0)){
                        dp[i][k] = grid[i][k] + min(dp[i - 1][k], dp[i][k - 1]);             
                    }
                    else{
                        if(i - 1 >= 0){
                            dp[i][k] = grid[i][k] + dp[i - 1][k];
                        }                        
                        if(k - 1 >= 0){
                            dp[i][k] = grid[i][k] + dp[i][k - 1];
                        }
                    }
                }
            }   
            
        }    
        int minPathSum(vector<vector<int>>& grid){            
            vector<vector<int>> dp(grid.size(), vector<int>(grid[0].size()));            
            dp[0][0] = grid[0][0];            
            Helper(grid, dp, grid.size() - 1, grid[0].size() - 1);            
            return dp[grid.size() - 1][grid[0].size() - 1];        
        }
};
```
