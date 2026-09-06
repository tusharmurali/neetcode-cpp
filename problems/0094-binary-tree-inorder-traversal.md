# 94. Binary Tree Inorder Traversal

- **Difficulty:** Easy  
- **Pattern:** Trees  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/binary-tree-inorder-traversal/>  
- **NeetCode:** <https://neetcode.io/problems/binary-tree-inorder-traversal>  
- **Video:** <https://www.youtube.com/watch?v=g_S5WuasWUE>  
- **Video approach:** 2. Iterative Depth First Search  

[← Back to index](../INDEX.md)

## 1. Depth First Search

Inorder traversal visits nodes in the order: left subtree, current node, right subtree. For a binary search tree, this produces values in sorted order. We can use recursion to naturally handle the traversal by first recursing on the left child, then processing the current node, and finally recursing on the right child.

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
    vector<int> res;

public:
    vector<int> inorderTraversal(TreeNode* root) {
        inorder(root);
        return res;
    }

private:
    void inorder(TreeNode* node) {
        if (!node) {
            return;
        }
        inorder(node->left);
        res.push_back(node->val);
        inorder(node->right);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(n)$ space for the recursion stack.
    - $O(n)$ space for the output array.

## 2. Iterative Depth First Search ▶ video

We can simulate the recursive call stack using an explicit stack. The key insight is that we need to go as far left as possible, then process the current node, and move to the right subtree. The stack helps us remember which nodes we still need to process after finishing the left subtrees.

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
    vector<int> inorderTraversal(TreeNode* root) {
        vector<int> res;
        stack<TreeNode*> stack;
        TreeNode* cur = root;

        while (cur || !stack.empty()) {
            while (cur) {
                stack.push(cur);
                cur = cur->left;
            }
            cur = stack.top();
            stack.pop();
            res.push_back(cur->val);
            cur = cur->right;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(n)$ space for the stack.
    - $O(n)$ space for the output array.

## 3. Morris Traversal

Morris Traversal achieves O(1) extra space by temporarily modifying the tree structure. The idea is to create a temporary link from the rightmost node of the left subtree back to the current node. This allows us to return to the current node after traversing the left subtree without using a stack. After processing, we remove the temporary link to restore the original tree.

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
    vector<int> inorderTraversal(TreeNode* root) {
        vector<int> res;
        TreeNode* cur = root;

        while (cur) {
            if (!cur->left) {
                res.push_back(cur->val);
                cur = cur->right;
            } else {
                TreeNode* prev = cur->left;
                while (prev->right && prev->right != cur) {
                    prev = prev->right;
                }

                if (!prev->right) {
                    prev->right = cur;
                    cur = cur->left;
                } else {
                    prev->right = nullptr;
                    res.push_back(cur->val);
                    cur = cur->right;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output array.

## Standalone solution file (`cpp/0094-binary-tree-inorder-traversal.cpp` in the NeetCode repo)

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
#include <stack>

class Solution {
public:
    /* Recursive
    vector<int> helper(TreeNode* node, vector<int>& path) {
        if (node == NULL)
            return path;

        path = helper(node->left, path);
        path.push_back(node->val);
        path = helper(node->right, path);
        return path;
    }
    */

    // Iterative
    vector<int> inorderTraversal(TreeNode* root) {
        stack<TreeNode*> stk;
        vector<int> path;
        TreeNode* current = root;

        while (!stk.empty() || current != NULL) {
            while (current != NULL) {
                stk.push(current);
                current = current->left;
            }
            TreeNode* node = stk.top();
            path.push_back(node->val);
            stk.pop();
            current = node->right;
        }
        return path;
    }
};
```
