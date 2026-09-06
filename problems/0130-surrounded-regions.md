# 130. Surrounded Regions

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/surrounded-regions/>  
- **NeetCode:** <https://neetcode.io/problems/surrounded-regions>  
- **Video:** <https://www.youtube.com/watch?v=9z2BunfoZ5Y>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

Only the **'O' regions that touch the border** can never be surrounded, because they have a path to the outside of the board.  
So instead of trying to find surrounded regions directly, we do the opposite:

1. **Mark all border-connected 'O' cells as “safe”** (temporary mark `'T'`).
2. Any remaining `'O'` is truly surrounded → flip it to `'X'`.
3. Convert the temporary `'T'` back to `'O'`.

```cpp
class Solution {
    int ROWS, COLS;

public:
    void solve(vector<vector<char>>& board) {
        ROWS = board.size();
        COLS = board[0].size();

        for (int r = 0; r < ROWS; r++) {
            if (board[r][0] == 'O') {
                capture(board, r, 0);
            }
            if (board[r][COLS - 1] == 'O') {
                capture(board, r, COLS - 1);
            }
        }

        for (int c = 0; c < COLS; c++) {
            if (board[0][c] == 'O') {
                capture(board, 0, c);
            }
            if (board[ROWS - 1][c] == 'O') {
                capture(board, ROWS - 1, c);
            }
        }

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (board[r][c] == 'O') {
                    board[r][c] = 'X';
                } else if (board[r][c] == 'T') {
                    board[r][c] = 'O';
                }
            }
        }
    }

private:
    void capture(vector<vector<char>>& board, int r, int c) {
        if (r < 0 || c < 0 || r >= ROWS ||
            c >= COLS || board[r][c] != 'O') {
            return;
        }
        board[r][c] = 'T';
        capture(board, r + 1, c);
        capture(board, r - 1, c);
        capture(board, r, c + 1);
        capture(board, r, c - 1);
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns of the $board$.

## 2. Breadth First Search

Same idea as DFS, but we use **BFS with a queue**.

- Any `'O'` that is connected to the **border** can "escape", so it should **NOT** be flipped.
- Start BFS from all border `'O'` cells and mark every reachable `'O'` as temporary `'T'` (safe).
- After that:
    - leftover `'O'` cells are fully surrounded → flip to `'X'`
    - `'T'` cells are safe → change back to `'O'`

```cpp
class Solution {
    int ROWS, COLS;
    vector<pair<int, int>> directions = {{1, 0}, {-1, 0},
                                         {0, 1}, {0, -1}};

public:
    void solve(vector<vector<char>>& board) {
        ROWS = board.size();
        COLS = board[0].size();

        capture(board);

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (board[r][c] == 'O') {
                    board[r][c] = 'X';
                } else if (board[r][c] == 'T') {
                    board[r][c] = 'O';
                }
            }
        }
    }

private:
    void capture(vector<vector<char>>& board) {
        queue<pair<int, int>> q;
        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if ((r == 0 || r == ROWS - 1 ||
                    c == 0 || c == COLS - 1) &&
                    board[r][c] == 'O') {
                    q.push({r, c});
                }
            }
        }
        while (!q.empty()) {
            auto [r, c] = q.front();
            q.pop();
            if (board[r][c] == 'O') {
                board[r][c] = 'T';
                for (auto& direction : directions) {
                    int nr = r + direction.first;
                    int nc = c + direction.second;
                    if (nr >= 0 && nr < ROWS &&
                        nc >= 0 && nc < COLS) {
                        q.push({nr, nc});
                    }
                }
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns of the $board$.

## 3. Disjoint Set Union

Treat every `'O'` cell as a node in a graph. Two `'O'` cells belong to the same region if they are **4-directionally connected**.

The key observation:

- Any region of `'O'` that touches the **border** is **safe** (it cannot be surrounded).
- Any region of `'O'` that does **not** touch the border is **captured** → should become `'X'`.

So we use **DSU (Union-Find)** to group connected `'O'` cells, and we create one extra **dummy node** that represents "connected to border".

- Union every border `'O'` with the dummy node.
- Union every `'O'` with its neighboring `'O'` cells.
- Finally, any cell **not connected** to the dummy node is surrounded → flip to `'X'`.

```cpp
class DSU {
    vector<int> Parent, Size;

public:
    DSU(int n) {
        Parent.resize(n + 1);
        Size.resize(n + 1);
        for (int i = 0; i <= n; i++) {
            Parent[i] = i;
            Size[i] = 1;
        }
    }

    int find(int node) {
        if (Parent[node] != node) {
            Parent[node] = find(Parent[node]);
        }
        return Parent[node];
    }

    bool unionNodes(int u, int v) {
        int pu = find(u), pv = find(v);
        if (pu == pv) return false;
        if (Size[pu] >= Size[pv]) {
            Size[pu] += Size[pv];
            Parent[pv] = pu;
        } else {
            Size[pv] += Size[pu];
            Parent[pu] = pv;
        }
        return true;
    }

    bool connected(int u, int v) {
        return find(u) == find(v);
    }
};

class Solution {
public:
    void solve(vector<vector<char>>& board) {
        int ROWS = board.size(), COLS = board[0].size();
        DSU dsu(ROWS * COLS + 1);
        vector<vector<int>> directions = {{1, 0}, {-1, 0},
                                          {0, 1}, {0, -1}};

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (board[r][c] != 'O') continue;
                if (r == 0 || c == 0 ||
                    r == ROWS - 1 || c == COLS - 1) {
                    dsu.unionNodes(ROWS * COLS, r * COLS + c);
                } else {
                    for (auto& dir : directions) {
                        int nr = r + dir[0], nc = c + dir[1];
                        if (board[nr][nc] == 'O') {
                            dsu.unionNodes(r * COLS + c, nr * COLS + nc);
                        }
                    }
                }
            }
        }

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (!dsu.connected(ROWS * COLS, r * COLS + c)) {
                    board[r][c] = 'X';
                }
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $m$ is the number of rows and $n$ is the number of columns of the $board$.

## Standalone solution file (`cpp/0130-surrounded-regions.cpp` in the NeetCode repo)

```cpp
/*
    Given a matrix, capture ('X') all regions that are surrounded ('O')

    Distinguish captured vs escaped, 'X' vs 'O' vs 'E'

    Time: O(m x n)
    Space: O(m x n)
*/

class Solution {
public:
    void solve(vector<vector<char>>& board) {
        int m = board.size();
        int n = board[0].size();
        
        // marking escaped cells along the border
        for (int i = 0; i < m; i++) {
            dfs(board,i,0,m,n);
            dfs(board,i,n-1,m,n);
        }
        
        for (int j = 0; j < n; j++) {
            dfs(board,0,j,m,n);
            dfs(board,m-1,j,m,n);
        }
        
        // flip cells to correct final states
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (board[i][j] == 'O') {
                    board[i][j] = 'X';
                }
                if (board[i][j] == 'E') {
                    board[i][j] = 'O';
                }
            }
        }
    }
private:
    void dfs(vector<vector<char>>& board, int i, int j, int m, int n) {
        if (i < 0 || i >= m || j < 0 || j >= n || board[i][j] != 'O') {
            return;
        }
        
        board[i][j] = 'E';
        
        dfs(board, i - 1, j, m, n);
        dfs(board, i + 1, j, m, n);
        dfs(board, i, j - 1, m, n);
        dfs(board, i, j + 1, m, n);
    }
};

/*
   BFS Solution
*/

class Solution {
private:
    int rows, cols;

    void bfs(int row, int col, vector<vector<char>>& board) {
        board[row][col] = 'E';
        queue<pair<int, int>> q;
        q.push({row, col});

        vector<pair<int, int>> directions = {{0, 1}, {1, 0}, {-1, 0}, {0, -1}};
        while (!q.empty()) {
            auto [r, c] = q.front();
            q.pop();
            for (const auto &direction : directions) {
                int newRow = r + direction.first;
                int newCol = c + direction.second;
                if (newRow < rows && newRow >= 0 && newCol < cols && newCol >= 0 && board[newRow][newCol] == 'O') {
                    board[newRow][newCol] = 'E';
                    q.push({newRow, newCol});
                }
            }
        }

    }

public:
    void solve(vector<vector<char>>& board) {
        rows = board.size();    
        cols = board[0].size();

        for (int row = 0; row < rows; ++row) {
            if (board[row][0] == 'O') bfs(row, 0, board);
            if (board[row][cols - 1] == 'O') bfs(row, cols - 1, board);
        }

        for (int col = 0; col < cols; ++col) {
            if (board[0][col] == 'O') bfs(0, col, board);
            if (board[rows - 1][col] == 'O') bfs(rows - 1, col, board);
        }

        for (int row = 0; row < rows; ++row) {
            for (int col = 0; col < cols; ++col) {
                if (board[row][col] == 'O') {
                    board[row][col] = 'X';
                }
                else if (board[row][col] == 'E') {
                    board[row][col] = 'O';
                }
            }
        }

    }
};
```
