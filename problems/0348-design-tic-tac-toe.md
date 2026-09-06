# 348. Design Tic-Tac-Toe

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/design-tic-tac-toe/>  
- **NeetCode:** <https://neetcode.io/problems/design-tic-tac-toe>  

[← Back to index](../INDEX.md)

## 1. Optimized Brute Force

In Tic-Tac-Toe, a player wins by filling an entire row, column, or diagonal. After each move, we only need to check if that specific move creates a winning condition. Instead of checking the entire board, we focus on the row and column affected by the move, and check the diagonals only if the move is on one of them.

```cpp
class TicTacToe {
public:
    vector<vector<int>> board;
    int n;

    TicTacToe(int n) {
        board.assign(n, vector<int>(n, 0));
        this->n = n;
    }

    int move(int row, int col, int player) {
        board[row][col] = player;
        if (checkCol(col, player) ||
            checkRow(row, player) ||
            (row == col && checkDiagonal(player)) ||
            (row == n - col - 1 && checkAntiDiagonal(player))) {
            return player;
        }
        // No one wins
        return 0;
    }

    bool checkDiagonal(int player) {
        for (int row = 0; row < n; row++) {
            if (board[row][row] != player) return false;
        }
        return true;
    }

    bool checkAntiDiagonal(int player) {
        for (int row = 0; row < n; row++) {
            if (board[row][n - row - 1] != player) return false;
        }
        return true;
    }

    bool checkCol(int col, int player) {
        for (int row = 0; row < n; row++) {
            if (board[row][col] != player) return false;
        }
        return true;
    }

    bool checkRow(int row, int player) {
        for (int col = 0; col < n; col++) {
            if (board[row][col] != player) return false;
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n^2)$

> Where $n$ is the size of the Tic-Tac-Toe board.

## 2. Optimized Approach

Rather than storing the entire board and checking all cells in a row, column, or diagonal after each move, we can maintain running counts. By using `+1` for player 1 and `-1` for player 2, we can track the cumulative sum for each row, column, and both diagonals. A player wins when any of these sums reaches `+n` or `-n`, indicating that all `n` cells in that line belong to the same player.

```cpp
class TicTacToe {
public:
    vector<int> rows;
    vector<int> cols;
    int diagonal;
    int antiDiagonal;

    TicTacToe(int n) {
        rows.assign(n, 0);
        cols.assign(n, 0);
        diagonal = 0;
        antiDiagonal = 0;
    }

    int move(int row, int col, int player) {
        int currentPlayer = (player == 1) ? 1 : -1;

        // update currentPlayer in rows and cols arrays
        rows[row] += currentPlayer;
        cols[col] += currentPlayer;

        // update diagonal
        if (row == col) {
            diagonal += currentPlayer;
        }

        // update anti diagonal
        if (col == (cols.size() - row - 1)) {
            antiDiagonal += currentPlayer;
        }

        int n = rows.size();
        // check if the current player wins
        if (abs(rows[row]) == n ||
            abs(cols[col]) == n ||
            abs(diagonal) == n ||
            abs(antiDiagonal) == n) {
            return player;
        }

        // No one wins
        return 0;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(n)$

> Where $n$ is the size of the Tic-Tac-Toe board.
