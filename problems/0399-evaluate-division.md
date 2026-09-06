# 399. Evaluate Division

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/evaluate-division/>  
- **NeetCode:** <https://neetcode.io/problems/evaluate-division>  
- **Video:** <https://www.youtube.com/watch?v=Uei1fwDoyKk>  

[← Back to index](../INDEX.md)

## 1. Breadth First Search

We can think of each equation `a / b = value` as a directed edge from `a` to `b` with weight `value`, and an edge from `b` to `a` with weight `1/value`. This transforms the problem into a graph traversal: to evaluate `x / y`, we need to find a path from `x` to `y` and multiply the edge weights along that path.

BFS works well here because we explore all neighbors at the current distance before moving further. Starting from the source variable, we track the accumulated product as we traverse. When we reach the target, that accumulated product gives us the answer.

```cpp
class Solution {
public:
    vector<double> calcEquation(vector<vector<string>>& equations, vector<double>& values, vector<vector<string>>& queries) {
        unordered_map<string, vector<pair<string, double>>> adj; // Map a -> list of [b, a/b]

        for (int i = 0; i < equations.size(); i++) {
            string a = equations[i][0];
            string b = equations[i][1];
            adj[a].emplace_back(b, values[i]);
            adj[b].emplace_back(a, 1.0 / values[i]);
        }

        vector<double> res;
        for (const auto& query : queries) {
            string src = query[0];
            string target = query[1];
            res.push_back(bfs(src, target, adj));
        }

        return res;
    }

private:
    double bfs(const string& src, const string& target, unordered_map<string, vector<pair<string, double>>>& adj) {
        if (!adj.count(src) || !adj.count(target)) {
            return -1.0;
        }

        queue<pair<string, double>> q;
        unordered_set<string> visited;
        q.emplace(src, 1.0);
        visited.insert(src);

        while (!q.empty()) {
            auto [node, weight] = q.front();
            q.pop();

            if (node == target) {
                return weight;
            }

            for (const auto& [nei, neiWeight] : adj[node]) {
                if (!visited.count(nei)) {
                    visited.insert(nei);
                    q.emplace(nei, weight * neiWeight);
                }
            }
        }

        return -1.0;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(n + m)$

> Where $n$ is the number of unique strings and $m$ is the number of queries.

## 2. Depth First Search

Like BFS, DFS also explores paths through the graph, but it goes deep before backtracking. We recursively explore from the source, multiplying edge weights as we go. The first complete path we find from source to target gives us the answer.

DFS is often simpler to implement recursively. At each step, we check if we have reached the target. If not, we try all unvisited neighbors, and if any recursive call succeeds (returns a non-negative result), we multiply by the current edge weight and return.

```cpp
class Solution {
public:
    vector<double> calcEquation(vector<vector<string>>& equations, vector<double>& values, vector<vector<string>>& queries) {
        unordered_map<string, vector<pair<string, double>>> adj; // Map a -> list of [b, a/b]

        for (int i = 0; i < equations.size(); i++) {
            string a = equations[i][0];
            string b = equations[i][1];
            adj[a].emplace_back(b, values[i]);
            adj[b].emplace_back(a, 1.0 / values[i]);
        }

        vector<double> res;
        for (const auto& query : queries) {
            string src = query[0];
            string target = query[1];
            res.push_back(dfs(src, target, adj, unordered_set<string>()));
        }

        return res;
    }

private:
    double dfs(const string& src, const string& target, unordered_map<string, vector<pair<string, double>>>& adj, unordered_set<string> visited) {
        if (!adj.count(src) || !adj.count(target)) {
            return -1.0;
        }
        if (src == target) {
            return 1.0;
        }

        visited.insert(src);

        for (const auto& [nei, weight] : adj[src]) {
            if (!visited.count(nei)) {
                double result = dfs(nei, target, adj, visited);
                if (result != -1.0) {
                    return weight * result;
                }
            }
        }

        return -1.0;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(n + m)$

> Where $n$ is the number of unique strings and $m$ is the number of queries.

## 3. Disjoint Set Union

Union-Find can track connected components, but here we need to track ratios between variables. The key insight is to store each variable's weight relative to its root. When we union two variables `x` and `y` with ratio `x/y = value`, we connect their roots and adjust weights so that the ratio relationship is preserved.

To query `x/y`, we find both roots. If they differ, no path exists. If they match, the answer is `weight[x] / weight[y]`, since both weights are relative to the same root.

```cpp
class UnionFind {
    unordered_map<string, string> parent;
    unordered_map<string, double> weight;

public:
    void add(const string& x) {
        if (parent.find(x) == parent.end()) {
            parent[x] = x;
            weight[x] = 1.0;
        }
    }

    string find(const string& x) {
        if (x != parent[x]) {
            string origParent = parent[x];
            parent[x] = find(parent[x]);
            weight[x] *= weight[origParent];
        }
        return parent[x];
    }

    void unionSets(const string& x, const string& y, double value) {
        add(x);
        add(y);
        string rootX = find(x);
        string rootY = find(y);

        if (rootX != rootY) {
            parent[rootX] = rootY;
            weight[rootX] = value * weight[y] / weight[x];
        }
    }

    double getRatio(const string& x, const string& y) {
        if (parent.find(x) == parent.end() || parent.find(y) == parent.end() || find(x) != find(y)) {
            return -1.0;
        }
        return weight[x] / weight[y];
    }
};

class Solution {
public:
    vector<double> calcEquation(vector<vector<string>>& equations, vector<double>& values, vector<vector<string>>& queries) {
        UnionFind uf;

        for (int i = 0; i < equations.size(); i++) {
            string a = equations[i][0];
            string b = equations[i][1];
            uf.unionSets(a, b, values[i]);
        }

        vector<double> result;
        for (const auto& query : queries) {
            string a = query[0];
            string b = query[1];
            result.push_back(uf.getRatio(a, b));
        }

        return result;
    }
};
```

**Complexity**

- Time complexity: $O((m + n)\log n)$
- Space complexity: $O(n + m)$

> Where $n$ is the number of unique strings and $m$ is the number of queries.

## 4. Floyd Warshall

Floyd-Warshall computes shortest paths between all pairs of nodes. Here, instead of distances, we compute the product of ratios. If we know `a/b` and `b/c`, then `a/c = (a/b) * (b/c)`. We precompute all such transitive ratios.

This approach trades query time for preprocessing time. After running Floyd-Warshall, each query becomes a simple lookup.

```cpp
class Solution {
public:
    vector<double> calcEquation(vector<vector<string>>& equations, vector<double>& values, vector<vector<string>>& queries) {
        unordered_map<string, unordered_map<string, double>> graph;

        for (int i = 0; i < equations.size(); i++) {
            string a = equations[i][0];
            string b = equations[i][1];
            double value = values[i];
            graph[a][b] = value;
            graph[b][a] = 1.0 / value;
        }

        for (const auto& pair : graph) {
            const string& k = pair.first;
            for (const auto& pair1 : graph[k]) {
                const string& i = pair1.first;
                for (const auto& pair2 : graph[k]) {
                    const string& j = pair2.first;
                    if (!graph[i].count(j)) {
                        graph[i][j] = graph[i][k] * graph[k][j];
                    }
                }
            }
        }

        vector<double> result;
        for (const auto& query : queries) {
            const string& a = query[0];
            const string& b = query[1];
            if (!graph.count(a) || !graph[a].count(b)) {
                result.push_back(-1.0);
            } else {
                result.push_back(graph[a][b]);
            }
        }

        return result;
    }
};
```

**Complexity**

- Time complexity: $O(m + n ^ 3)$
- Space complexity: $O(n ^ 2 + m)$

> Where $n$ is the number of unique strings and $m$ is the number of queries.

## Standalone solution file (`cpp/0399-evaluate-division.cpp` in the NeetCode repo)

```cpp
class Solution {
    unordered_map<string, vector<pair<string, double>>> graph;
    unordered_map<string, bool> visited;
    double queryAns;

public:
    bool dfs(string startNode, string endNode, double runningProduct){
        if(graph.find(startNode) == graph.end() || graph.find(endNode) == graph.end()) {
            return false;
        }
        
        if(startNode == endNode && graph.find(startNode)!=graph.end()) {
            queryAns = runningProduct;
            return true;
            
        }
        
        bool tempAns = false;
        visited[startNode] = true;
        
        for(int i = 0; i < graph[startNode].size(); i++){
            if(!visited[graph[startNode][i].first]){
                tempAns = dfs(graph[startNode][i].first, endNode, runningProduct*graph[startNode][i].second);
                if(tempAns){
                    break;
                }
            }
        }
        visited[startNode] = false;
        
        return tempAns;
    }
    
    vector<double> calcEquation(vector<vector<string>>& equations, vector<double>& values, vector<vector<string>>& queries) {
        int n = equations.size(), m = queries.size();
        vector<double> ans(m);
        
        for(int i = 0; i < n ; i++){
            
            graph[equations[i][0]].push_back({equations[i][1], values[i]});
            graph[equations[i][1]].push_back({equations[i][0], 1/values[i]});
            visited[equations[i][0]] = false;
            visited[equations[i][1]] = false;

        }
        
        for(int i = 0; i < m ; i++){
            
            queryAns = 1;
            bool pathFound = dfs(queries[i][0], queries[i][1], 1);            
            if(pathFound) ans[i] = queryAns;
            else ans[i] = -1;
            
        }
        return ans;
    }
};
```
