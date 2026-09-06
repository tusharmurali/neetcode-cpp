# 669. Trim a Binary Search Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/trim-a-binary-search-tree/>  
- **NeetCode:** <https://neetcode.io/problems/trim-a-binary-search-tree>  
- **Video:** <https://www.youtube.com/watch?v=jwt5mTjEXGc>  
- **Video approach:** 1. Depth First Search (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Depth First Search ▶ video

The BST property gives us a powerful pruning strategy. If the current node's value is greater than `high`, then the node and its entire right subtree are too large, so we can discard them and only keep the trimmed left subtree. Similarly, if the value is less than `low`, the node and its left subtree are too small. When the node is within range, we recursively trim both children and attach the results.

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
    TreeNode* trimBST(TreeNode* root, int low, int high) {
        if (!root) return nullptr;

        if (root->val > high) {
            return trimBST(root->left, low, high);
        }
        if (root->val < low) {
            return trimBST(root->right, low, high);
        }

        root->left = trimBST(root->left, low, high);
        root->right = trimBST(root->right, low, high);
        return root;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Iterative DFS

We can avoid recursion by using a stack. The idea remains the same: nodes outside the range need to be replaced by their valid children. We first find a valid root, then process the tree using the stack, fixing any out-of-range children by replacing them with their appropriate grandchildren.

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
    TreeNode* trimBST(TreeNode* root, int low, int high) {
        while (root && (root->val < low || root->val > high)) {
            root = (root->val < low) ? root->right : root->left;
        }

        stack<TreeNode*> stack;
        stack.push(root);

        while (!stack.empty()) {
            TreeNode* node = stack.top();
            stack.pop();
            if (!node) continue;

            bool leftOut = (node->left && node->left->val < low);
            bool rightOut = (node->right && node->right->val > high);

            if (leftOut) node->left = node->left->right;
            if (rightOut) node->right = node->right->left;

            if (leftOut || rightOut) {
                stack.push(node);
            } else {
                if (node->left) stack.push(node->left);
                if (node->right) stack.push(node->right);
            }
        }

        return root;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Iterative DFS (Optimal)

Instead of using a stack, we can trim the tree in two linear passes. After finding a valid root, we traverse down the left spine fixing any nodes that fall below `low`, then traverse down the right spine fixing any nodes that exceed `high`. This works because in a BST, once we fix a node on one side, we only need to continue checking in that direction.

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
    TreeNode* trimBST(TreeNode* root, int low, int high) {
        while (root && (root->val < low || root->val > high)) {
            root = (root->val < low) ? root->right : root->left;
        }

        TreeNode* tmpRoot = root;
        while (root) {
            while (root->left && root->left->val < low) {
                root->left = root->left->right;
            }
            root = root->left;
        }

        root = tmpRoot;
        while (root) {
            while (root->right && root->right->val > high) {
                root->right = root->right->left;
            }
            root = root->right;
        }

        return tmpRoot;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
