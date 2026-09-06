# 133. Clone Graph

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/clone-graph/>  
- **NeetCode:** <https://neetcode.io/problems/clone-graph>  
- **Video:** <https://www.youtube.com/watch?v=mQeF6bN8hMk>  
- **Video approach:** 1. Depth First Seacrh  

[← Back to index](../INDEX.md)

## 1. Depth First Seacrh ▶ video

The graph may contain **cycles**, so we cannot simply copy nodes recursively without remembering what we've already copied.  
To handle this, we use a **map (old → new)**:

- When we first see a node, we create its copy.
- If we see the same node again, we reuse the already-created copy.
- This avoids infinite loops and ensures each node is cloned exactly once.

Depth First Search (DFS) helps us explore and clone all connected nodes.

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    vector<Node*> neighbors;
    Node() {
        val = 0;
        neighbors = vector<Node*>();
    }
    Node(int _val) {
        val = _val;
        neighbors = vector<Node*>();
    }
    Node(int _val, vector<Node*> _neighbors) {
        val = _val;
        neighbors = _neighbors;
    }
};
*/

class Solution {
public:
    Node* cloneGraph(Node* node) {
        map<Node*, Node*> oldToNew;
        return dfs(node, oldToNew);
    }

    Node* dfs(Node* node, map<Node*, Node*>& oldToNew) {
        if (node == nullptr) {
            return nullptr;
        }

        if (oldToNew.count(node)) {
            return oldToNew[node];
        }

        Node* copy = new Node(node->val);
        oldToNew[node] = copy;

        for (Node* nei : node->neighbors) {
            copy->neighbors.push_back(dfs(nei, oldToNew));
        }

        return copy;
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## 2. Breadth First Search

The graph can have **cycles**, so while cloning we must avoid creating duplicate nodes or looping forever.  
Using **Breadth First Search (BFS)**, we explore the graph level by level and keep a **map from original nodes to their clones**.

- When a node is first seen, create its clone and store it in the map.
- For every neighbor, ensure its clone exists, then connect the cloned nodes.
- The map guarantees each node is cloned only once.

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    vector<Node*> neighbors;
    Node() {
        val = 0;
        neighbors = vector<Node*>();
    }
    Node(int _val) {
        val = _val;
        neighbors = vector<Node*>();
    }
    Node(int _val, vector<Node*> _neighbors) {
        val = _val;
        neighbors = _neighbors;
    }
};
*/

class Solution {
public:
    Node* cloneGraph(Node* node) {
        if (!node) return nullptr;
        unordered_map<Node*, Node*> oldToNew;
        queue<Node*> q;
        oldToNew[node] = new Node(node->val);
        q.push(node);

        while (!q.empty()) {
            Node* cur = q.front();
            q.pop();
            for (Node* nei : cur->neighbors) {
                if (oldToNew.find(nei) == oldToNew.end()) {
                    oldToNew[nei] = new Node(nei->val);
                    q.push(nei);
                }
                oldToNew[cur]->neighbors.push_back(oldToNew[nei]);
            }
        }
        return oldToNew[node];
    }
};
```

**Complexity**

- Time complexity: $O(V + E)$
- Space complexity: $O(V)$

> Where $V$ is the number of vertices and $E$ is the number of edges.

## Standalone solution file (`cpp/0133-clone-graph.cpp` in the NeetCode repo)

```cpp
/*
    Given ref of a node in connected undirected graph, return deep copy

    Both BFS & DFS work, map original node to its copy

    Time: O(m + n)
    Space: O(n)
*/

/*
// Definition for a Node.
class Node {
public:
    int val;
    vector<Node*> neighbors;
    Node() {
        val = 0;
        neighbors = vector<Node*>();
    }
    Node(int _val) {
        val = _val;
        neighbors = vector<Node*>();
    }
    Node(int _val, vector<Node*> _neighbors) {
        val = _val;
        neighbors = _neighbors;
    }
};
*/

// class Solution {
// public:
//     Node* cloneGraph(Node* node) {
//         if (node == NULL) {
//             return NULL;
//         } 
//         if (m.find(node) == m.end()) {
//             m[node] = new Node(node->val);
//             for (int i = 0; i < node->neighbors.size(); i++) {
//                 Node* neighbor = node->neighbors[i];
//                 m[node]->neighbors.push_back(cloneGraph(neighbor));
//             }
//         }
//         return m[node];
//     }
// private:
//     unordered_map<Node*, Node*> m;
// };

class Solution {
public:
    Node* cloneGraph(Node* node) {
        if (node == NULL) {
            return NULL;
        }
        
        Node* copy = new Node(node->val);
        m[node] = copy;
        
        queue<Node*> q;
        q.push(node);
        
        while (!q.empty()) {
            Node* curr = q.front();
            q.pop();
            
            for (int i = 0; i < curr->neighbors.size(); i++) {
                Node* neighbor = curr->neighbors[i];
                
                if (m.find(neighbor) == m.end()) {
                    m[neighbor] = new Node(neighbor->val);
                    q.push(neighbor);
                }
                
                m[curr]->neighbors.push_back(m[neighbor]);
            }
        }
        
        return copy;
    }
private:
    unordered_map<Node*, Node*> m;
};
```
