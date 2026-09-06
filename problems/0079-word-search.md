# 79. Word Search

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/word-search/>  
- **NeetCode:** <https://neetcode.io/problems/search-for-word>  
- **Video:** <https://www.youtube.com/watch?v=pfiQ_PS1g8E>  
- **Video approach:** 1. Backtracking (Hash Set)  

[← Back to index](../INDEX.md)

## 1. Backtracking (Hash Set) ▶ video

We need to check if the word can be formed by walking **up/down/left/right** on the grid, using **each cell at most once** in the same path.

So for every cell, we try to start the word there:

- If the current cell matches the current character, we move to its 4 neighbors for the next character.
- While exploring, we mark the cell as **visited** (in a hash set) so we don't reuse it in the same path.
- If a path fails, we **undo (backtrack)** the visit and try other directions.

If we ever match all characters, we return `true` (found the word).

```cpp
class Solution {
public:
    int ROWS, COLS;
    set<pair<int, int>> path;

    bool exist(vector<vector<char>>& board, string word) {
        ROWS = board.size();
        COLS = board[0].size();

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (dfs(board, word, r, c, 0)) {
                    return true;
                }
            }
        }
        return false;
    }

    bool dfs(vector<vector<char>>& board, string word, int r, int c, int i) {
        if (i == word.length()) {
            return true;
        }

        if (r < 0 || c < 0 || r >= ROWS || c >= COLS ||
            board[r][c] != word[i] || path.count({r, c})) {
            return false;
        }

        path.insert({r, c});
        bool res = dfs(board, word, r + 1, c, i + 1) ||
                   dfs(board, word, r - 1, c, i + 1) ||
                   dfs(board, word, r, c + 1, i + 1) ||
                   dfs(board, word, r, c - 1, i + 1);
        path.erase({r, c});

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * 4 ^ n)$
- Space complexity: $O(n)$

> Where $m$ is the number of cells in the $board$ and $n$ is the length of the $word$.

## 2. Backtracking (Visited Array)

We try to form the word by **walking through adjacent cells** (up, down, left, right) in the grid.
Each cell can be used **only once in the current path**, so we keep a `visited` matrix to mark cells that are already part of the path.

From every cell, we attempt to match the word starting at index `0`.
If at any point the character doesn't match, goes out of bounds, or the cell is already visited, we stop that path.
If all characters are matched successfully, the word exists in the grid and we return `true`.

```cpp
class Solution {
public:
    int ROWS, COLS;
    vector<vector<bool>> visited;

    bool exist(vector<vector<char>>& board, string word) {
        ROWS = board.size();
        COLS = board[0].size();
        visited = vector<vector<bool>>(ROWS, vector<bool>(COLS, false));

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (dfs(board, word, r, c, 0)) {
                    return true;
                }
            }
        }
        return false;
    }

    bool dfs(vector<vector<char>>& board, string word, int r, int c, int i) {
        if (i == word.length()) {
            return true;
        }

        if (r < 0 || c < 0 || r >= ROWS || c >= COLS ||
            board[r][c] != word[i] || visited[r][c]) {
            return false;
        }

        visited[r][c] = true;
        bool res = dfs(board, word, r + 1, c, i + 1) ||
                   dfs(board, word, r - 1, c, i + 1) ||
                   dfs(board, word, r, c + 1, i + 1) ||
                   dfs(board, word, r, c - 1, i + 1);
        visited[r][c] = false;

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * 4 ^ n)$
- Space complexity: $O(n)$

> Where $m$ is the number of cells in the $board$ and $n$ is the length of the $word$.

## 3. Backtracking (Optimal)

We want to check if the word can be formed by moving **up/down/left/right** in the grid, using each cell **at most once** in a single path.

Instead of keeping a separate `visited` matrix (extra space), we temporarily **mark the current cell as used** by replacing its character with a special value (like `'#'`).
This means:

- If we ever see `'#'`, we know this cell is already in our current path → we can't reuse it.
- After exploring from that cell, we **restore** the original character (this is the "backtrack" step), so other paths can use it.

So the idea is:

- Try every cell as a starting point.
- Do `DFS` to match the word character by character.
- Mark → explore neighbors → unmark.

```cpp
class Solution {
public:
    int ROWS, COLS;

    bool exist(vector<vector<char>>& board, string word) {
        ROWS = board.size();
        COLS = board[0].size();

        for (int r = 0; r < ROWS; r++) {
            for (int c = 0; c < COLS; c++) {
                if (dfs(board, word, r, c, 0)) {
                    return true;
                }
            }
        }
        return false;
    }

    bool dfs(vector<vector<char>>& board, string word, int r, int c, int i) {
        if (i == word.size()) {
            return true;
        }
        if (r < 0 || c < 0 || r >= ROWS || c >= COLS ||
            board[r][c] != word[i] || board[r][c] == '#') {
            return false;
        }

        board[r][c] = '#';
        bool res = dfs(board, word, r + 1, c, i + 1) ||
                   dfs(board, word, r - 1, c, i + 1) ||
                   dfs(board, word, r, c + 1, i + 1) ||
                   dfs(board, word, r, c - 1, i + 1);
        board[r][c] = word[i];
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * 4 ^ n)$
- Space complexity: $O(n)$

> Where $m$ is the number of cells in the $board$ and $n$ is the length of the $word$.

## Standalone solution file (`cpp/0079-word-search.cpp` in the NeetCode repo)

```cpp
/*
    Given a char board & a word, return true if word exists in the grid

    DFS traversal, set visited cells to '#', search in 4 directions, backtrack

    Time: O(n x 3^l) -> n = # of cells, l = length of word
    Space: O(l)
*/

class Solution {
public:
    bool exist(vector<vector<char>>& board, string word) {
        int m = board.size();
        int n = board[0].size();
        
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (board[i][j] == word[0]) {
                    if (dfs(board, word, 0, i, j, m, n)) {
                        return true;
                    }
                }
            }
        }
        
        return false;
    }
private:
    bool dfs(vector<vector<char>>& board, string word,
        int index, int i, int j, int m, int n) {
        
        if (i < 0 || i >= m || j < 0 || j >= n || board[i][j] != word[index]) {
            return false;
        }
        if (index == word.size() - 1) {
            return true;
        }
        
        board[i][j] = '#';
        
        if (dfs(board, word, index + 1, i - 1, j, m, n)
            || dfs(board, word, index + 1, i + 1, j, m, n)
            || dfs(board, word, index + 1, i, j - 1, m, n)
            || dfs(board, word, index + 1, i, j + 1, m, n)) {
            return true;
        }
        
        board[i][j] = word[index];
        return false;
    }
};
```
