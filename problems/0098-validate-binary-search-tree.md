# 98. Validate Binary Search Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/validate-binary-search-tree/>  
- **NeetCode:** <https://neetcode.io/problems/valid-binary-search-tree>  
- **Video:** <https://www.youtube.com/watch?v=s6ATEkipzow>  
- **Video approach:** 2. Depth First Search  

[← Back to index](../INDEX.md)

## 1. Brute Force

To check if a tree is a valid **Binary Search Tree (BST)**, every node must satisfy:

- All values in its **left subtree** are **strictly less** than the node’s value.
- All values in its **right subtree** are **strictly greater** than the node’s value.

In this brute force idea, for **each node** we:

1. Check **all nodes** in its left subtree to confirm they are `< node.val`.
2. Check **all nodes** in its right subtree to confirm they are `> node.val`.
3. Then recursively repeat the same process for each child as a new root.

This re-checks many nodes multiple times, so it’s correct but not efficient.

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
    static bool left_check(int val, int limit) {
        return val < limit;
    }

    static bool right_check(int val, int limit) {
        return val > limit;
    }

    bool isValidBST(TreeNode* root) {
        if (!root) {
            return true;
        }

        if (!isValid(root->left, root->val, left_check) ||
            !isValid(root->right, root->val, right_check)) {
            return false;
        }

        return isValidBST(root->left) && isValidBST(root->right);
    }

    bool isValid(TreeNode* root, int limit, bool (*check)(int, int)) {
        if (!root) {
            return true;
        }
        if (!check(root->val, limit)) {
            return false;
        }
        return isValid(root->left, limit, check) &&
               isValid(root->right, limit, check);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Depth First Search ▶ video

A Binary Search Tree isn’t just about each node being smaller or larger than its parent —  
**every node must fit within a valid value range decided by all its ancestors**.

- For the root, the allowed range is `(-∞, +∞)`.
- When you go **left**, the node’s value must be **less than the parent**, so the upper bound becomes smaller.
- When you go **right**, the node’s value must be **greater than the parent**, so the lower bound becomes larger.

As we move down the tree, we keep tightening these bounds.  
If any node violates its allowed range → the tree is not a BST.

This checks all BST rules efficiently in one DFS pass.

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
    bool isValidBST(TreeNode* root) {
        return valid(root, LONG_MIN, LONG_MAX);
    }

    bool valid(TreeNode* node, long left, long right) {
        if (!node) {
            return true;
        }
        if (!(left < node->val && node->val < right)) {
            return false;
        }
        return valid(node->left, left, node->val) &&
               valid(node->right, node->val, right);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Breadth First Search

A tree is a valid BST only if **every node lies within a valid range** defined by its ancestors.  
Instead of using recursion, we can use a queue (BFS) to check this level by level.

- Start with the root, whose valid range is `(-∞, +∞)`.
- When moving to the **left child**, its maximum allowed value becomes the current node’s value.
- When moving to the **right child**, its minimum allowed value becomes the current node’s value.
- If any node violates its allowed range, the tree is not a BST.

This way, we verify every node exactly once using BFS.

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
    bool isValidBST(TreeNode* root) {
        if (!root) {
            return true;
        }

        queue<tuple<TreeNode*, long, long>> queue;
        queue.push(make_tuple(root, LONG_MIN, LONG_MAX));

        while (!queue.empty()) {
            auto [node, left, right] = queue.front();
            queue.pop();

            if (!(left < node->val && node->val < right)) {
                return false;
            }
            if (node->left) {
                queue.push(make_tuple(node->left, left, node->val));
            }
            if (node->right) {
                queue.push(make_tuple(node->right, node->val, right));
            }
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0098-validate-binary-search-tree.cpp` in the NeetCode repo)

```cpp
/*
    Given root of binary tree, determine if it's valid (left all < curr, right all > curr)
    
    Inorder traversal & check if prev >= curr, recursive/iterative solutions
    
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
    bool isValidBST(TreeNode* root) {
        return helper(root, LONG_MIN, LONG_MAX);
    }
private:
    bool helper(TreeNode* root, long left, long right){
        if (!root)
            return true;
        if (root->val < right && root->val > left){
            return helper(root->left, left, root->val) && helper(root->right, root->val, right);
        }
        return false;
    }
};
/*
class Solution {
public:
    bool isValidBST(TreeNode* root) {
        TreeNode* prev = NULL;
        return inorder(root, prev);
    }
private:
    bool inorder(TreeNode* root, TreeNode*& prev) {
        if (root == NULL) {
            return true;
        }
        
        if (!inorder(root->left, prev)) {
            return false;
        }
        
        if (prev != NULL && prev->val >= root->val) {
            return false;
        }
        prev = root;
        
        if (!inorder(root->right, prev)) {
            return false;
        }
        
        return true;
    }
};
*/

// class Solution {
// public:
//     bool isValidBST(TreeNode* root) {
//         stack<TreeNode*> stk;
//         TreeNode* prev = NULL;
        
//         while (!stk.empty() || root != NULL) {
//             while (root != NULL) {
//                 stk.push(root);
//                 root = root->left;
//             }
//             root = stk.top();
//             stk.pop();
            
//             if (prev != NULL && prev->val >= root->val) {
//                 return false;
//             }
            
//             prev = root;
//             root = root->right;
//         }
        
//         return true;
//     }
// };
```
