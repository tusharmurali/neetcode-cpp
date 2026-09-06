# 1993. Operations On Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/operations-on-tree/>  
- **NeetCode:** <https://neetcode.io/problems/operations-on-tree>  
- **Video:** <https://www.youtube.com/watch?v=qK4PtjrVD0U>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

We need to simulate a locking system on a tree structure. The key insight is that `lock` and `unlock` are simple O(1) operations since they only check and modify a single node. The `upgrade` operation is more complex: it requires checking all ancestors (no locks allowed) and all descendants (at least one lock required, then unlock all).

For the ancestor check, we traverse up the parent chain. For the descendant check and unlock, we use `dfs` to visit all nodes in the subtree, counting and clearing any locks.

```cpp
class LockingTree {
private:
    vector<int> parent;
    vector<vector<int>> child;
    vector<int> locked;

public:
    LockingTree(vector<int>& parent) : parent(parent), locked(parent.size()) {
        int n = parent.size();
        child.resize(n);
        for (int node = 1; node < n; node++) {
            child[parent[node]].push_back(node);
        }
    }

    bool lock(int num, int user) {
        if (locked[num]) {
            return false;
        }
        locked[num] = user;
        return true;
    }

    bool unlock(int num, int user) {
        if (locked[num] != user) {
            return false;
        }
        locked[num] = 0;
        return true;
    }

    bool upgrade(int num, int user) {
        int node = num;
        while (node != -1) {
            if (locked[node]) {
                return false;
            }
            node = parent[node];
        }

        int lockedCount = dfs(num);
        if (lockedCount > 0) {
            locked[num] = user;
            return true;
        }
        return false;
    }

private:
    int dfs(int node) {
        int lockedCount = 0;
        if (locked[node]) {
            lockedCount++;
            locked[node] = 0;
        }
        for (int& nei : child[node]) {
            lockedCount += dfs(nei);
        }
        return lockedCount;
    }
};
```

**Complexity**

- Time complexity:
    - $O(n)$ time for initialization.
    - $O(1)$ time for each $lock()$ and $unlock()$ function call.
    - $O(n)$ time for each $upgrade()$ function call.
- Space complexity: $O(n)$

## 2. Breadth First Search

This solution replaces the recursive `dfs` for the descendant traversal with an iterative BFS using a queue. The logic remains identical: `lock` and `unlock` are O(1) operations, while `upgrade` requires ancestor and descendant checks.

BFS processes nodes level by level, which can be more cache-friendly in some cases and avoids potential stack overflow issues with very deep trees.

```cpp
class LockingTree {
private:
    vector<int> parent;
    vector<vector<int>> child;
    vector<int> locked;

public:
    LockingTree(vector<int>& parent) : parent(parent), locked(parent.size()) {
        int n = parent.size();
        child.resize(n);
        for (int node = 1; node < n; node++) {
            child[parent[node]].push_back(node);
        }
    }

    bool lock(int num, int user) {
        if (locked[num]) {
            return false;
        }
        locked[num] = user;
        return true;
    }

    bool unlock(int num, int user) {
        if (locked[num] != user) {
            return false;
        }
        locked[num] = 0;
        return true;
    }

    bool upgrade(int num, int user) {
        int node = num;
        while (node != -1) {
            if (locked[node]) {
                return false;
            }
            node = parent[node];
        }

        int lockedCount = 0;
        queue<int> q;
        q.push(num);

        while (!q.empty()) {
            node = q.front(); q.pop();
            if (locked[node]) {
                locked[node] = 0;
                lockedCount++;
            }
            for (int nei : child[node]) {
                q.push(nei);
            }
        }

        if (lockedCount > 0) {
            locked[num] = user;
            return true;
        }
        return false;
    }
};
```

**Complexity**

- Time complexity:
    - $O(n)$ time for initialization.
    - $O(1)$ time for each $lock()$ and $unlock()$ function call.
    - $O(n)$ time for each $upgrade()$ function call.
- Space complexity: $O(n)$

## 3. Iterative DFS

This approach converts the recursive `dfs` into an iterative version using an explicit stack. This is useful when you want to avoid recursion overhead or potential stack overflow on very large trees, while maintaining the depth-first traversal order.

The core logic for all three operations remains unchanged from the recursive `dfs` solution.

```cpp
class LockingTree {
private:
    vector<int> parent;
    vector<vector<int>> child;
    vector<int> locked;

public:
    LockingTree(vector<int>& parent) : parent(parent), locked(parent.size()) {
        int n = parent.size();
        child.resize(n);
        for (int node = 1; node < n; node++) {
            child[parent[node]].push_back(node);
        }
    }

    bool lock(int num, int user) {
        if (locked[num]) {
            return false;
        }
        locked[num] = user;
        return true;
    }

    bool unlock(int num, int user) {
        if (locked[num] != user) {
            return false;
        }
        locked[num] = 0;
        return true;
    }

    bool upgrade(int num, int user) {
        int node = num;
        while (node != -1) {
            if (locked[node]) {
                return false;
            }
            node = parent[node];
        }

        int lockedCount = 0;
        stack<int> stk;
        stk.push(num);

        while (!stk.empty()) {
            node = stk.top(); stk.pop();
            if (locked[node]) {
                locked[node] = 0;
                lockedCount++;
            }
            for (int& nei : child[node]) {
                stk.push(nei);
            }
        }

        if (lockedCount > 0) {
            locked[num] = user;
            return true;
        }
        return false;
    }
};
```

**Complexity**

- Time complexity:
    - $O(n)$ time for initialization.
    - $O(1)$ time for each $lock()$ and $unlock()$ function call.
    - $O(n)$ time for each $upgrade()$ function call.
- Space complexity: $O(n)$
