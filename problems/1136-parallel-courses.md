# 1136. Parallel Courses

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/parallel-courses/>  
- **NeetCode:** <https://neetcode.io/problems/parallel-courses>  

[← Back to index](../INDEX.md)

## 1. Breadth-First Search (Kahn's Algorithm)

This problem asks for the minimum number of semesters to complete all courses with prerequisites. Since we can take multiple courses in parallel each semester (as long as their prerequisites are met), this naturally maps to a topological sort problem where we process courses level by level.

Kahn's algorithm works perfectly here. We start with courses that have no prerequisites (in-degree of 0) and take them all in the first semester. Then we remove their outgoing edges, which may unlock new courses for the next semester. Each BFS level represents one semester.

If we cannot complete all courses (due to a cycle), we return -1.

```cpp
class Solution {
public:
    int minimumSemesters(int N, vector<vector<int>>& relations) {
        vector<int> inCount(N + 1, 0);  // or indegree
        vector<vector<int>> graph(N + 1);
        for (auto& relation : relations) {
            graph[relation[0]].push_back(relation[1]);
            inCount[relation[1]]++;
        }

        int step = 0;
        int studiedCount = 0;
        vector<int> bfsQueue;
        for (int node = 1; node < N + 1; node++) {
            if (inCount[node] == 0) {
                bfsQueue.push_back(node);
            }
        }

        // start learning with BFS
        while (!bfsQueue.empty()) {
            // start new semester
            step++;
            vector<int> nextQueue;
            for (auto& node : bfsQueue) {
                studiedCount++;
                for (auto& endNode : graph[node]) {
                    inCount[endNode]--;
                    // if all prerequisite courses learned
                    if (inCount[endNode] == 0) {
                        nextQueue.push_back(endNode);
                    }
                }
            }
            bfsQueue = nextQueue;
        }

        // check if learn all courses
        return studiedCount == N ? step : -1;
    }
};
```

**Complexity**

- Time complexity: $O(N + E)$
- Space complexity: $O(N + E)$

> Where $E$ is the length of `relations` and $N$ is the number of courses.

## 2. Depth-First Search: Check for Cycles + Find Longest Path

The minimum number of semesters equals the length of the longest path in the prerequisite graph. This is because courses along the longest dependency chain must be taken sequentially, one per semester.

This approach uses two DFS passes: first to detect cycles (making it impossible to finish), then to find the longest path from any starting node. We use memoization to avoid recomputing path lengths for nodes we have already visited.

```cpp
class Solution {
public:
    int minimumSemesters(int N, vector<vector<int>>& relations) {
        vector<vector<int>> graph(N + 1);
        for (auto& relation : relations) {
            graph[relation[0]].push_back(relation[1]);
        }
        // check if the graph contains a cycle
        vector<int> visited(N + 1, 0);
        for (int node = 1; node < N + 1; node++) {
            // if has cycle, return -1
            if (dfsCheckCycle(node, graph, visited) == -1) {
                return -1;
            }
        }

        // if no cycle, return the longest path
        vector<int> visitedLength(N + 1, 0);
        int maxLength = 1;
        for (int node = 1; node < N + 1; node++) {
            int length = dfsMaxPath(node, graph, visitedLength);
            maxLength = max(length, maxLength);
        }
        return maxLength;
    }

private:
    int dfsCheckCycle(int node, vector<vector<int>>& graph,
                      vector<int>& visited) {
        // return -1 if has a cycle
        // return 1 if does not have any cycle
        if (visited[node] != 0) {
            return visited[node];
        } else {
            // mark as visiting
            visited[node] = -1;
        }
        for (auto& endNode : graph[node]) {
            if (dfsCheckCycle(endNode, graph, visited) == -1) {
                // we meet a cycle!
                return -1;
            }
        }
        // mark as visited
        visited[node] = 1;
        return 1;
    }

    int dfsMaxPath(int node, vector<vector<int>>& graph,
                   vector<int>& visitedLength) {
        // return the longest path (inclusive)
        if (visitedLength[node] != 0) {
            return visitedLength[node];
        }
        int maxLength = 1;
        for (auto& endNode : graph[node]) {
            int length = dfsMaxPath(endNode, graph, visitedLength);
            maxLength = max(length + 1, maxLength);
        }
        // store it
        visitedLength[node] = maxLength;
        return maxLength;
    }
};
```

**Complexity**

- Time complexity: $O(N + E)$
- Space complexity: $O(N + E)$

> Where $E$ is the length of `relations` and $N$ is the number of courses.

## 3. Depth-First Search: Combine

We can combine cycle detection and longest path computation into a single DFS. The key insight is that a node in the "visiting" state during DFS indicates a cycle. We use -1 as a sentinel value to indicate both "currently visiting" and "cycle detected."

When we finish processing a node, we store its longest path length. If we ever encounter -1 from a recursive call, we propagate that cycle indicator upward. This eliminates the need for a separate cycle detection pass.

```cpp
class Solution {
public:
    int minimumSemesters(int N, vector<vector<int>>& relations) {
        vector<vector<int>> graph(N + 1);
        for (auto& relation : relations) {
            graph[relation[0]].push_back(relation[1]);
        }

        vector<int> visited(N + 1, 0);
        int maxLength = 1;
        for (int node = 1; node < N + 1; node++) {
            int length = dfs(node, graph, visited);
            // we meet a cycle!
            if (length == -1) {
                return -1;
            }
            maxLength = max(length, maxLength);
        }
        return maxLength;
    }

private:
    int dfs(int node, vector<vector<int>>& graph, vector<int>& visited) {
        // return the longest path (inclusive)
        if (visited[node] != 0) {
            return visited[node];
        } else {
            // mark as visiting
            visited[node] = -1;
        }
        int maxLength = 1;
        for (auto& endNode : graph[node]) {
            int length = dfs(endNode, graph, visited);
            // we meet a cycle!
            if (length == -1) {
                return -1;
            }
            maxLength = max(length + 1, maxLength);
        }
        // mark as visited
        visited[node] = maxLength;
        return maxLength;
    }
};
```

**Complexity**

- Time complexity: $O(N + E)$
- Space complexity: $O(N + E)$

> Where $E$ is the length of `relations` and $N$ is the number of courses.
