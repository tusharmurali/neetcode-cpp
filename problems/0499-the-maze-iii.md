# 499. The Maze III

- **Difficulty:** Hard  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/the-maze-iii/>  
- **NeetCode:** <https://neetcode.io/problems/the-maze-iii>  

[← Back to index](../INDEX.md)

## 1. Dijkstra's

This problem extends Maze II by adding a hole the ball can fall into and requiring the lexicographically smallest path among all shortest paths. The ball must stop at the hole if it rolls over it during movement.

We use Dijkstra's algorithm with a priority queue that orders states by distance first, then by path string lexicographically. This ensures when we first reach the hole, we have both the shortest distance and the lexicographically smallest path for that distance.

```cpp
class Solution {
private:
    // State: (distance, path, row, col)
    // Priority queue will sort by distance first, then path lexicographically
    using State = tuple<int, string, int, int>;

    vector<vector<int>> directions = {{0, -1}, {-1, 0}, {0, 1}, {1, 0}};
    vector<string> textDirections = {"l", "u", "r", "d"};
    int m;
    int n;

    bool valid(int row, int col, vector<vector<int>>& maze) {
        if (row < 0 || row >= m || col < 0 || col >= n) {
            return false;
        }
        return maze[row][col] == 0;
    }

    vector<State> getNeighbors(int row, int col, vector<vector<int>>& maze, vector<int>& hole) {
        vector<State> neighbors;

        for (int i = 0; i < 4; i++) {
            int dy = directions[i][0];
            int dx = directions[i][1];
            string direction = textDirections[i];

            int currRow = row;
            int currCol = col;
            int dist = 0;

            while (valid(currRow + dy, currCol + dx, maze)) {
                currRow += dy;
                currCol += dx;
                dist++;

                if (currRow == hole[0] && currCol == hole[1]) {
                    break;
                }
            }

            neighbors.push_back(make_tuple(dist, direction, currRow, currCol));
        }

        return neighbors;
    }

public:
    string findShortestWay(vector<vector<int>>& maze, vector<int>& ball, vector<int>& hole) {
        m = maze.size();
        n = maze[0].size();

        // Min heap: sorts by distance, then path lexicographically
        priority_queue<State, vector<State>, greater<State>> heap;
        vector<vector<bool>> seen(m, vector<bool>(n, false));

        heap.push(make_tuple(0, "", ball[0], ball[1]));

        while (!heap.empty()) {
            State curr = heap.top();
            heap.pop();

            int dist = get<0>(curr);
            string path = get<1>(curr);
            int row = get<2>(curr);
            int col = get<3>(curr);

            if (seen[row][col]) {
                continue;
            }

            if (row == hole[0] && col == hole[1]) {
                return path;
            }

            seen[row][col] = true;

            for (State& nextState : getNeighbors(row, col, maze, hole)) {
                int nextDist = get<0>(nextState);
                string nextChar = get<1>(nextState);
                int nextRow = get<2>(nextState);
                int nextCol = get<3>(nextState);

                heap.push(make_tuple(dist + nextDist, path + nextChar, nextRow, nextCol));
            }
        }

        return "impossible";
    }
};
```

**Complexity**

- Time complexity: $O(n \cdot \log n)$
- Space complexity: $O(n)$

> Where $n$ is the number of squares in `maze`.
