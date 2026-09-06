# 52. N Queens II

- **Difficulty:** Hard  
- **Pattern:** Backtracking  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/n-queens-ii/>  
- **NeetCode:** <https://neetcode.io/problems/n-queens-ii>  
- **Video:** <https://www.youtube.com/watch?v=nalYyLZgvCY>  
- **Video approach:** 2. Backtracking (Hash Set)  

[← Back to index](../INDEX.md)

## 1. Backtracking

We place queens row by row, ensuring each placement is valid before moving to the next row. For each column in the current row, we check if placing a queen there would conflict with any queen already placed above. A queen attacks along its column and both diagonals, so we scan upward in those three directions. If no conflict exists, we place the queen and recurse to the next row. When we successfully place queens in all rows, we have found a valid configuration.

```cpp
class Solution {
public:
    int totalNQueens(int n) {
        int res = 0;
        vector<string> board(n, string(n, '.'));
        backtrack(0, board, res);
        return res;
    }

    void backtrack(int r, vector<string>& board, int& res) {
        if (r == board.size()) {
            res++;
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

## 2. Backtracking (Hash Set) ▶ video

Instead of scanning the board to check for conflicts, we can track which columns and diagonals are already occupied using hash sets. Each column has a unique index. For diagonals, cells on the same positive diagonal (bottom-left to top-right) share the same value of `row + col`, while cells on the same negative diagonal (top-left to bottom-right) share the same value of `row - col`. By checking set membership, we determine in constant time whether a position is under attack.

```cpp
class Solution {
public:
    unordered_set<int> col;
    unordered_set<int> posDiag;
    unordered_set<int> negDiag;

    int totalNQueens(int n) {
        int res = 0;
        backtrack(0, n, res);
        return res;
    }

private:
    void backtrack(int r, int n, int& res) {
        if (r == n) {
            res++;
            return;
        }

        for (int c = 0; c < n; c++) {
            if (col.count(c) || posDiag.count(r + c) || negDiag.count(r - c)) {
                continue;
            }

            col.insert(c);
            posDiag.insert(r + c);
            negDiag.insert(r - c);

            backtrack(r + 1, n, res);

            col.erase(c);
            posDiag.erase(r + c);
            negDiag.erase(r - c);
        }
    }
};
```

**Complexity**

- Time complexity: $O(n!)$
- Space complexity: $O(n)$

## 3. Backtracking (Boolean Array)

Hash sets have some overhead for insertions and lookups. Since the board size is fixed and the range of diagonal indices is bounded, we can use boolean arrays instead. An array of size `n` tracks occupied columns, and arrays of size `2n` track the positive and negative diagonals. For negative diagonals, we add `n` to the index to ensure non-negative array indices. This gives us the same constant-time conflict checking with lower overhead.

```cpp
class Solution {
public:
    vector<string> board;
    vector<bool> col, posDiag, negDiag;

    int totalNQueens(int n) {
        col.resize(n, false);
        posDiag.resize(2 * n, false);
        negDiag.resize(2 * n, false);

        int res = 0;
        backtrack(0, n, res);
        return res;
    }

    void backtrack(int r, int n, int& res) {
        if (r == n) {
            res++;
            return;
        }
        for (int c = 0; c < n; c++) {
            if (col[c] || posDiag[r + c] || negDiag[r - c + n]) {
                continue;
            }
            col[c] = true;
            posDiag[r + c] = true;
            negDiag[r - c + n] = true;

            backtrack(r + 1, n, res);

            col[c] = false;
            posDiag[r + c] = false;
            negDiag[r - c + n] = false;
        }
    }
};
```

**Complexity**

- Time complexity: $O(n!)$
- Space complexity: $O(n)$

## 4. Backtracking (Bit Mask)

Bit manipulation offers the most compact representation for tracking occupied columns and diagonals. We use three integers as bitmasks: each bit in `col` represents whether that column is occupied, and similarly for the two diagonal masks. Checking if a position is attacked becomes a single bitwise AND operation. Setting and unsetting bits is done with XOR. This approach is both space-efficient and cache-friendly.

```cpp
class Solution {
public:
    int col = 0, posDiag = 0, negDiag = 0;
    vector<string> board;

    int totalNQueens(int n) {
        int res = 0;
        backtrack(0, n, res);
        return res;
    }

    void backtrack(int r, int n, int& res) {
        if (r == n) {
            res++;
            return;
        }
        for (int c = 0; c < n; c++) {
            if ((col & (1 << c)) || (posDiag & (1 << (r + c))) ||
                (negDiag & (1 << (r - c + n)))) {
                continue;
            }
            col ^= (1 << c);
            posDiag ^= (1 << (r + c));
            negDiag ^= (1 << (r - c + n));

            backtrack(r + 1, n, res);

            col ^= (1 << c);
            posDiag ^= (1 << (r + c));
            negDiag ^= (1 << (r - c + n));
        }
    }
};
```

**Complexity**

- Time complexity: $O(n!)$
- Space complexity: $O(n)$ for recursion stack.

## Standalone solution file (`cpp/0052-n-queens-ii.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int queen[9];
    bool check(int &r,int &c,int n){
        for(int i=0;i<r;i++){
            // here we have to check from before rows any queen(queen[i]) is placed to attk the cur level queen;
            int pre_row=i; // previous row
            int pre_col=queen[i]; // previous col is stored in queen[i]
            // checking for col collison as rows cant be && and for diagonal attk
            if(pre_col==c or abs(r-pre_row)==abs(c-pre_col)) return false;
        }
        return true;
    }
    int bt(int level,int n){
        // base conditon
        
        if(level==n) return 1;
        // return 1 as u made a board and placing queens from 0 to n-1 so u came out of board
        
        int ans=0;
        // exploring choices and computation
        for(int col=0;col<n;col++){
            if(check(level,col,n)){
                // check
                queen[level]=col;
                // move
                ans+=bt(level+1,n);
                queen[level]=-1;
            }
        }
        // return count of ways to place queen from this row to n-1/ last row
        return ans;
    }
    int totalNQueens(int n) {
        memset(queen,-1,sizeof(queen));
        return bt(0,n);
    }
};
```
