# 1059. All Paths from Source Lead to Destination

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/all-paths-from-source-lead-to-destination/>  
- **NeetCode:** <https://neetcode.io/problems/all-paths-from-source-lead-to-destination>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

We need to verify two conditions: every path from the source eventually reaches the destination, and there are no cycles that would create infinite paths. A DFS with cycle detection handles both.

We use a three-color marking scheme. Nodes start unvisited (`white`). When we begin processing a node, we mark it `gray`. When all its descendants have been fully explored, we mark it `black`. If we ever encounter a `gray` node during traversal, we've found a back edge, meaning there's a cycle.

A leaf node (no outgoing edges) must be the destination. If we find any leaf that isn't the destination, or any cycle, we return false.

```cpp
class Solution {
public:
    static const int GRAY = 1;
    static const int BLACK = 2;
    
    bool leadsToDestination(int n, vector<vector<int>>& edges, int source, int destination) {
        vector<vector<int>> graph = buildDigraph(n, edges);
        vector<int> states(n, 0);
        return leadsToDest(graph, source, destination, states);
    }
    
private:
    bool leadsToDest(vector<vector<int>>& graph, int node, int dest, vector<int>& states) {
        if (states[node] != 0) {
            return states[node] == BLACK;
        }
        if (graph[node].size() == 0) {
            return node == dest;
        }
        states[node] = GRAY;
        for (int next_node : graph[node]) {
            if (!leadsToDest(graph, next_node, dest, states)) {
                return false;
            }
        }
        states[node] = BLACK;
        return true;
    }
    
    vector<vector<int>> buildDigraph(int n, vector<vector<int>>& edges) {
        vector<vector<int>> graph(n);
        for (auto& edge : edges) {
            graph[edge[0]].push_back(edge[1]);
        }
        return graph;
    }
};
```

**Complexity**

- Time complexity:
    - Typically for an entire DFS over an input graph, it takes $O(V + E)$ where $V$ represents the number of vertices in the graph and likewise, $E$ represents the number of edges in the graph. In the worst case $E$ can be $O(V^2)$ in case each vertex is connected to every other vertex in the graph. However even in the worst case, we will end up discovering a cycle very early on and prune the recursion tree. If we were to traverse the entire graph, then the complexity would be $O(V^2)$ as the $O(E)$ part would dominate. However, due to pruning and backtracking in case of cycle detection, we end up with an overall time complexity of $O(V)$.

- Space complexity: $O(V + E)$
    - Where $O(E)$ is occupied by the adjacency list and $O(V)$ is occupied by the recursion stack and the color states.

>  Where $V$ represents the number of vertices in the graph and $E$ represents the number of edges in the graph.
