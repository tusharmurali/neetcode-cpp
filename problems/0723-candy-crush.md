# 723. Candy Crush

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/candy-crush/>  
- **NeetCode:** <https://neetcode.io/problems/candy-crush>  

[← Back to index](../INDEX.md)

## 1. Separate Steps: Find, Crush, Drop

We simulate the candy crush game by repeatedly performing three operations: find all candies that need to be crushed (three or more adjacent same-colored candies horizontally or vertically), crush them by setting their values to zero, and then drop remaining candies down to fill the gaps. We repeat this cycle until no more candies can be crushed.

```cpp
class Solution {
    int m, n;

    set<pair<int, int>> find(vector<vector<int>>& board) {
        set<pair<int, int>> crushedSet;

        // Check vertically adjacent candies
        for (int r = 1; r < m - 1; r++) {
            for (int c = 0; c < n; c++) {
                if (board[r][c] == 0) {
                    continue;
                }
                if (board[r][c] == board[r - 1][c] && board[r][c] == board[r + 1][c]) {
                    crushedSet.insert({r, c});
                    crushedSet.insert({r - 1, c});
                    crushedSet.insert({r + 1, c});
                }
            }
        }

        // Check horizontally adjacent candies
        for (int r = 0; r < m; r++) {
            for (int c = 1; c < n - 1; c++) {
                if (board[r][c] == 0) {
                    continue;
                }
                if (board[r][c] == board[r][c - 1] && board[r][c] == board[r][c + 1]) {
                    crushedSet.insert({r, c});
                    crushedSet.insert({r, c - 1});
                    crushedSet.insert({r, c + 1});
                }
            }
        }

        return crushedSet;
    }

    void crush(vector<vector<int>>& board, set<pair<int, int>>& crushedSet) {
        for (const auto& p : crushedSet) {
            int r = p.first;
            int c = p.second;
            board[r][c] = 0;
        }
    }

    void drop(vector<vector<int>>& board) {
        for (int c = 0; c < n; c++) {
            int lowestZero = -1;

            // Iterate over each column
            for (int r = m - 1; r >= 0; r--) {
                if (board[r][c] == 0) {
                    lowestZero = max(lowestZero, r);
                } else if (lowestZero >= 0) {
                    int temp = board[r][c];
                    board[r][c] = board[lowestZero][c];
                    board[lowestZero][c] = temp;
                    lowestZero--;
                }
            }
        }
    }

public:
    vector<vector<int>> candyCrush(vector<vector<int>>& board) {
        m = board.size();
        n = board[0].size();

        set<pair<int, int>> crushedSet = find(board);
        while (!crushedSet.empty()) {
            crush(board, crushedSet);
            drop(board);
            crushedSet = find(board);
        }

        return board;
    }
};
```

**Complexity**

- Time complexity: $O(m^2 \cdot n^2)$
- Space complexity: $O(m \cdot n)$

> Where $m × n$ is the size of the grid `board`

## 2. In-place Modification

Instead of using a separate set to track crushed candies, we can mark them in-place by negating their values. This allows us to identify candies to crush while still being able to check for matching (using absolute values). After marking, we convert all negative values to `0`. This reduces space usage compared to maintaining a separate set.

```cpp
class Solution {
    int m, n;

    bool findAndCrush(vector<vector<int>>& board) {
        bool complete = true;

        // Check vertically adjacent candies
        for (int r = 1; r < m - 1; r++) {
            for (int c = 0; c < n; c++) {
                if (board[r][c] == 0) {
                    continue;
                }
                if (abs(board[r][c]) == abs(board[r - 1][c]) && abs(board[r][c]) == abs(board[r + 1][c])) {
                    board[r][c] = -abs(board[r][c]);
                    board[r - 1][c] = -abs(board[r - 1][c]);
                    board[r + 1][c] = -abs(board[r + 1][c]);
                    complete = false;
                }
            }
        }

        // Check horizontally adjacent candies
        for (int r = 0; r < m; r++) {
            for (int c = 1; c < n - 1; c++) {
                if (board[r][c] == 0) {
                    continue;
                }
                if (abs(board[r][c]) == abs(board[r][c - 1]) && abs(board[r][c]) == abs(board[r][c + 1])) {
                    board[r][c] = -abs(board[r][c]);
                    board[r][c - 1] = -abs(board[r][c - 1]);
                    board[r][c + 1] = -abs(board[r][c + 1]);
                    complete = false;
                }
            }
        }

        // Set the value of each candy to be crushed as 0
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (board[r][c] < 0) {
                    board[r][c] = 0;
                }
            }
        }

        return complete;
    }

    void drop(vector<vector<int>>& board) {
        for (int c = 0; c < n; c++) {
            int lowestZero = -1;

            // Iterate over each column
            for (int r = m - 1; r >= 0; r--) {
                if (board[r][c] == 0) {
                    lowestZero = max(lowestZero, r);
                } else if (lowestZero >= 0) {
                    int temp = board[r][c];
                    board[r][c] = board[lowestZero][c];
                    board[lowestZero][c] = temp;
                    lowestZero--;
                }
            }
        }
    }

public:
    vector<vector<int>> candyCrush(vector<vector<int>>& board) {
        m = board.size();
        n = board[0].size();

        // Continue with the three steps until we can no longer find any crushable candies.
        while (!findAndCrush(board)) {
            drop(board);
        }

        return board;
    }
};
```

**Complexity**

- Time complexity: $O(m^2 \cdot n^2)$
- Space complexity: $O(1)$ constant space

> Where $m × n$ is the size of the grid `board`
