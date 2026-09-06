# 450. Delete Node in a BST

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/delete-node-in-a-bst/>  
- **NeetCode:** <https://neetcode.io/problems/delete-node-in-a-bst>  
- **Video:** <https://www.youtube.com/watch?v=LFzAoJJt92M>  

[← Back to index](../INDEX.md)

## 1. Recursion - I

To delete a node in a BST, we first need to locate it using the BST property (left children are smaller, right children are larger). Once found, we handle three cases: if the node has no left child, replace it with its right child; if no right child, replace with the left child. The tricky case is when the node has both children. We find the in-order successor (the smallest node in the right subtree), copy its value to the current node, and then delete that successor node. This approach swaps values rather than restructuring pointers.

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
    TreeNode* deleteNode(TreeNode* root, int key) {
        if (!root) return root;

        if (key > root->val) {
            root->right = deleteNode(root->right, key);
        } else if (key < root->val) {
            root->left = deleteNode(root->left, key);
        } else {
            if (!root->left) return root->right;
            if (!root->right) return root->left;

            TreeNode* cur = root->right;
            while (cur->left) {
                cur = cur->left;
            }
            root->val = cur->val;
            root->right = deleteNode(root->right, root->val);
        }

        return root;
    }
};
```

**Complexity**

- Time complexity: $O(h)$
- Space complexity: $O(h)$ for the recursion stack.

> Where $h$ is the height of the given binary search tree.

## 2. Recursion - II

Instead of copying the successor's value and deleting it separately, we can restructure the tree directly. When the node to delete has both children, we find the in-order successor (leftmost node in the right subtree) and attach the left subtree of the deleted node as the left child of this successor. Then we simply return the right subtree as the replacement. This avoids value copying and removes the node in a single pass through the tree.

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
    TreeNode* deleteNode(TreeNode* root, int key) {
        if (!root) return root;

        if (key > root->val) {
            root->right = deleteNode(root->right, key);
        } else if (key < root->val) {
            root->left = deleteNode(root->left, key);
        } else {
            if (!root->left) return root->right;
            if (!root->right) return root->left;

            TreeNode* cur = root->right;
            while (cur->left) {
                cur = cur->left;
            }
            cur->left = root->left;
            TreeNode* res = root->right;
            delete root;
            return res;
        }

        return root;
    }
};
```

**Complexity**

- Time complexity: $O(h)$
- Space complexity: $O(h)$ for the recursion stack.

> Where $h$ is the height of the given binary search tree.

## 3. Iteration

This approach avoids recursion by using a loop to find the node to delete and its parent. Once found, we handle the same three deletion cases, but we manually update parent pointers. When the node has two children, we find the in-order successor, detach it from its position, and replace the deleted node with it. This requires careful pointer manipulation to maintain tree structure.

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
    TreeNode* deleteNode(TreeNode* root, int key) {
        if (!root) return root;

        TreeNode* parent = nullptr;
        TreeNode* cur = root;

        // Find the node to delete
        while (cur && cur->val != key) {
            parent = cur;
            if (key > cur->val) {
                cur = cur->right;
            } else {
                cur = cur->left;
            }
        }

        if (!cur) return root;

        // Node with only one child or no child
        if (!cur->left || !cur->right) {
            TreeNode* child = cur->left ? cur->left : cur->right;
            if (!parent) return child;
            if (parent->left == cur) {
                parent->left = child;
            } else {
                parent->right = child;
            }
        } else {
            // Node with two children
            TreeNode* par = nullptr; // parent of right subtree's min node
            TreeNode* delNode = cur;
            cur = cur->right;
            while (cur->left) {
                par = cur;
                cur = cur->left;
            }

            if (par) { // if there was a left traversal
                par->left = cur->right;
                cur->right = delNode->right;
            }
            cur->left = delNode->left;

            if (!parent) return cur; // if deleting root

            if (parent->left == delNode) {
                parent->left = cur;
            } else {
                parent->right = cur;
            }
        }

        return root;
    }
};
```

**Complexity**

- Time complexity: $O(h)$
- Space complexity: $O(1)$ extra space.

> Where $h$ is the height of the given binary search tree.

## Standalone solution file (`cpp/0450-delete-node-in-a-bst.cpp` in the NeetCode repo)

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

// Time: O(h)
// Space: O(1)
class Solution {
public:
    TreeNode* deleteNode(TreeNode* root, int key) {
        if(root == nullptr) return root;

        if(root->val > key) {
            root->left = deleteNode(root->left, key);
        }
        else if(root->val < key) {
            root->right = deleteNode(root->right, key);
        }

        // perform deletion if root->val == key
        else {
            if(!root->left) return root->right;
            if(!root->right) return root->left;

            // both left and right subtrees are not null
            // traverse the right subtree to find the minimum/leftmost value
            // (or) travel the left subtree to find the maximum/rightmost value
            TreeNode* temp = root->right;
            while(temp->left) {
                temp = temp->left;
            }
            root->val = temp->val;

            root->right = deleteNode(root->right, temp->val);
        }

        return root;
    }
};
```
