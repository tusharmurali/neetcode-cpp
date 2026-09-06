# 2092. Find All People With Secret

- **Difficulty:** Hard  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-all-people-with-secret/>  
- **NeetCode:** <https://neetcode.io/problems/find-all-people-with-secret>  
- **Video:** <https://www.youtube.com/watch?v=1XujGRSU1bQ>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

The secret spreads through meetings in chronological order. At each point in time, all meetings happening simultaneously form a graph where people can share secrets with each other. If anyone in a connected group already knows the secret, everyone in that group learns it by the end of that time slot. We process meetings time by time, using DFS to propagate the secret through connected components.

```cpp
class Solution {
public:
    unordered_set<int> secrets, visit;

    vector<int> findAllPeople(int n, vector<vector<int>>& meetings, int firstPerson) {
        secrets = {0, firstPerson};
        unordered_map<int, unordered_map<int, vector<int>>> time_map;

        for (auto& meet : meetings) {
            int src = meet[0], dst = meet[1], t = meet[2];
            time_map[t][src].push_back(dst);
            time_map[t][dst].push_back(src);
        }

        vector<int> timeKeys;
        for (auto& [t, _] : time_map) {
            timeKeys.push_back(t);
        }
        sort(timeKeys.begin(), timeKeys.end());

        for (int& t : timeKeys) {
            visit.clear();
            for (auto& [src, _] : time_map[t]) {
                if (secrets.count(src)) {
                    dfs(src, time_map[t]);
                }
            }
        }

        return vector<int>(secrets.begin(), secrets.end());
    }

private:
    void dfs(int src, unordered_map<int, vector<int>>& adj) {
        if (!visit.insert(src).second) return;
        secrets.insert(src);
        for (int& nei : adj[src]) {
            dfs(nei, adj);
        }
    }
};
```

**Complexity**

- Time complexity: $O(m \log m + n)$
- Space complexity: $O(m + n)$

> Where $m$ is the number of meetings and $n$ is the number of people.

## 2. Breadth First Search

This is the same concept as the DFS approach, but we use BFS instead to propagate the secret. At each time slot, we start BFS from all people who already know the secret and explore their meeting connections level by level. Both approaches achieve the same result with similar complexity.

```cpp
class Solution {
public:
    vector<int> findAllPeople(int n, vector<vector<int>>& meetings, int firstPerson) {
        unordered_set<int> secrets = {0, firstPerson};
        map<int, unordered_map<int, vector<int>>> time_map;

        for (auto& meet : meetings) {
            int src = meet[0], dst = meet[1], t = meet[2];
            time_map[t][src].push_back(dst);
            time_map[t][dst].push_back(src);
        }

        for (auto& [t, adj] : time_map) {
            unordered_set<int> visit;
            queue<int> q;

            for (auto& [src, _] : adj) {
                if (secrets.count(src)) {
                    q.push(src);
                    visit.insert(src);
                }
            }

            while (!q.empty()) {
                int node = q.front();
                q.pop();
                secrets.insert(node);
                for (int nei : adj[node]) {
                    if (!visit.count(nei)) {
                        visit.insert(nei);
                        q.push(nei);
                    }
                }
            }
        }

        return vector<int>(secrets.begin(), secrets.end());
    }
};
```

**Complexity**

- Time complexity: $O(m \log m + n)$
- Space complexity: $O(m + n)$

> Where $m$ is the number of meetings and $n$ is the number of people.

## 3. Iterative DFS

Instead of using recursion for DFS, we can use an explicit stack. This approach sorts all meetings by time first, then processes groups of meetings with the same timestamp together. For each group, we build an adjacency list and use a stack-based DFS starting from all current secret-holders.

```cpp
class Solution {
public:
    vector<int> findAllPeople(int n, vector<vector<int>>& meetings, int firstPerson) {
        sort(meetings.begin(), meetings.end(), [](auto& a, auto& b) {
            return a[2] < b[2];
        });

        vector<bool> secrets(n, false);
        secrets[0] = secrets[firstPerson] = true;

        int i = 0, m = meetings.size();
        while (i < m) {
            int time = meetings[i][2];
            unordered_map<int, vector<int>> adj;
            unordered_set<int> visited;

            while (i < m && meetings[i][2] == time) {
                int u = meetings[i][0], v = meetings[i][1];
                adj[u].push_back(v);
                adj[v].push_back(u);
                if (secrets[u]) visited.insert(u);
                if (secrets[v]) visited.insert(v);
                i++;
            }

            stack<int> stack(visited.begin(), visited.end());
            while (!stack.empty()) {
                int node = stack.top(); stack.pop();
                for (int& nei : adj[node]) {
                    if (!visited.count(nei)) {
                        visited.insert(nei);
                        stack.push(nei);
                        secrets[nei] = true;
                    }
                }
            }
        }

        vector<int> res;
        for (int j = 0; j < n; j++) {
            if (secrets[j]) res.push_back(j);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m \log m + n)$
- Space complexity: $O(m + n)$

> Where $m$ is the number of meetings and $n$ is the number of people.

## 4. Disjoint Set Union

We can model the secret-sharing as a union-find problem. People who meet at the same time are temporarily connected. If any person in a connected component knows the secret (i.e., is connected to person `0`), everyone in that component learns it. The key insight is that after processing each time slot, we must reset people who did not get connected to person `0`, since the secret only spreads within a time slot.

```cpp
class DSU {
public:
    vector<int> Parent, Size;

    DSU(int n) {
        Parent.resize(n + 1);
        Size.resize(n + 1, 1);
        for (int i = 0; i <= n; i++) {
            Parent[i] = i;
        }
    }

    int find(int node) {
        if (Parent[node] != node) {
            Parent[node] = find(Parent[node]);
        }
        return Parent[node];
    }

    void unionSets(int u, int v) {
        int pu = find(u), pv = find(v);
        if (pu == pv) return;
        if (Size[pu] < Size[pv]) swap(pu, pv);
        Size[pu] += Size[pv];
        Parent[pv] = pu;
    }

    void reset(int node) {
        Parent[node] = node;
        Size[node] = 1;
    }
};

class Solution {
public:
    vector<int> findAllPeople(int n, vector<vector<int>>& meetings, int firstPerson) {
        sort(meetings.begin(), meetings.end(), [](auto &a, auto &b) {
            return a[2] < b[2];
        });
        DSU dsu(n);
        dsu.unionSets(0, firstPerson);

        for (int i = 0; i < meetings.size(); ) {
            int time = meetings[i][2];
            unordered_set<int> group;

            for (; i < meetings.size() && meetings[i][2] == time; i++) {
                int u = meetings[i][0], v = meetings[i][1];
                dsu.unionSets(u, v);
                group.insert(u);
                group.insert(v);
            }

            for (int node : group) {
                if (dsu.find(node) != dsu.find(0)) {
                    dsu.reset(node);
                }
            }
        }

        vector<int> result;
        for (int i = 0; i < n; i++) {
            if (dsu.find(i) == dsu.find(0)) result.push_back(i);
        }
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(m \log m + (m * α(n)))$
- Space complexity:
    - $O(n)$ extra space.
    - $O(m)$ space depending on the sorting algorithm.

> Where $m$ is the number of meetings and $n$ is the number of people.
