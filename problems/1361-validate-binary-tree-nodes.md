# 1361. Validate Binary Tree Nodes

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/validate-binary-tree-nodes/>  
- **NeetCode:** <https://neetcode.io/problems/validate-binary-tree-nodes>  
- **Video:** <https://www.youtube.com/watch?v=Mw67DTgUEqk>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

A valid binary tree must have exactly one root (a node with no parent), every other node must have exactly one parent, and all nodes must be reachable from the root without cycles. The key insight is that we can identify the root as the only node that never appears as a child, then use DFS to verify that we can reach all n nodes without revisiting any node.

```cpp
class Solution {
public:
    unordered_set<int> visit;

    bool validateBinaryTreeNodes(int n, vector<int>& leftChild, vector<int>& rightChild) {
        unordered_set<int> hasParent;
        for (int c : leftChild) if (c != -1) hasParent.insert(c);
        for (int c : rightChild) if (c != -1) hasParent.insert(c);
        if (hasParent.size() == n) return false;

        int root = -1;
        for (int i = 0; i < n; i++) {
            if (!hasParent.count(i)) {
                root = i;
                break;
            }
        }
        return dfs(root, leftChild, rightChild) && visit.size() == n;
    }

private:
    bool dfs(int i, vector<int>& leftChild, vector<int>& rightChild) {
        if (i == -1) return true;
        if (visit.count(i)) return false;
        visit.insert(i);
        return dfs(leftChild[i], leftChild, rightChild) &&
               dfs(rightChild[i], leftChild, rightChild);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Breadth First Search

Instead of using recursion, we can use BFS to traverse the tree level by level. The approach uses indegree counting: in a valid binary tree, every node except the root has exactly one incoming edge (one parent). By tracking indegrees, we can detect nodes with multiple parents and identify the unique root.

```cpp
class Solution {
public:
    bool validateBinaryTreeNodes(int n, vector<int>& leftChild, vector<int>& rightChild) {
        vector<int> indegree(n, 0);
        for (int i = 0; i < n; i++) {
            if (leftChild[i] != -1) {
                if (++indegree[leftChild[i]] > 1) return false;
            }
            if (rightChild[i] != -1) {
                if (++indegree[rightChild[i]] > 1) return false;
            }
        }

        int root = -1;
        for (int i = 0; i < n; i++) {
            if (indegree[i] == 0) {
                if (root != -1) return false;
                root = i;
            }
        }

        if (root == -1) return false;

        int count = 0;
        queue<int> q;
        q.push(root);

        while (!q.empty()) {
            int i = q.front();q.pop();
            count++;
            if (leftChild[i] != -1) q.push(leftChild[i]);
            if (rightChild[i] != -1) q.push(rightChild[i]);
        }
        return count == n;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Iterative DFS

This approach combines the indegree validation from BFS with an iterative stack-based traversal instead of recursion. Using a stack avoids potential stack overflow issues for deep trees while maintaining the same logical flow as recursive DFS.

```cpp
class Solution {
public:
    bool validateBinaryTreeNodes(int n, vector<int>& leftChild, vector<int>& rightChild) {
        vector<int> indegree(n, 0);
        for (int i = 0; i < n; i++) {
            if (leftChild[i] != -1 && ++indegree[leftChild[i]] > 1) return false;
            if (rightChild[i] != -1 && ++indegree[rightChild[i]] > 1) return false;
        }

        int root = -1;
        for (int i = 0; i < n; i++) {
            if (indegree[i] == 0) {
                if (root != -1) return false;
                root = i;
            }
        }

        if (root == -1) return false;

        int count = 0;
        stack<int> stk;
        stk.push(root);

        while (!stk.empty()) {
            int node = stk.top(); stk.pop();
            count++;
            if (leftChild[node] != -1) stk.push(leftChild[node]);
            if (rightChild[node] != -1) stk.push(rightChild[node]);
        }
        return count == n;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Disjoint Set Union

Union-Find provides an elegant way to detect cycles and verify connectivity. The key insight is that in a valid tree, connecting a parent to a child should always merge two separate components. If the child already has a parent (its root is not itself) or connecting them would create a cycle (same root), the structure is invalid.

```cpp
class DSU {
public:
    vector<int> Parent;
    int Components;

    DSU(int n) {
        Parent.resize(n);
        iota(Parent.begin(), Parent.end(), 0);
        Components = n;
    }

    int find(int node) {
        if (Parent[node] != node) {
            Parent[node] = find(Parent[node]);
        }
        return Parent[node];
    }

    bool unionSets(int parent, int child) {
        int parentRoot = find(parent);
        int childRoot = find(child);
        if (childRoot != child || parentRoot == childRoot) {
            return false;
        }

        Components--;
        Parent[childRoot] = parentRoot;
        return true;
    }
};

class Solution {
public:
    bool validateBinaryTreeNodes(int n, vector<int>& leftChild, vector<int>& rightChild) {
        DSU dsu(n);

        for (int parent = 0; parent < n; parent++) {
            for (int child : {leftChild[parent], rightChild[parent]}) {
                if (child == -1) continue;
                if (!dsu.unionSets(parent, child)) return false;
            }
        }

        return dsu.Components == 1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
