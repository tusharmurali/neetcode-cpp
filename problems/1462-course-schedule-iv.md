# 1462. Course Schedule IV

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/course-schedule-iv/>  
- **NeetCode:** <https://neetcode.io/problems/course-schedule-iv>  
- **Video:** <https://www.youtube.com/watch?v=cEW05ofxhn0>  

[← Back to index](../INDEX.md)

## 1. Brute Force (DFS)

To check if course A is a prerequisite of course B, we need to determine if there is a path from A to B in the prerequisite graph. A depth-first search starting from A can explore all courses reachable from A. If we reach B during this traversal, then A is indeed a prerequisite of B.

```cpp
class Solution {
    vector<vector<int>> adj;

public:
    vector<bool> checkIfPrerequisite(int numCourses, vector<vector<int>>& prerequisites, vector<vector<int>>& queries) {
        adj.assign(numCourses, vector<int>());
        for (auto& pre : prerequisites) {
            adj[pre[0]].push_back(pre[1]);
        }

        vector<bool> res;
        for (auto& query : queries) {
            res.push_back(dfs(query[0], query[1]));
        }
        return res;
    }

private:
    bool dfs(int node, int target) {
        if (node == target) return true;
        for (int nei : adj[node]) {
            if (dfs(nei, target)) return true;
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O((V + E) * m)$
- Space complexity: $O(V + E + m)$

> Where $m$ is the number of queries, $V$ is the number of courses, and $E$ is the number of prerequisites.

## 2. Depth First Search (Hash Set)

Instead of running DFS for every query, we can precompute all prerequisites for each course. For each course, we use DFS to find all courses that are prerequisites (directly or indirectly) and store them in a set. Then answering any query becomes a simple set lookup.

```cpp

class Solution {
    vector<vector<int>> adj;
    unordered_map<int, unordered_set<int>> prereqMap;

public:
    vector<bool> checkIfPrerequisite(int numCourses, vector<vector<int>>& prerequisites, vector<vector<int>>& queries) {
        adj.assign(numCourses, vector<int>());
        for (auto& pre : prerequisites) {
            adj[pre[1]].push_back(pre[0]);
        }
        for (int crs = 0; crs < numCourses; crs++) {
            dfs(crs);
        }

        vector<bool> res;
        for (auto& query : queries) {
            res.push_back(prereqMap[query[1]].count(query[0]));
        }
        return res;
    }

private:
    unordered_set<int>& dfs(int crs) {
        if (prereqMap.count(crs)) {
            return prereqMap[crs];
        }
        prereqMap[crs] = unordered_set<int>();
        for (int pre : adj[crs]) {
            auto& cur = dfs(pre);
            prereqMap[crs].insert(cur.begin(), cur.end());
        }
        prereqMap[crs].insert(crs);
        return prereqMap[crs];
    }
};
```

**Complexity**

- Time complexity: $O(V * (V + E) + m)$
- Space complexity: $O(V ^ 2 + E + m)$

> Where $m$ is the number of queries, $V$ is the number of courses, and $E$ is the number of prerequisites.

## 3. Depth First Search (Memoization)

We can optimize by memoizing the result for each pair of courses. When checking if course `A` is a prerequisite of course `B`, we store the result so that future queries for the same pair can be answered instantly. This avoids redundant graph traversals for repeated or similar queries.

```cpp
class Solution {
    vector<vector<int>> adj;
    vector<vector<int>> isPrereq;

public:
    vector<bool> checkIfPrerequisite(int numCourses, vector<vector<int>>& prerequisites, vector<vector<int>>& queries) {
        adj.assign(numCourses, vector<int>());
        isPrereq.assign(numCourses, vector<int>(numCourses, -1));

        for (auto& pre : prerequisites) {
            adj[pre[1]].push_back(pre[0]);
            isPrereq[pre[1]][pre[0]] = 1;
        }

        vector<bool> res;
        for (auto& query : queries) {
            res.push_back(dfs(query[1], query[0]));
        }
        return res;
    }

private:
    bool dfs(int crs, int prereq) {
        if (isPrereq[crs][prereq] != -1) {
            return isPrereq[crs][prereq] == 1;
        }
        for (int pre : adj[crs]) {
            if (pre == prereq || dfs(pre, prereq)) {
                isPrereq[crs][prereq] = 1;
                return true;
            }
        }
        isPrereq[crs][prereq] = 0;
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(V * (V + E) + m)$
- Space complexity: $O(V ^ 2 + E + m)$

> Where $m$ is the number of queries, $V$ is the number of courses, and $E$ is the number of prerequisites.

## 4. Topological Sort (Kahn's Algorithm)

Using topological sort, we process courses in an order where all prerequisites of a course are processed before the course itself. When we process a course, we propagate all its prerequisites to its successors. This way, each course accumulates the complete set of all courses that must be taken before it.

```cpp
class Solution {
public:
    vector<bool> checkIfPrerequisite(int numCourses, vector<vector<int>>& prerequisites, vector<vector<int>>& queries) {
        vector<unordered_set<int>> adj(numCourses), isPrereq(numCourses);
        vector<int> indegree(numCourses, 0);

        for (auto& pre : prerequisites) {
            adj[pre[0]].insert(pre[1]);
            indegree[pre[1]]++;
        }

        queue<int> q;
        for (int i = 0; i < numCourses; i++) {
            if (indegree[i] == 0) q.push(i);
        }

        while (!q.empty()) {
            int node = q.front(); q.pop();
            for (int neighbor : adj[node]) {
                isPrereq[neighbor].insert(node);
                isPrereq[neighbor].insert(isPrereq[node].begin(), isPrereq[node].end());
                indegree[neighbor]--;
                if (indegree[neighbor] == 0) q.push(neighbor);
            }
        }

        vector<bool> res;
        for (auto& query : queries) {
            res.push_back(isPrereq[query[1]].count(query[0]));
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(V * (V + E) + m)$
- Space complexity: $O(V ^ 2 + E + m)$

> Where $m$ is the number of queries, $V$ is the number of courses, and $E$ is the number of prerequisites.

## 5. Floyd Warshall Algorithm

The Floyd-Warshall algorithm finds all-pairs reachability in a graph. We can adapt it to find transitive closure: if there is a path from `A` to `B` through any intermediate course `K`, then `A` is a prerequisite of `B`. After running the algorithm, we have direct `O(1)` lookup for any pair.

```cpp
class Solution {
public:
    vector<bool> checkIfPrerequisite(int numCourses, vector<vector<int>>& prerequisites, vector<vector<int>>& queries) {
        vector<vector<bool>> adj(numCourses, vector<bool>(numCourses, false));
        vector<bool> res;

        for (auto& pre : prerequisites) {
            adj[pre[0]][pre[1]] = true;
        }

        for (int k = 0; k < numCourses; k++) {
            for (int i = 0; i < numCourses; i++) {
                for (int j = 0; j < numCourses; j++) {
                    adj[i][j] = adj[i][j] || (adj[i][k] && adj[k][j]);
                }
            }
        }

        for (auto& q : queries) {
            res.push_back(adj[q[0]][q[1]]);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(V ^ 3 + E + m)$
- Space complexity: $O(V ^ 2 + E + m)$

> Where $m$ is the number of queries, $V$ is the number of courses, and $E$ is the number of prerequisites.
