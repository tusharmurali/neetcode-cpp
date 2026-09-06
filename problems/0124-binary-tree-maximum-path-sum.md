# 124. Binary Tree Maximum Path Sum

- **Difficulty:** Hard  
- **Pattern:** Trees  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/binary-tree-maximum-path-sum/>  
- **NeetCode:** <https://neetcode.io/problems/binary-tree-maximum-path-sum>  
- **Video:** <https://www.youtube.com/watch?v=Hr5cWUld4vU>  
- **Video approach:** 2. Depth First Search (Optimal)  

[← Back to index](../INDEX.md)

## 1. Depth First Search

For each node, consider it as the **highest point** of a potential path.
A path can pass through a node as:

**left-subtree → node → right-subtree**

So for every node we need two things:

1. **Maximum downward path** from its left child
2. **Maximum downward path** from its right child

A downward path ends at that child and goes only downward (no turning back up).
This is computed using `getMax()`.

Then we compute the best full path through this node:

```
node.val + leftDown + rightDown
```

We try this for **every node** using `DFS` and update the global answer.

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
    int res = INT_MIN;

    int getMax(TreeNode* root) {
        if (!root) return 0;
        int left = getMax(root->left);
        int right = getMax(root->right);
        int path = root->val + std::max(left, right);
        return std::max(0, path);
    }

    void dfs(TreeNode* root) {
        if (!root) return;
        int left = getMax(root->left);
        int right = getMax(root->right);
        res = std::max(res, root->val + left + right);
        dfs(root->left);
        dfs(root->right);
    }

public:
    int maxPathSum(TreeNode* root) {
        dfs(root);
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Depth First Search (Optimal) ▶ video

In the maximum path sum problem, a _path_ can start and end anywhere in the tree, but it must go **downward** at each step (parent → child).

For every node, two values matter:

1. **Max Downward Path** starting at this node
    - This path can only go to _one_ side (left or right).
    - Used by the parent to extend the path upward.
    - Computed as:
        ```
        node.val + max(leftDown, rightDown)
        ```

2. **Max Path Through This Node**
    - This can include **both** left and right downward paths:
        ```
        node.val + leftDown + rightDown
        ```
    - This may form the global maximum path.

While computing `DFS`:

- If a downward path sum is negative, we drop it (take `0`), because adding negative values only makes the path worse.
- At each node, update the global maximum using the "path through this node".
- Return the best downward path to the parent.

This ensures each node is visited once — **O(n)** optimal time.

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
    int maxPathSum(TreeNode* root) {
        int res = root->val;
        dfs(root, res);
        return res;
    }

private:
    int dfs(TreeNode* root, int& res) {
        if (!root) {
            return 0;
        }

        int leftMax = max(dfs(root->left, res), 0);
        int rightMax = max(dfs(root->right, res), 0);

        res = max(res, root->val + leftMax + rightMax);
        return root->val + max(leftMax, rightMax);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0124-binary-tree-maximum-path-sum.cpp` in the NeetCode repo)

```cpp
/*
    Given root of binary tree, return max path sum (seq of adj node values added together)

    Path can only have <= 1 split point, assume curPath has it, so return can't split again

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
    int maxPathSum(TreeNode* root) {
        int maxPath = INT_MIN;
        dfs(root, maxPath);
        return maxPath;
    }
private:
    int dfs(TreeNode* root, int& maxPath) {
        if (root == NULL) {
            return 0;
        }
        
        int left = max(dfs(root->left, maxPath), 0);
        int right = max(dfs(root->right, maxPath), 0);
        
        int curPath = root->val + left + right;
        maxPath = max(maxPath, curPath);
        
        return root->val + max(left, right);
    }
};
```
