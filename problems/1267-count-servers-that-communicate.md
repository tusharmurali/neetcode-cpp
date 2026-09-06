# 1267. Count Servers that Communicate

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/count-servers-that-communicate/>  
- **NeetCode:** <https://neetcode.io/problems/count-servers-that-communicate>  
- **Video:** <https://www.youtube.com/watch?v=meTbkgqNNYM>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A server can communicate if there is at least one other server in the same row or column. For each server, we can directly check its entire row and column to see if any other server exists. If we find at least one, this server counts toward our result.

```cpp
class Solution {
public:
    int countServers(vector<vector<int>>& grid) {
        int m = grid.size(), n = grid[0].size();
        int res = 0;

        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (grid[r][c] == 0) continue;

                bool found = false;
                for (int col = 0; col < n; col++) {
                    if (col != c && grid[r][col] == 1) {
                        found = true;
                        break;
                    }
                }

                if (!found) {
                    for (int row = 0; row < m; row++) {
                        if (row != r && grid[row][c] == 1) {
                            found = true;
                            break;
                        }
                    }
                }

                if (found) res++;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n ^ 2)$
- Space complexity: $O(1)$

> Where $m$ is the number of rows and $n$ is the number of columns of the given matrix $grid$.

## 2. Iteration

Instead of checking each server's row and column individually, we can precompute the count of servers in each row and column. A server can communicate if there is more than one server in its row or more than one server in its column. This allows us to determine each server's status in constant time after the preprocessing step.

```cpp
class Solution {
public:
    int countServers(vector<vector<int>>& grid) {
        int ROWS = grid.size(), COLS = grid[0].size();
        vector<int> row_cnt(ROWS, 0), col_cnt(COLS, 0);

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (grid[r][c] == 1) {
                    row_cnt[r]++;
                    col_cnt[c]++;
                }
            }
        }

        int res = 0;
        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (grid[r][c] == 1 && max(row_cnt[r], col_cnt[c]) > 1) {
                    res++;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m + n)$

> Where $m$ is the number of rows and $n$ is the number of columns of the given matrix $grid$.

## 3. Iteration (Space Optimized)

We can avoid using extra arrays by processing rows and columns separately and using the grid itself to mark processed servers. First, we process all rows with multiple servers and mark those servers. Then, we process columns and only count unmarked servers in columns with multiple servers. The marking prevents double counting servers that belong to both a communicating row and column.

```cpp
class Solution {
public:
    int countServers(vector<vector<int>>& grid) {
        int res = 0;
        int ROWS = grid.size(), COLS = grid[0].size();

        // Rows
        for (int r = 0; r < ROWS; r++) {
            int rowSum = accumulate(grid[r].begin(), grid[r].end(), 0);
            if (rowSum <= 1) continue;
            res += rowSum;
            for (int c = 0; c < COLS; c++) {
                if (grid[r][c] == 1) grid[r][c] = -1; // Mark
            }
        }

        // Cols
        for (int c = 0; c < COLS; c++) {
            int colSum = 0, unmarked = 0;
            for (int r = 0; r < ROWS; r++) {
                colSum += abs(grid[r][c]);
                if (grid[r][c] > 0) unmarked++;
                else if (grid[r][c] < 0) grid[r][c] = 1; // Unmark
            }
            if (colSum >= 2) res += unmarked;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(1)$

> Where $m$ is the number of rows and $n$ is the number of columns of the given matrix $grid$.
