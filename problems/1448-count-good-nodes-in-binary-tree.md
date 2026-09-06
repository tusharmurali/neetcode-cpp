# 1448. Count Good Nodes In Binary Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/count-good-nodes-in-binary-tree/>  
- **NeetCode:** <https://neetcode.io/problems/count-good-nodes-in-binary-tree>  
- **Video:** <https://www.youtube.com/watch?v=7cp5imvDzl4>  
- **Video approach:** 1. Depth First Search  

[← Back to index](../INDEX.md)

## 1. Depth First Search ▶ video

A node is “good” if on the path from the root to that node, **no earlier node has a value greater than it**.  
So while traversing the tree, we just need to carry the **maximum value seen so far** on the current path.

If the current node’s value ≥ that maximum → it is a good node.

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
    int goodNodes(TreeNode* root) {
        return dfs(root, root->val);
    }

private:
    int dfs(TreeNode* node, int maxVal) {
        if (!node) {
            return 0;
        }

        int res = (node->val >= maxVal) ? 1 : 0;
        maxVal = max(maxVal, node->val);
        res += dfs(node->left, maxVal);
        res += dfs(node->right, maxVal);
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Breadth First Search

A node is “good” if along the path from the root to that node, **no earlier node has a value greater than it**.  
Using BFS, we can traverse level by level while carrying the **maximum value seen so far** for each path.  
Whenever we visit a node, we compare its value with that max — if it's greater or equal, this node is good.

Each child inherits the updated maximum of its own path.

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
    int goodNodes(TreeNode* root) {
        int res = 0;
        queue<pair<TreeNode*, int>> q;
        q.push({root, -INT_MAX});

        while (!q.empty()) {
            auto [node, maxval] = q.front();
            q.pop();
            if (node->val >= maxval) {
                res++;
            }
            if (node->left) {
                q.push({node->left, max(maxval, node->val)});
            }
            if (node->right) {
                q.push({node->right, max(maxval, node->val)});
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/1448-count-good-nodes-in-binary-tree.cpp` in the NeetCode repo)

```cpp
/*
    Given binary tree, node is "good" if path from root has no nodes > X, return # of "good"

    Maintain greatest value seen so far on a path, if further node >= this max, "good" node

    Time: O(n)
    Space: O(n)
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
    int goodNodes(TreeNode* root) {
        int result = 0;
        dfs(root, root->val, result);
        return result;
    }
private:
    void dfs(TreeNode* root, int maxSoFar, int& result) {
        if (root == NULL) {
            return;
        }
        
        if (root->val >= maxSoFar) {
            result++;
        }
        
        dfs(root->left, max(maxSoFar, root->val), result);
        dfs(root->right, max(maxSoFar, root->val), result);
    }
};
```
