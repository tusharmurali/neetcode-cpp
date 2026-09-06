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
// NeetCode has no C++ version of this approach yet.
```

**Complexity**

- Time complexity: $O\left(\left(\max(|x|, |y|)\right)^2\right)$
- Space complexity: $O\left(\left(\max(|x|, |y|)\right)^2\right)$

> Where $(x,y)$ is the coordinate of the target.

## 2. Bidirectional BFS

Standard BFS explores an ever-growing circle from the origin. Bidirectional BFS reduces the search space by expanding from both the origin and the target simultaneously. When the two search frontiers meet, we've found the shortest path.

This optimization works well because the area explored grows quadratically with distance. By meeting in the middle, each search only needs to cover roughly half the distance, significantly reducing the total positions explored.

```cpp
// NeetCode has no C++ version of this approach yet.
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
