# 207. Course Schedule

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/course-schedule/>  
- **NeetCode:** <https://neetcode.io/problems/course-schedule>  
- **Video:** <https://www.youtube.com/watch?v=EgI5nU9etnU>  
- **Video approach:** 1. Cycle Detection (DFS)  

[← Back to index](../INDEX.md)

## 1. Cycle Detection (DFS) ▶ video

Each course is a node, and each prerequisite is a **directed edge**.  
You can finish all courses **only if there is no cycle** in this directed graph.

A cycle means:

- Course A needs B
- B needs C
- C needs A  
  So you’re stuck forever.

We use **DFS with cycle detection**:

- While doing DFS, keep track of courses in the **current recursion path**.
- If we visit a course already in the current path → **cycle found**.
- If a course has no prerequisites left, it’s safe.

```cpp
class Solution {
    // Map each course to its prerequisites
    unordered_map<int, vector<int>> preMap;
    // Store all courses along the current DFS path
    unordered_set<int> visiting;

public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        for (int i = 0; i < numCourses; i++) {
            preMap[i] = {};
        }
        for (const auto& prereq : prerequisites) {
            preMap[prereq[0]].push_back(prereq[1]);
        }

        for (int c = 0; c < numCourses; c++) {
            if (!dfs(c)) {
                return false;
            }
        }
        return true;
    }

    bool dfs(int crs) {
        if (visiting.count(crs)) {
            // Cycle detected
            return false;
        }
        if (preMap[crs].empty()) {
            return true;
        }

        visiting.insert(crs);
        for (int pre : preMap[crs]) {
            if (!dfs(pre)) {
                return false;
            }
        }
        visiting.erase(crs);
        preMap[crs].clear();
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of courses and $E$ is the number of prerequisites.

## 2. Topological Sort (Kahn's Algorithm)

Treat each course as a **node** and each prerequisite as a **directed edge**.
If a course has no prerequisites, it can be taken immediately.

Kahn's Algorithm repeatedly takes courses that have **zero prerequisites**.
When we finish a course, we remove its dependency effect from other courses.

- If all courses can be taken this way - **no cycle**, return `true`
- If some courses are never taken - **cycle exists**, return `false`

```cpp
class Solution {
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        vector<int> indegree(numCourses, 0);
        vector<vector<int>> adj(numCourses);

        for (auto& pre : prerequisites) {
            indegree[pre[1]]++;
            adj[pre[0]].push_back(pre[1]);
        }

        queue<int> q;
        for (int i = 0; i < numCourses; ++i) {
            if (indegree[i] == 0) {
                q.push(i);
            }
        }

        int finish = 0;
        while (!q.empty()) {
            int node = q.front();
            q.pop();
            finish++;
            for (int nei : adj[node]) {
                indegree[nei]--;
                if (indegree[nei] == 0) {
                    q.push(nei);
                }
            }
        }

        return finish == numCourses;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of courses and $E$ is the number of prerequisites.

## Standalone solution file (`cpp/0207-course-schedule.cpp` in the NeetCode repo)

```cpp
/*
    Courses & prerequisites, return true if can finish all courses
    Ex. numCourses = 2, prerequisites = [[1,0]] -> true

    All courses can be completed if there's no cycle (visit already visited)

    Time: O(V + E)
    Space: O(V + E)
*/

class Solution {
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        // map each course to prereq list
        unordered_map<int, vector<int>> m;
        for (int i = 0; i < prerequisites.size(); i++) {
            m[prerequisites[i][0]].push_back(prerequisites[i][1]);
        }
        // all courses along current DFS path
        unordered_set<int> visited;
        
        for (int course = 0; course < numCourses; course++) {
            if (!dfs(course, m, visited)) {
                return false;
            }
        }
        return true;
    }
private:
    bool dfs(int course, unordered_map<int, vector<int>>& m, unordered_set<int>& visited) {
        if (visited.find(course) != visited.end()) {
            return false;
        }
        if (m[course].empty()) {
            return true;
        }
        visited.insert(course);
        for (int i = 0; i < m[course].size(); i++) {
            int nextCourse = m[course][i];
            if (!dfs(nextCourse, m, visited)) {
                return false;
            }
        }
        m[course].clear();
        visited.erase(course);
        return true;
    }
};
```
