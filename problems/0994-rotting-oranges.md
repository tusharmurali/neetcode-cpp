# 994. Rotting Oranges

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/rotting-oranges/>  
- **NeetCode:** <https://neetcode.io/problems/rotting-fruit>  
- **Video:** <https://www.youtube.com/watch?v=y704fEOx0s0>  
- **Video approach:** 1. Breadth First Search  

[← Back to index](../INDEX.md)

## 1. Breadth First Search ▶ video

This is a **multi-source BFS** problem.

All **rotten oranges (2)** start spreading rot **at the same time** to their neighboring fresh oranges (1).
Each BFS level represents **1 minute**.
If a fresh orange is reached, it becomes rotten in the next minute.

Key ideas:

- Start BFS from **all rotten oranges together**
- Count how many **fresh oranges** exist
- Each BFS layer = one unit of time
- If any fresh orange is left at the end → answer is `-1`

```cpp
class Solution {
public:
    int orangesRotting(vector<vector<int>>& grid) {
        queue<pair<int, int>> q;
        int fresh = 0;
        int time = 0;

        for (int r = 0; r < grid.size(); r++) {
            for (int c = 0; c < grid[0].size(); c++) {
                if (grid[r][c] == 1) {
                    fresh++;
                }
                if (grid[r][c] == 2) {
                    q.push({r, c});
                }
            }
        }

        vector<pair<int, int>> directions = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
        while (fresh > 0 && !q.empty()) {
            int length = q.size();
            for (int i = 0; i < length; i++) {
                auto curr = q.front();
                q.pop();
                int r = curr.first;
                int c = curr.second;

                for (const auto& dir : directions) {
                    int row = r + dir.first;
                    int col = c + dir.second;
                    if (row >= 0 && row < grid.size() &&
                        col >= 0 && col < grid[0].size() &&
                        grid[row][col] == 1) {
                        grid[row][col] = 2;
                        q.push({row, col});
                        fresh--;
                    }
                }
            }
            time++;
        }
        return fresh == 0 ? time : -1;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns in the $grid$.

## 2. Breadth First Search (No Queue)

This is still **BFS by levels**, but instead of using a queue, we simulate "minutes" with **grid marking**.

Think of each loop iteration as **1 minute**:

- Cells with value **2** are the oranges that are rotten _at the start of this minute_.
- Any fresh neighbor they rot during this minute is temporarily marked as **3** (meaning "will become rotten next minute").
- After scanning the whole grid, we convert all **3 → 2** to prepare for the next minute.

Why use `3`?

- To prevent a newly rotted orange from spreading in the **same minute** (which would incorrectly speed up time).

If during a minute **no fresh orange becomes 3**, but `fresh` still exists, then rot can't spread anymore → return `-1`.

```cpp
class Solution {
public:
    int orangesRotting(vector<vector<int>>& grid) {
        int ROWS = grid.size(), COLS = grid[0].size();
        int fresh = 0, time = 0;

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (grid[r][c] == 1) fresh++;
            }
        }

        vector<vector<int>> directions = {{0, 1}, {0, -1},
                                          {1, 0}, {-1, 0}};

        while (fresh > 0) {
            bool flag = false;
            for (int r = 0; r < ROWS; r++) {
                for (int c = 0; c < COLS; c++) {
                    if (grid[r][c] == 2) {
                        for (auto& d : directions) {
                            int row = r + d[0], col = c + d[1];
                            if (row >= 0 && col >= 0 &&
                                row < ROWS && col < COLS &&
                                grid[row][col] == 1) {
                                grid[row][col] = 3;
                                fresh--;
                                flag = true;
                            }
                        }
                    }
                }
            }

            if (!flag) return -1;

            for (int r = 0; r < ROWS; r++) {
                for (int c = 0; c < COLS; c++) {
                    if (grid[r][c] == 3) grid[r][c] = 2;
                }
            }

            time++;
        }

        return time;
    }
};
```

**Complexity**

- Time complexity: $O((m * n) ^ 2)$
- Space complexity: $O(1)$

> Where $m$ is the number of rows and $n$ is the number of columns in the $grid$.

## Standalone solution file (`cpp/0994-rotting-oranges.cpp` in the NeetCode repo)

```cpp
/*
    Given grid: 0 empty cell, 1 fresh orange, 2 rotten orange
    Return min # of minutes until no cell has a fresh orange

    BFS: rotten will contaminate neighbors first, then propagate out

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    int orangesRotting(vector<vector<int>>& grid) {
        int m = grid.size();
        int n = grid[0].size();
        
        // build initial set of rotten oranges
        queue<pair<int, int>> q;
        int fresh = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 2) {
                    q.push({i, j});
                } else if (grid[i][j] == 1) {
                    fresh++;
                }
            }
        }
        // mark the start of a minute
        q.push({-1, -1});
        
        int result = -1;
        
        // start rotting process via BFS
        while (!q.empty()) {
            int row = q.front().first;
            int col = q.front().second;
            q.pop();
            
            if (row == -1) {
                // finish 1 minute of processing, mark next minute
                result++;
                if (!q.empty()) {
                    q.push({-1, -1});
                }
            } else {
                // rotten orange, contaminate its neighbors
                for (int i = 0; i < dirs.size(); i++) {
                    int x = row + dirs[i][0];
                    int y = col + dirs[i][1];
                    
                    if (x < 0 || x >= m || y < 0 || y >= n) {
                        continue;
                    }
                    
                    if (grid[x][y] == 1) {
                        // contaminate
                        grid[x][y] = 2;
                        fresh--;
                        // this orange will now contaminate others
                        q.push({x, y});
                    }
                }
            }
        }
        
        if (fresh == 0) {
            return result;
        }
        return -1;
    }
private:
    vector<vector<int>> dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
};
```
