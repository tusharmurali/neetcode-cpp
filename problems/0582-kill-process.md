# 582. Kill Process

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/kill-process/>  
- **NeetCode:** <https://neetcode.io/problems/kill-process>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

When we kill a process, all its descendants must also be killed. This is naturally a tree traversal problem. The brute force approach scans through all processes for each recursive call to find children of the current process. While this works, it repeatedly searches the entire list, making it inefficient for large inputs.

```cpp
class Solution {
public:
    vector<int> killProcess(vector<int>& pid, vector<int>& ppid, int kill) {
        vector<int> result;
        if (kill == 0) return result;

        result.push_back(kill);
        for (int i = 0; i < ppid.size(); i++) {
            if (ppid[i] == kill) {
                vector<int> children = killProcess(pid, ppid, pid[i]);
                result.insert(result.end(), children.begin(), children.end());
            }
        }

        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n^2)$
- Space complexity: $O(n)$

> Where $n$ is the length of the `pid` and `ppid`.

## 2. Tree Simulation

Instead of repeatedly scanning arrays, we can build an actual tree structure upfront. By creating node objects with parent-child relationships, we transform the implicit tree (represented by parallel arrays) into an explicit one. Once built, collecting all descendants becomes a simple tree traversal.

```cpp
class Solution {
    struct Node {
        int val;
        vector<Node*> children;
        Node(int v) : val(v) {}
    };

public:
    vector<int> killProcess(vector<int>& pid, vector<int>& ppid, int kill) {
        unordered_map<int, Node*> mp;
        for (int id : pid) {
            mp[id] = new Node(id);
        }

        for (int i = 0; i < ppid.size(); i++) {
            if (ppid[i] > 0) {
                mp[ppid[i]]->children.push_back(mp[pid[i]]);
            }
        }

        vector<int> result;
        result.push_back(kill);
        getAllChildren(mp[kill], result);
        return result;
    }

private:
    void getAllChildren(Node* node, vector<int>& result) {
        for (Node* child : node->children) {
            result.push_back(child->val);
            getAllChildren(child, result);
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the length of the `pid` and `ppid`.

## 3. HashMap + Depth First Search

We can simplify the tree simulation by using a hash map that directly maps each parent to its list of children. This avoids creating node objects while still giving us `O(1)` access to any process's children. The DFS traversal then becomes straightforward.

```cpp
class Solution {
public:
    vector<int> killProcess(vector<int>& pid, vector<int>& ppid, int kill) {
        unordered_map<int, vector<int>> map;
        for (int i = 0; i < ppid.size(); i++) {
            if (ppid[i] > 0) {
                map[ppid[i]].push_back(pid[i]);
            }
        }

        vector<int> result;
        result.push_back(kill);
        getAllChildren(map, result, kill);
        return result;
    }

private:
    void getAllChildren(unordered_map<int, vector<int>>& map, vector<int>& result, int kill) {
        if (map.find(kill) != map.end()) {
            for (int child_id : map[kill]) {
                result.push_back(child_id);
                getAllChildren(map, result, child_id);
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the length of the `pid` and `ppid`.

## 4. HashMap + Breadth First Search

BFS offers an alternative to DFS for traversing the process tree. Instead of going deep into one branch before backtracking, BFS processes all children at the current level before moving to the next. Both approaches yield the same result but BFS can be more intuitive when thinking about the spread of the kill signal.

```cpp
class Solution {
public:
    vector<int> killProcess(vector<int>& pid, vector<int>& ppid, int kill) {
        unordered_map<int, vector<int>> map;
        for (int i = 0; i < ppid.size(); i++) {
            if (ppid[i] > 0) {
                map[ppid[i]].push_back(pid[i]);
            }
        }

        queue<int> q;
        vector<int> result;
        q.push(kill);
        while (!q.empty()) {
            int r = q.front();
            q.pop();
            result.push_back(r);
            if (map.find(r) != map.end()) {
                for (int child_id : map[r]) {
                    q.push(child_id);
                }
            }
        }

        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the length of the `pid` and `ppid`.
