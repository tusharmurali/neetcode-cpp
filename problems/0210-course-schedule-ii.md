# 210. Course Schedule II

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/course-schedule-ii/>  
- **NeetCode:** <https://neetcode.io/problems/course-schedule-ii>  
- **Video:** <https://www.youtube.com/watch?v=Akt3glAwyfY>  
- **Video approach:** 1. Cycle Detection (DFS)  

[← Back to index](../INDEX.md)

## 1. Cycle Detection (DFS) ▶ video

Each course is a **node**, and each prerequisite is a **directed edge**.  
We want an order of courses such that all prerequisites of a course are taken **before** it.

Using **DFS**, we:

- Detect cycles (which make it impossible to finish all courses)
- Add a course to the result **after** all its prerequisites are processed  
  (this naturally gives a valid topological order)

```cpp
class Solution {
public:
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
        unordered_map<int, vector<int>> prereq;
        for (const auto& pair : prerequisites) {
            prereq[pair[0]].push_back(pair[1]);
        }

        vector<int> output;
        unordered_set<int> visit;
        unordered_set<int> cycle;

        for (int course = 0; course < numCourses; course++) {
            if (!dfs(course, prereq, visit, cycle, output)) {
                return {};
            }
        }

        return output;
    }

private:
    bool dfs(int course, const unordered_map<int, vector<int>>& prereq,
             unordered_set<int>& visit, unordered_set<int>& cycle,
             vector<int>& output) {

        if (cycle.count(course)) {
            return false;
        }
        if (visit.count(course)) {
            return true;
        }

        cycle.insert(course);
        if (prereq.count(course)) {
            for (int pre : prereq.at(course)) {
                if (!dfs(pre, prereq, visit, cycle, output)) {
                    return false;
                }
            }
        }
        cycle.erase(course);
        visit.insert(course);
        output.push_back(course);
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
A course can be taken only when **all its prerequisites are completed**.

Kahn's Algorithm works by:

- Always taking courses with **no remaining prerequisites** (`indegree = 0`)
- Removing them from the graph
- Gradually unlocking other courses

If at the end some courses are still locked, it means a **cycle exists**, so no valid order is possible.

```cpp
class Solution {
public:
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
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
        vector<int> output(numCourses);
        while (!q.empty()) {
            int node = q.front();q.pop();
            output[numCourses - finish - 1] = node;
            finish++;
            for (int nei : adj[node]) {
                indegree[nei]--;
                if (indegree[nei] == 0) {
                    q.push(nei);
                }
            }
        }

        if (finish != numCourses) {
            return {};
        }
        return output;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of courses and $E$ is the number of prerequisites.

## 3. Topological Sort (DFS)

We want an order of courses such that **every course appears after its prerequisites**.
This approach mixes **Topological Sorting** with **DFS-style traversal**.

The idea is:

- Start from courses that have **no prerequisites** (`indegree = 0`)
- Once we take a course, we "remove" it by decreasing the `indegree` of courses that depend on it
- When a dependent course's `indegree` becomes `0`, it is now safe to take, so we continue DFS from it

If we can visit all courses this way, a valid order exists.
If not, a **cycle** is present, making it impossible.

```cpp
class Solution {
    vector<int> output;
    vector<int> indegree;
    vector<vector<int>> adj;

    void dfs(int node) {
        output.push_back(node);
        indegree[node]--;
        for (int nei : adj[node]) {
            indegree[nei]--;
            if (indegree[nei] == 0) {
                dfs(nei);
            }
        }
    }

public:
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
        adj = vector<vector<int>>(numCourses);
        indegree = vector<int>(numCourses, 0);
        for (auto& pre : prerequisites) {
            indegree[pre[0]]++;
            adj[pre[1]].push_back(pre[0]);
        }

        for (int i = 0; i < numCourses; i++) {
            if (indegree[i] == 0) {
                dfs(i);
            }
        }

        if (output.size() != numCourses) return {};
        return output;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V + E)$

> Where $V$ is the number of courses and $E$ is the number of prerequisites.

## Standalone solution file (`cpp/0210-course-schedule-ii.cpp` in the NeetCode repo)

```cpp
/*
    Courses & prerequisites, return ordering of courses to take to finish all courses
    Ex. numCourses = 2, prerequisites = [[1,0]] -> [0,1], take course 0 then 1

    All courses can be completed if there's no cycle, check for cycles

    Time: O(V + E)
    Space: O(V + E)
*/

class Solution {
public:
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
        unordered_map<int, vector<int>> m;
        // build adjacency list of prereqs
        for (int i = 0; i < prerequisites.size(); i++) {
            m[prerequisites[i][0]].push_back(prerequisites[i][1]);
        }
        unordered_set<int> visit;
        unordered_set<int> cycle;
        
        vector<int> result;
        for (int course = 0; course < numCourses; course++) {
            if (!dfs(course, m, visit, cycle, result)) {
                return {};
            }
        }
        return result;
    }
private:
    // a course has 3 possible states:
    // visited -> course added to result
    // visiting -> course not added to result, but added to cycle
    // unvisited -> course not added to result or cycle
    bool dfs(int course, unordered_map<int, vector<int>>& m, unordered_set<int>& visit,
        unordered_set<int>& cycle, vector<int>& result) {
        
        if (cycle.find(course) != cycle.end()) {
            return false;
        }
        if (visit.find(course) != visit.end()) {
            return true;
        }
        cycle.insert(course);
        for (int i = 0; i < m[course].size(); i++) {
            int nextCourse = m[course][i];
            if (!dfs(nextCourse, m, visit, cycle, result)) {
                return false;
            }
        }
        cycle.erase(course);
        visit.insert(course);
        result.push_back(course);
        return true;
    }
};
```
