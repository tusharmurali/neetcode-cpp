# 36. Valid Sudoku

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/valid-sudoku/>  
- **NeetCode:** <https://neetcode.io/problems/valid-sudoku>  
- **Video:** <https://www.youtube.com/watch?v=TjFXEUCMqI8>  
- **Video approach:** 2. Hash Set (One Pass)  

[← Back to index](../INDEX.md)

## 1. Brute Force

A valid Sudoku board must follow three rules:

1. Each **row** can contain digits `1–9` at most once.
2. Each **column** can contain digits `1–9` at most once.
3. Each **3×3 box** can contain digits `1–9` at most once.

We can directly check all these conditions one by one.  
For every row, every column, and every 3×3 box, we keep a set of seen digits and make sure no number appears twice.  
If we ever find a duplicate in any of these three checks, the board is invalid.

```cpp
class Solution {
public:
    bool isValidSudoku(vector<vector<char>>& board) {
        for (int row = 0; row < 9; row++) {
            unordered_set<char> seen;
            for (int i = 0; i < 9; i++) {
                if (board[row][i] == '.') continue;
                if (seen.count(board[row][i])) return false;
                seen.insert(board[row][i]);
            }
        }

        for (int col = 0; col < 9; col++) {
            unordered_set<char> seen;
            for (int i = 0; i < 9; i++) {
                if (board[i][col] == '.') continue;
                if (seen.count(board[i][col])) return false;
                seen.insert(board[i][col]);
            }
        }

        for (int square = 0; square < 9; square++) {
            unordered_set<char> seen;
            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 3; j++) {
                    int row = (square / 3) * 3 + i;
                    int col = (square % 3) * 3 + j;
                    if (board[row][col] == '.') continue;
                    if (seen.count(board[row][col])) return false;
                    seen.insert(board[row][col]);
                }
            }
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Hash Set (One Pass) ▶ video

Instead of checking rows, columns, and 3×3 boxes separately, we can validate the entire Sudoku board in **one single pass**.  
For each cell, we check whether the digit has already appeared in:

1. the same **row**
2. the same **column**
3. the same **3×3 box**

We track these using three hash sets:

- `rows[r]` keeps digits seen in row `r`
- `cols[c]` keeps digits seen in column `c`
- `squares[(r // 3, c // 3)]` keeps digits in the 3×3 box

If a digit appears again in any of these places, the board is invalid.

```cpp
class Solution {
public:
    bool isValidSudoku(vector<vector<char>>& board) {
        unordered_map<int, unordered_set<char>> rows, cols;
        map<pair<int, int>, unordered_set<char>> squares;

        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                if (board[r][c] == '.') continue;

                pair<int, int> squareKey = {r / 3, c / 3};

                if (rows[r].count(board[r][c]) || cols[c].count(board[r][c]) || squares[squareKey].count(board[r][c])) {
                    return false;
                }

                rows[r].insert(board[r][c]);
                cols[c].insert(board[r][c]);
                squares[squareKey].insert(board[r][c]);
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Bitmask

Every digit from `1` to `9` can be represented using a single bit in an integer.  
For example, digit `1` uses bit `0`, digit `2` uses bit `1`, …, digit `9` uses bit `8`.  
This means we can track which digits have appeared in a row, column, or 3×3 box using just **one integer per row/column/box** instead of a hash set.

When we encounter a digit, we compute its bit position and check:

- if that bit is already set in the row → duplicate in row
- if that bit is already set in the column → duplicate in column
- if that bit is already set in the box → duplicate in box

If none of these checks fail, we “turn on” that bit to mark the digit as seen.  
This approach is both memory efficient and fast.

```cpp
class Solution {
public:
    bool isValidSudoku(vector<vector<char>>& board) {
        int rows[9] = {0};
        int cols[9] = {0};
        int squares[9] = {0};

        for (int r = 0; r < 9; ++r) {
            for (int c = 0; c < 9; ++c) {
                if (board[r][c] == '.') continue;

                int val = board[r][c] - '1';

                if ((rows[r] & (1 << val)) || (cols[c] & (1 << val)) ||
                    (squares[(r / 3) * 3 + (c / 3)] & (1 << val))) {
                    return false;
                }

                rows[r] |= (1 << val);
                cols[c] |= (1 << val);
                squares[(r / 3) * 3 + (c / 3)] |= (1 << val);
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0036-valid-sudoku.cpp` in the NeetCode repo)

```cpp
/*
    Determine if a 9x9 Sudoku board is valid (no repeats)

    Boolean matrices to store seen values. Check rows, cols, 3x3 sub-boxes

    Time: O(cnt^2)
    Space: O(cnt^2)
*/

class Solution {
public:
    bool isValidSudoku(vector<vector<char>>& board) {
        const int cnt = 9;
        bool row[cnt][cnt] = {false};
        bool col[cnt][cnt] = {false};
        bool sub[cnt][cnt] = {false};
        
        for(int r = 0; r < cnt; ++r){
            for(int c = 0; c < cnt; ++c){
                if(board[r][c] == '.')
                    continue; // if not number pass
                
                int idx = board[r][c] - '0' - 1; //char to num idx
                int area = (r/3) * 3 + (c/3);
                
                //if number already exists
                if(row[r][idx] || col[c][idx] || sub[area][idx]){
                    return false;
                }
                
                row[r][idx] = true;
                col[c][idx] = true;
                sub[area][idx] = true;
            }
        }
        return true;
    }
};
```
