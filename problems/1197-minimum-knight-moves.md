# 1197. Minimum Knight Moves

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-knight-moves/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-knight-moves>  

[← Back to index](../INDEX.md)

## 1. BFS (Breadth-First Search)

Finding the minimum moves for a knight is a classic shortest path problem on an unweighted graph. Each cell is a node, and knight moves define the edges. BFS naturally finds the shortest path because it explores all positions at distance `k` before any position at distance `k+1`.

Starting from the origin `(0, 0)`, we expand outward level by level. The first time we reach the target coordinates, we've found the minimum number of moves.

```cpp
class Solution {
public:
    int minKnightMoves(int x, int y) {
        // the offsets in the eight directions
        int offsets[8][2] = {{1, 2}, {2, 1}, {2, -1}, {1, -2},
                             {-1, -2}, {-2, -1}, {-2, 1}, {-1, 2}};

        // - Rather than using the inefficient hash set, we use the bitmap
        //     otherwise we would run out of time for the test cases.
        // - We create a bitmap that is sufficient to cover all the possible
        //     inputs, according to the description of the problem.
        vector<vector<bool>> visited(607, vector<bool>(607, false));

        queue<pair<int, int>> q;
        q.push({0, 0});
        int steps = 0;

        while (!q.empty()) {
            int currLevelSize = q.size();
            // iterate through the current level
            for (int i = 0; i < currLevelSize; i++) {
                auto [cx, cy] = q.front();
                q.pop();
                if (cx == x && cy == y) {
                    return steps;
                }

                for (auto& offset : offsets) {
                    int nx = cx + offset[0], ny = cy + offset[1];
                    // align the coordinate to the bitmap
                    if (!visited[nx + 302][ny + 302]) {
                        visited[nx + 302][ny + 302] = true;
                        q.push({nx, ny});
                    }
                }
            }
            // move on to the next level
            steps++;
        }
        return steps;
    }
};
```

**Complexity**

- Time complexity: $O\left(\left(\max(|x|, |y|)\right)^2\right)$
- Space complexity: $O\left(\left(\max(|x|, |y|)\right)^2\right)$

> Where $(x,y)$ is the coordinate of the target.

## 2. Bidirectional BFS

Standard BFS explores an ever-growing circle from the origin. Bidirectional BFS reduces the search space by expanding from both the origin and the target simultaneously. When the two search frontiers meet, we've found the shortest path.

This optimization works well because the area explored grows quadratically with distance. By meeting in the middle, each search only needs to cover roughly half the distance, significantly reducing the total positions explored.

```cpp
class Solution {
public:
    int minKnightMoves(int x, int y) {
        // the offsets in the eight directions
        int offsets[8][2] = {{1, 2}, {2, 1}, {2, -1}, {1, -2},
                             {-1, -2}, {-2, -1}, {-2, 1}, {-1, 2}};

        auto key = [](int a, int b) { return (long long)a * 1000 + b; };

        // data structures needed to move from the origin point
        queue<array<int, 3>> originQueue;
        originQueue.push({0, 0, 0});
        unordered_map<long long, int> originDistance;
        originDistance[key(0, 0)] = 0;

        // data structures needed to move from the target point
        queue<array<int, 3>> targetQueue;
        targetQueue.push({x, y, 0});
        unordered_map<long long, int> targetDistance;
        targetDistance[key(x, y)] = 0;

        while (true) {
            // check if we reach the circle of target
            auto origin = originQueue.front();
            originQueue.pop();
            long long originXY = key(origin[0], origin[1]);
            if (targetDistance.count(originXY)) {
                return origin[2] + targetDistance[originXY];
            }

            // check if we reach the circle of origin
            auto target = targetQueue.front();
            targetQueue.pop();
            long long targetXY = key(target[0], target[1]);
            if (originDistance.count(targetXY)) {
                return target[2] + originDistance[targetXY];
            }

            for (auto& offset : offsets) {
                // expand the circle of origin
                int nox = origin[0] + offset[0], noy = origin[1] + offset[1];
                long long nextOriginXY = key(nox, noy);
                if (!originDistance.count(nextOriginXY)) {
                    originQueue.push({nox, noy, origin[2] + 1});
                    originDistance[nextOriginXY] = origin[2] + 1;
                }

                // expand the circle of target
                int ntx = target[0] + offset[0], nty = target[1] + offset[1];
                long long nextTargetXY = key(ntx, nty);
                if (!targetDistance.count(nextTargetXY)) {
                    targetQueue.push({ntx, nty, target[2] + 1});
                    targetDistance[nextTargetXY] = target[2] + 1;
                }
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O\left(\left(\max(|x|, |y|)\right)^2\right)$
- Space complexity: $O\left(\left(\max(|x|, |y|)\right)^2\right)$

> Where $(x,y)$ is the coordinate of the target.

## 3. DFS (Depth-First Search) with Memoization

Due to the knight's movement symmetry, we only need to consider the first quadrant (positive `x` and `y`). The minimum moves to reach `(-x, y)`, `(x, -y)`, or `(-x, -y)` are the same as reaching `(x, y)`.

We can define a recursive relation: the minimum moves to reach `(x, y)` equals `1` plus the minimum of reaching `(|x-1|, |y-2|)` or `(|x-2|, |y-1|)`. The absolute values keep us in the first quadrant, and memoization prevents redundant calculations.

```cpp
class Solution {
private:
    unordered_map<string, int> memo;

    int dfs(int x, int y) {
        string key = to_string(x) + "," + to_string(y);
        if (memo.find(key) != memo.end()) {
            return memo[key];
        }

        if (x + y == 0) {
            return 0;
        } else if (x + y == 2) {
            return 2;
        } else {
            int ret = min(dfs(abs(x - 1), abs(y - 2)),
                         dfs(abs(x - 2), abs(y - 1))) + 1;
            memo[key] = ret;
            return ret;
        }
    }

public:
    int minKnightMoves(int x, int y) {
        return dfs(abs(x), abs(y));
    }
};
```

**Complexity**

- Time complexity: $O(|x \cdot y|)$
- Space complexity: $O(|x \cdot y|)$

> Where $(x,y)$ is the coordinate of the target.
