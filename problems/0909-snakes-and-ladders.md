# 909. Snakes And Ladders

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/snakes-and-ladders/>  
- **NeetCode:** <https://neetcode.io/problems/snakes-and-ladders>  
- **Video:** <https://www.youtube.com/watch?v=6lH4nO3JfLk>  

[← Back to index](../INDEX.md)

## 1. Breadth First Search - I

This is a shortest path problem on an implicit graph where each square connects to the next 1 to 6 squares (simulating a dice roll). BFS naturally finds the shortest path in an unweighted graph. The tricky part is converting between square numbers and board coordinates, since the board uses a boustrophedon (zigzag) pattern starting from the bottom-left.

```cpp
class Solution {
public:
    int snakesAndLadders(vector<vector<int>>& board) {
        int n = board.size();
        queue<pair<int, int>> q;
        q.push({1, 0});
        unordered_set<int> visit;

        while (!q.empty()) {
            auto [square, moves] = q.front(); q.pop();

            for (int i = 1; i <= 6; i++) {
                int nextSquare = square + i;
                auto [r, c] = intToPos(nextSquare, n);
                if (board[r][c] != -1) {
                    nextSquare = board[r][c];
                }
                if (nextSquare == n * n) return moves + 1;
                if (!visit.count(nextSquare)) {
                    visit.insert(nextSquare);
                    q.push({nextSquare, moves + 1});
                }
            }
        }
        return -1;
    }

private:
    pair<int, int> intToPos(int square, int n) {
        int r = (square - 1) / n;
        int c = (square - 1) % n;
        if (r % 2 == 1) c = n - 1 - c;
        r = n - 1 - r;
        return {r, c};
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 2. Breadth First Search - II

This variation uses a distance array instead of a visited set, storing the minimum moves to reach each square. This approach is slightly more explicit about tracking distances and allows for early termination once we reach the destination. The core BFS logic remains the same.

```cpp
class Solution {
public:
    int snakesAndLadders(vector<vector<int>>& board) {
        int n = board.size();
        vector<int> dist(n * n + 1, -1);
        queue<int> q;
        q.push(1);
        dist[1] = 0;

        while (!q.empty()) {
            int square = q.front();
            q.pop();

            for (int i = 1; i <= 6; i++) {
                int nextSquare = square + i;
                if (nextSquare > n * n) {
                    break;
                }

                auto [r, c] = intToPos(nextSquare, n);
                if (board[r][c] != -1) {
                    nextSquare = board[r][c];
                }

                if (dist[nextSquare] == -1) {
                    dist[nextSquare] = dist[square] + 1;
                    if (nextSquare == n * n) {
                        return dist[nextSquare];
                    }
                    q.push(nextSquare);
                }
            }
        }

        return -1;
    }

private:
    pair<int, int> intToPos(int square, int n) {
        int r = (square - 1) / n;
        int c = (square - 1) % n;
        if (r % 2 == 1) {
            c = n - 1 - c;
        }
        r = n - 1 - r;
        return {r, c};
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Breadth First Search - III

This optimization modifies the board in place to track visited squares, eliminating the need for a separate visited set or distance array. By marking visited positions directly on the board with a special value (0), we reduce memory overhead while maintaining the same BFS traversal logic.

```cpp
class Solution {
public:
    int snakesAndLadders(vector<vector<int>>& board) {
        int n = board.size();
        queue<int> q;
        q.push(1);
        board[n - 1][0] = 0;
        int moves = 0;

        while (!q.empty()) {
            for (int it = q.size(); it > 0; it--) {
                int square = q.front(); q.pop();
                for (int i = 1; i <= 6; i++) {
                    int nextSquare = square + i;
                    if (nextSquare > n * n) {
                        break;
                    }

                    auto [r, c] = intToPos(nextSquare, n);
                    if (board[r][c] != -1) {
                        nextSquare = board[r][c];
                    }

                    if (board[r][c] != 0) {
                        if (nextSquare == n * n) {
                            return moves + 1;
                        }

                        board[r][c] = 0;
                        q.push(nextSquare);
                    }
                }
            }
            moves++;
        }

        return -1;
    }

private:
    pair<int, int> intToPos(int square, int n) {
        int r = (square - 1) / n;
        int c = (square - 1) % n;
        if (r % 2 == 1) {
            c = n - 1 - c;
        }
        r = n - 1 - r;
        return {r, c};
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$
