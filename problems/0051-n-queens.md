# 51. N Queens

- **Difficulty:** Hard  
- **Pattern:** Backtracking  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/n-queens/>  
- **NeetCode:** <https://neetcode.io/problems/n-queens>  
- **Video:** <https://www.youtube.com/watch?v=Ph95IHmRp5M>  

[← Back to index](../INDEX.md)

## 1. Backtracking

The goal is to place **one queen in each row** such that no two queens attack each other.

Key observations:

- A queen can attack **vertically**, **diagonally left**, and **diagonally right**
- Since we place queens **row by row from top to bottom**, we only need to check rows **above** the current row
- If a position is safe, we place a queen and move to the next row
- If we reach a dead end, we **backtrack** by removing the last queen and trying another column

This is a classic **backtracking + constraint checking** problem.

```cpp
class Solution {
public:
    vector<vector<string>> solveNQueens(int n) {
        vector<vector<string>> res;
        vector<string> board(n, string(n, '.'));
        backtrack(0, board, res);
        return res;
    }

    void backtrack(int r, vector<string>& board, vector<vector<string>>& res) {
        if (r == board.size()) {
            res.push_back(board);
            return;
        }
        for (int c = 0; c < board.size(); c++) {
            if (isSafe(r, c, board)) {
                board[r][c] = 'Q';
                backtrack(r + 1, board, res);
                board[r][c] = '.';
            }
        }
    }

    bool isSafe(int r, int c, vector<string>& board) {
        for (int i = r - 1; i >= 0; i--) {
            if (board[i][c] == 'Q') return false;
        }
        for (int i = r - 1, j = c - 1; i >= 0 && j >= 0; i--, j--) {
            if (board[i][j] == 'Q') return false;
        }
        for (int i = r - 1, j = c + 1; i >= 0 && j < board.size(); i--, j++) {
            if (board[i][j] == 'Q') return false;
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n!)$
- Space complexity: $O(n ^ 2)$

## 2. Backtracking (Hash Set)

Instead of checking the board every time to see if a queen is safe, we **remember the attacked positions** using hash sets.

For any queen at position `(row, col)`:

- **Column conflict** → same `col`
- **Positive diagonal conflict** → same `(row + col)`
- **Negative diagonal conflict** → same `(row - col)`

By storing these in sets, we can check whether a position is safe in **O(1)** time.

We still place **one queen per row**, move row by row, and backtrack when a placement leads to a conflict.

```cpp
class Solution {
public:
    unordered_set<int> col;
    unordered_set<int> posDiag;
    unordered_set<int> negDiag;
    vector<vector<string>> res;

    vector<vector<string>> solveNQueens(int n) {
        vector<string> board(n, string(n, '.'));

        backtrack(0, n, board);
        return res;
    }

private:
    void backtrack(int r, int n, vector<string>& board) {
        if (r == n) {
            res.push_back(board);
            return;
        }

        for (int c = 0; c < n; c++) {
            if (col.count(c) || posDiag.count(r + c) ||
                negDiag.count(r - c)) {
                continue;
            }

            col.insert(c);
            posDiag.insert(r + c);
            negDiag.insert(r - c);
            board[r][c] = 'Q';

            backtrack(r + 1, n, board);

            col.erase(c);
            posDiag.erase(r + c);
            negDiag.erase(r - c);
            board[r][c] = '.';
        }
    }
};
```

**Complexity**

- Time complexity: $O(n!)$
- Space complexity: $O(n ^ 2)$

## 3. Backtracking (Visited Array)

This approach is the **array-based version** of the hash-set solution.

Instead of using sets, we use **boolean arrays** to mark whether a column or diagonal is already occupied by a queen.  
This works because:

- Columns are limited to `n`
- Diagonals can be mapped to indices using math

For a queen at position `(row, col)`:

- **Column index** → `col`
- **Positive diagonal ( / )** → `row + col`
- **Negative diagonal ( \ )** → `row - col + n` (shifted to avoid negative index)

If any of these positions are already marked `True`, placing a queen there would cause a conflict.

We place queens **row by row**, and backtrack when no safe column is available.

```cpp
class Solution {
public:
    vector<string> board;
    vector<bool> col, posDiag, negDiag;
    vector<vector<string>> res;

    vector<vector<string>> solveNQueens(int n) {
        col.resize(n, false);
        posDiag.resize(2 * n, false);
        negDiag.resize(2 * n, false);
        board.resize(n, string(n, '.'));

        backtrack(0, n);
        return res;
    }

    void backtrack(int r, int n) {
        if (r == n) {
            res.push_back(board);
            return;
        }
        for (int c = 0; c < n; c++) {
            if (col[c] || posDiag[r + c] || negDiag[r - c + n]) {
                continue;
            }
            col[c] = true;
            posDiag[r + c] = true;
            negDiag[r - c + n] = true;
            board[r][c] = 'Q';

            backtrack(r + 1, n);

            col[c] = false;
            posDiag[r + c] = false;
            negDiag[r - c + n] = false;
            board[r][c] = '.';
        }
    }
};
```

**Complexity**

- Time complexity: $O(n!)$
- Space complexity: $O(n ^ 2)$

## 4. Backtracking (Bit Mask)

This is the **most optimized backtracking approach** for the N-Queens problem.

Instead of using arrays or hash sets to track occupied columns and diagonals, we use **bit masks (integers)**.  
Each bit represents whether a column or diagonal is already occupied.

Why this works well:

- Integers allow **O(1)** checks using bitwise operations
- Uses **very little memory**
- Faster than arrays/sets in practice

For a queen placed at position `(row, col)`:

- **Column mask** → bit `col`
- **Positive diagonal (`/`)** → bit `(row + col)`
- **Negative diagonal (`\`)** → bit `(row - col + n)`

If any of these bits are already set, placing a queen there causes a conflict.

We still place queens **row by row**, but conflict checks are done using bitwise AND.

```cpp
class Solution {
public:
    int col = 0, posDiag = 0, negDiag = 0;
    vector<string> board;
    vector<vector<string>> res;

    vector<vector<string>> solveNQueens(int n) {
        board.resize(n, string(n, '.'));

        backtrack(0, n);
        return res;
    }

    void backtrack(int r, int n) {
        if (r == n) {
            res.push_back(board);
            return;
        }
        for (int c = 0; c < n; c++) {
            if ((col & (1 << c)) || (posDiag & (1 << (r + c)))
                 || (negDiag & (1 << (r - c + n)))) {
                continue;
            }
            col ^= (1 << c);
            posDiag ^= (1 << (r + c));
            negDiag ^= (1 << (r - c + n));
            board[r][c] = 'Q';

            backtrack(r + 1, n);

            col ^= (1 << c);
            posDiag ^= (1 << (r + c));
            negDiag ^= (1 << (r - c + n));
            board[r][c] = '.';
        }
    }
};
```

**Complexity**

- Time complexity: $O(n!)$
- Space complexity: $O(n ^ 2)$

## Standalone solution file (`cpp/0051-n-queens.cpp` in the NeetCode repo)

```cpp
/*
    N-Queens: place n queens such that no 2 queens atk each other, return all soln's

    Place queens per row, try all possibilities & validate for further rows, backtrack

    Time: O(n!)
    Space: O(n^2)
*/

class Solution {
private:
    unordered_set<int> cols;     //for Columns
    unordered_set<int> negDiag;  //for negative diagnals R-C
    unordered_set<int> posDiag;  //for positive diagnals R+C
    
    void backtrack(int n, int row, vector<vector<string>>& res, vector<string>& board){
        if(row==n){
            res.push_back(board);
            return ; 
        }
        
        for(int col = 0; col < n; col++){   //Shifting through each col
            if( cols.find(col) != cols.end() or //if queen alread placed in this col
                negDiag.find(row - col) != negDiag.end() or //if queen in negDiag
                posDiag.find(row + col) != posDiag.end()    //if queen in posDiag
              )
                continue;
            
            cols.insert(col);
            negDiag.insert(row - col);
            posDiag.insert(row + col);
            board[row][col] = 'Q';
            
            backtrack(n, row +1, res, board);
            
            cols.erase(col);
            negDiag.erase(row - col);
            posDiag.erase(row + col);
            board[row][col] = '.';
        }
    }
   
public:
    vector<vector<string>> solveNQueens(int n) {
        vector<vector<string>> res;
        vector<string> board(n, string(n,'.'));
        backtrack(n, 0, res, board);
        return res;
    }
};
```
