# 958. Check Completeness of a Binary Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/check-completeness-of-a-binary-tree/>  
- **NeetCode:** <https://neetcode.io/problems/check-completeness-of-a-binary-tree>  
- **Video:** <https://www.youtube.com/watch?v=olbiZ-EOSig>  

[← Back to index](../INDEX.md)

## 1. Breadth First Search

In a complete binary tree, all nodes are as far left as possible, with no gaps. If we traverse level by level and encounter a null node, all subsequent nodes in the traversal must also be null. If we find any non-null node after a null, the tree is not complete.

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    bool isCompleteTree(TreeNode* root) {
        queue<TreeNode*> q;
        q.push(root);

        while (!q.empty()) {
            TreeNode* node = q.front();
            q.pop();
            if (node) {
                q.push(node->left);
                q.push(node->right);
            } else {
                while (!q.empty()) {
                    if (q.front()) {
                        return false;
                    }
                    q.pop();
                }
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Breadth First Search (Optimal)

This is a cleaner version of the BFS approach. Instead of draining the queue after seeing `null`, we use a flag to track whether a `null` has been seen. If we encounter a non-null node after the flag is set, the tree is incomplete.

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    bool isCompleteTree(TreeNode* root) {
        queue<TreeNode*> q;
        q.push(root);
        bool nullSeen = false;

        while (!q.empty()) {
            TreeNode* node = q.front();
            q.pop();
            if (node) {
                if (nullSeen) return false;
                q.push(node->left);
                q.push(node->right);
            } else {
                nullSeen = true;
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Depth First Search (Two Pass)

A complete binary tree with `n` nodes has a specific property: if we number nodes starting from 0 (root) where a node at index `i` has children at 2`i`+1 and 2`i`+2, then every node's index must be less than `n`. First count all nodes, then verify that no node has an index >= `n`.

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    int countNodes(TreeNode* root) {
        if (!root) return 0;
        return 1 + countNodes(root->left) + countNodes(root->right);
    }

    bool dfs(TreeNode* node, int index, int n) {
        if (!node) return true;
        if (index >= n) return false;
        return dfs(node->left, 2 * index + 1, n) && dfs(node->right, 2 * index + 2, n);
    }

    bool isCompleteTree(TreeNode* root) {
        int n = countNodes(root);
        return dfs(root, 0, n);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 4. Depth First Search (Optimal)

We can verify completeness in a single DFS pass by tracking the tree's height and whether we have seen a "short" path (one that ends before the maximum depth). In a complete tree, all paths to null nodes at the deepest level must appear before any paths ending one level higher, when traversing left to right.

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    int treeHgt = 0;
    bool nullSeen = false;

    bool dfs(TreeNode* node, int hgt) {
        if (!node) {
            if (treeHgt == 0) {
                treeHgt = hgt;
            } else if (hgt == treeHgt - 1) {
                nullSeen = true;
            } else if (hgt != treeHgt) {
                return false;
            }
            return !(hgt == treeHgt && nullSeen);
        }

        return dfs(node->left, hgt + 1) && dfs(node->right, hgt + 1);
    }

    bool isCompleteTree(TreeNode* root) {
        return dfs(root, 0);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## Standalone solution file (`cpp/0958-check-completeness-of-a-binary-tree.cpp` in the NeetCode repo)

```cpp
/*
  Given the root of a binary tree, determine if it is a complete binary tree.

  In a complete binary tree, every level, except possibly the last, is completely filled,
  and all nodes in the last level are as far left as possible. It can have between 1 and 2h
  nodes inclusive at the last level h.

  Ex. Input: root = [1,2,3,4,5,6]
      Output: true
      Explanation: Every level before the last is full (ie. levels with node-values {1} and {2, 3}), 
      and all nodes in the last level ({4, 5, 6}) are as far left as possible.

  Time  : O(N);
  Space : O(N);
*/

/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    bool isCompleteTree(TreeNode* root) {
        queue <TreeNode*> q;
        q.push(root);
        bool isNull = false;

        while(!q.empty()) {
            TreeNode * front = q.front();
            if(!front)
                isNull = true;
            else {
                if(isNull)
                    return false;
                q.push(front -> left);
                q.push(front -> right);
            }
            q.pop();
        }
        return true;
    }
};
```
