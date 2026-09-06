# 236. Lowest Common Ancestor of a Binary Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/>  
- **NeetCode:** <https://neetcode.io/problems/lowest-common-ancestor-of-a-binary-tree>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

The lowest common ancestor (LCA) is the deepest node that has both `p` and `q` as descendants. We traverse the tree and track whether each subtree contains `p`, `q`, or both. The first node where we find both targets in its subtree (including itself) is the LCA. Once found, we can stop searching.

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        lca = nullptr;
        dfs(root, p, q);
        return lca;
    }

private:
    TreeNode* lca;

    pair<bool,bool> dfs(TreeNode* node, TreeNode* p, TreeNode* q) {
        if (!node || lca) {
            return {false, false};
        }
        auto left = dfs(node->left, p, q);
        auto right = dfs(node->right, p, q);
        bool foundP = left.first || right.first || node == p;
        bool foundQ = left.second || right.second || node == q;
        if (foundP && foundQ && !lca) {
            lca = node;
        }
        return {foundP, foundQ};
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Depth First Search (Optimal)

We can simplify the approach by returning the node itself rather than boolean flags. If a node is `p` or `q`, we return it immediately. Otherwise, we recursively search both subtrees. If both return non-`null` values, the current node must be the LCA. If only one side returns a value, we propagate that up since both targets are in that subtree.

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        if (!root || root == p || root == q) {
            return root;
        }
        TreeNode* left = lowestCommonAncestor(root->left, p, q);
        TreeNode* right = lowestCommonAncestor(root->right, p, q);
        if (left && right) {
            return root;
        }
        return left ? left : right;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Breadth First Search

Instead of recursion, we can use BFS to build a parent pointer map for each node. Once we have parent pointers, we trace the path from `p` to the root and store all ancestors. Then we trace from `q` upward until we hit a node that's already in `p`'s ancestor set. That node is the LCA.

```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        if (!root) return nullptr;
        unordered_map<TreeNode*, TreeNode*> parent;
        queue<TreeNode*> queue;
        parent[root] = nullptr;
        queue.push(root);
        while (!parent.count(p) || !parent.count(q)) {
            TreeNode* node = queue.front(); queue.pop();
            if (node->left) {
                parent[node->left] = node;
                queue.push(node->left);
            }
            if (node->right) {
                parent[node->right] = node;
                queue.push(node->right);
            }
        }

        unordered_set<TreeNode*> ancestors;
        while (p) {
            ancestors.insert(p);
            p = parent[p];
        }
        while (!ancestors.count(q)) {
            q = parent[q];
        }
        return q;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
