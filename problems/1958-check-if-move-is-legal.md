# 1958. Check if Move Is Legal

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/check-if-move-is-legal/>  
- **NeetCode:** <https://neetcode.io/problems/check-if-move-is-legal>  
- **Video:** <https://www.youtube.com/watch?v=KxK33AcQZpQ>  
- **Video approach:** 1. Iteration - I (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Iteration - I ▶ video

This problem simulates an Othello/Reversi move validation. A move is legal if placing a piece creates a "good line" in any of the 8 directions (horizontal, vertical, or diagonal). A good line starts with the placed piece, has one or more opponent pieces in between, and ends with another piece of the same color. The total length must be at least 3.

```cpp
class Solution {
public:
    bool checkMove(vector<vector<char>>& board, int rMove, int cMove, char color) {
        int ROWS = board.size(), COLS = board[0].size();
        vector<vector<int>> direction = {{1, 0}, {-1, 0}, {0, 1}, {0, -1},
                                         {1, 1}, {-1, -1}, {1, -1}, {-1, 1}};

        board[rMove][cMove] = color;

        for (auto& d : direction) {
            if (legal(board, rMove, cMove, color, d)) {
                return true;
            }
        }
        return false;
    }

private:
    bool legal(vector<vector<char>>& board, int row, int col, char color, vector<int>& direc) {
        int ROWS = board.size(), COLS = board[0].size();
        int dr = direc[0], dc = direc[1];
        row += dr;
        col += dc;
        int length = 1;

        while (row >= 0 && row < ROWS && col >= 0 && col < COLS) {
            length++;
            if (board[row][col] == '.') {
                return false;
            }
            if (board[row][col] == color) {
                return length >= 3;
            }
            row += dr;
            col += dc;
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 2. Iteration - II

This is a more compact implementation of the same logic. Instead of storing directions as pairs, we use a single array where consecutive elements form direction pairs. This reduces memory usage slightly and makes the iteration more streamlined.

```cpp
class Solution {
public:
    bool checkMove(vector<vector<char>>& board, int rMove, int cMove, char color) {
        int ROWS = board.size(), COLS = board[0].size();
        int direction[10] = {0, 1, 0, -1, 0, 1, 1, -1, -1, 1};

        board[rMove][cMove] = color;

        for (int d = 0; d < 9; ++d) {
            int row = rMove, col = cMove;
            for (int length = 1; ; ++length) {
                row += direction[d];
                col += direction[d + 1];

                if (row < 0 || col < 0 || row >= ROWS || col >= COLS || board[row][col] == '.')
                    break;
                if (board[row][col] == color) {
                    if (length > 1)
                        return true;
                    break;
                }
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/1958-check-if-move-is-legal.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    bool checkMove(vector<vector<char>>& board, int rMove, int cMove, char color) {
        const int ROWS = board.size(), COLS = board[0].size();
        int direction[8][4] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1},
                               {1, 1}, {-1, -1}, {1, -1}, {-1, 1}};
        board[rMove][cMove] = color;
        
        function<bool(int, int, char, int[])> legal = [&] (int row, int col, char color, int direc[]) -> bool {
            int dr = direc[0], dc = direc[1];
            row = row + dr;
            col = col + dc;
            int length = 1;
            
            while(0 <= row && row < ROWS && 0 <= col && col < COLS) {
                length += 1;
                if(board[row][col] == '.') return false;
                if(board[row][col] == color)
                    return length >= 3;
                row = row + dr;
                col = col + dc;
            }
            return false;
        };
        
        for(auto& d: direction)
            if(legal(rMove, cMove, color, d)) return true;
        return false;
    }
};
```
