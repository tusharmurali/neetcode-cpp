# 235. Lowest Common Ancestor of a Binary Search Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/>  
- **NeetCode:** <https://neetcode.io/problems/lowest-common-ancestor-in-binary-search-tree>  
- **Video:** <https://www.youtube.com/watch?v=gs2LMfuOR9k>  
- **Video approach:** 2. Iteration  

[← Back to index](../INDEX.md)

## 1. Recursion

We are working with a **Binary Search Tree (BST)**, so:

- All values in the **left subtree** of a node are **smaller** than the node’s value.
- All values in the **right subtree** are **greater** than the node’s value.

For two nodes `p` and `q`:

- If **both** values are smaller than the current node -> both must lie in the **left subtree**.
- If **both** values are greater than the current node -> both must lie in the **right subtree**.
- Otherwise, the current node is the **split point** where one node is on the left and the other is on the right (or one is equal to the current node).
  That split point is the **Lowest Common Ancestor (LCA)**.

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
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        if (!root || !p || !q) {
            return nullptr;
        }
        if (max(p->val, q->val) < root->val) {
            return lowestCommonAncestor(root->left, p, q);
        } else if (min(p->val, q->val) > root->val) {
            return lowestCommonAncestor(root->right, p, q);
        } else {
            return root;
        }
    }
};
```

**Complexity**

- Time complexity: $O(h)$
- Space complexity: $O(h)$

> Where $h$ is the height of the tree.

## 2. Iteration ▶ video

This is the iterative version of finding the **Lowest Common Ancestor (LCA)** in a **Binary Search Tree (BST)**.
Because a BST is ordered:

- Left subtree < node < right subtree

We can decide **where both nodes lie** just by comparing values.

- If `p` and `q` are both **greater** than the current node -> move **right**.
- If they are both **smaller** -> move **left**.
- If they split (one on each side) or one equals the current node ->
  **current node is the LCA**, because it's the first node where their paths diverge.

This avoids recursion and simply walks down the tree until the split point is found.

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
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        TreeNode* cur = root;

        while (cur) {
            if (p->val > cur->val && q->val > cur->val) {
                cur = cur->right;
            } else if (p->val < cur->val && q->val < cur->val) {
                cur = cur->left;
            } else {
                return cur;
            }
        }
        return nullptr;
    }
};
```

**Complexity**

- Time complexity: $O(h)$
- Space complexity: $O(1)$

> Where $h$ is the height of the tree.

## Standalone solution file (`cpp/0235-lowest-common-ancestor-of-a-binary-search-tree.cpp` in the NeetCode repo)

```cpp
/*
    Given a binary search tree (BST), find the LCA of 2 given nodes in the BST

    Use BST property: if curr > left & right go left, else if < go right, else done

    Time: O(n)
    Space: O(n)
*/

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
        if (p->val < root->val && q->val < root->val) {
            return lowestCommonAncestor(root->left, p, q);
        } else if (p->val > root->val && q->val > root->val) {
            return lowestCommonAncestor(root->right, p, q);
        } else {
            return root;
        }
    }
};

// class Solution {
// public:
//     TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
//         while (root != NULL) {
//             if (p->val < root->val && q->val < root->val) {
//                 root = root->left;
//             } else if (p->val > root->val && q->val > root->val) {
//                 root = root->right;
//             } else {
//                 return root;
//             }
//         }
//         return NULL;
//     }
// };
```
