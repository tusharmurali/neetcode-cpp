# 2050. Parallel Courses III

- **Difficulty:** Hard  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/parallel-courses-iii/>  
- **NeetCode:** <https://neetcode.io/problems/parallel-courses-iii>  
- **Video:** <https://www.youtube.com/watch?v=a_NlRPnqCrg>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

Each course has a duration, and we can take courses in parallel as long as prerequisites are satisfied. The minimum time to finish all courses equals the longest path in the dependency graph, where path length is the sum of course durations along that path.

For each course, we need to find the maximum time required to complete it and all its dependent courses. Using DFS with memoization, we compute the total time starting from each course by taking the maximum of all paths through its dependencies, plus the course's own duration.

```cpp
class Solution {
public:
    unordered_map<int, int> maxTime;
    vector<vector<int>> adj;
    vector<int> time;

    int minimumTime(int n, vector<vector<int>>& relations, vector<int>& time) {
        this->time = time;
        adj.resize(n + 1);

        for (auto& relation : relations) {
            adj[relation[0]].push_back(relation[1]);
        }

        for (int i = 1; i <= n; i++) {
            dfs(i);
        }

        int res = 0;
        for (auto& [key, value] : maxTime) {
            res = max(res, value);
        }
        return res;
    }

private:
    int dfs(int src) {
        if (maxTime.count(src)) {
            return maxTime[src];
        }

        int res = time[src - 1];
        for (int nei : adj[src]) {
            res = max(res, time[src - 1] + dfs(nei));
        }
        maxTime[src] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of courses and $E$ is the number of prerequisites.

## 2. Iterative DFS

The recursive DFS can be converted to an iterative version using an explicit stack. This avoids potential stack overflow for deep recursion and gives more control over the traversal order.

We use a two-phase approach: first push a node onto the stack, then when we pop it again after processing its children, we compute its final value. A "processed" flag distinguishes between these two phases.

```cpp
class Solution {
public:
    int minimumTime(int n, vector<vector<int>>& relations, vector<int>& time) {
        vector<vector<int>> adj(n);
        for (auto& rel : relations) {
            adj[rel[0] - 1].push_back(rel[1] - 1);
        }

        vector<int> maxTime(n, -1);
        vector<bool> processed(n, false);

        for (int i = 0; i < n; i++) {
            if (maxTime[i] == -1) {
                stack<int> stk;
                stk.push(i);
                while (!stk.empty()) {
                    int node = stk.top(); stk.pop();
                    if (processed[node]) {
                        int best = 0;
                        for (int nei : adj[node]) {
                            best = max(best, maxTime[nei]);
                        }
                        maxTime[node] = time[node] + best;
                    } else {
                        processed[node] = true;
                        stk.push(node);
                        for (int nei : adj[node]) {
                            if (maxTime[nei] == -1) {
                                stk.push(nei);
                            }
                        }
                    }
                }
            }
        }
        return *max_element(maxTime.begin(), maxTime.end());
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of courses and $E$ is the number of prerequisites.

## 3. Topological Sort (Kahn's Algorithm)

Instead of working backwards from end nodes (DFS approach), we can work forwards from start nodes using topological sort. Kahn's algorithm processes nodes in dependency order, ensuring that when we process a course, all its prerequisites have already been processed.

For each course, we track the maximum time needed to reach it (including its own duration). When we process a course, we update all its dependents by propagating the maximum completion time. This naturally computes the longest weighted path through the graph.

```cpp
class Solution {
public:
    int minimumTime(int n, vector<vector<int>>& relations, vector<int>& time) {
        vector<vector<int>> adj(n);
        vector<int> indegree(n, 0);
        vector<int> maxTime(time.begin(), time.end());

        for (auto& relation : relations) {
            int src = relation[0] - 1, dst = relation[1] - 1;
            adj[src].push_back(dst);
            indegree[dst]++;
        }

        queue<int> queue;
        for (int i = 0; i < n; i++) {
            if (indegree[i] == 0) {
                queue.push(i);
            }
        }

        while (!queue.empty()) {
            int node = queue.front(); queue.pop();
            for (int nei : adj[node]) {
                maxTime[nei] = max(maxTime[nei], maxTime[node] + time[nei]);
                if (--indegree[nei] == 0) {
                    queue.push(nei);
                }
            }
        }

        return *max_element(maxTime.begin(), maxTime.end());
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of courses and $E$ is the number of prerequisites.
