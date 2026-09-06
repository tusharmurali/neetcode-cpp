# 99. Recover Binary Search Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/recover-binary-search-tree/>  
- **NeetCode:** <https://neetcode.io/problems/recover-binary-search-tree>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach is to try every possible pair of nodes and check if swapping their values produces a valid BST. Since exactly two nodes were swapped, one such pair must restore the tree to its correct state.

For each pair of nodes, we swap their values, validate whether the resulting tree is a valid BST, and either keep the swap (if valid) or revert it (if invalid). While inefficient, this approach guarantees finding the solution by exhaustively checking all possibilities.

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
    void recoverTree(TreeNode* root) {
        dfs(root, root, root);
    }

    bool dfs(TreeNode* node1, TreeNode* node2, TreeNode* root) {
        if (!node1) return false;
        if (dfs1(node1, node2, root)) return true;
        return dfs(node1->left, node2, root) || dfs(node1->right, node2, root);
    }

    bool dfs1(TreeNode* node1, TreeNode* node2, TreeNode* root) {
        if (!node2 || node1 == node2) return false;

        swap(node1->val, node2->val);
        if (isBST(root)) return true;
        swap(node1->val, node2->val);

        return dfs1(node1, node2->left, root) || dfs1(node1, node2->right, root);
    }

    bool isBST(TreeNode* node) {
        TreeNode* prev = nullptr;
        return inorder(node, prev);
    }

    bool inorder(TreeNode* node, TreeNode*& prev) {
        if (!node) return true;
        if (!inorder(node->left, prev)) return false;
        if (prev && prev->val >= node->val) return false;
        prev = node;
        return inorder(node->right, prev);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Inorder Traversal

A key property of BSTs is that an inorder traversal produces values in sorted order. When two nodes are swapped incorrectly, this sorted sequence will have one or two "inversions" where a value is greater than the next value.

If the swapped nodes are adjacent in the inorder sequence, there will be exactly one inversion. If they are not adjacent, there will be two inversions. In the first inversion, the larger (out-of-place) node is the first swapped node. In the second inversion (or the same one if only one exists), the smaller node is the second swapped node.

By collecting all nodes during inorder traversal and then scanning for these inversions, we can identify the two swapped nodes and swap their values back.

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
    void recoverTree(TreeNode* root) {
        vector<TreeNode*> arr;
        inorder(root, arr);

        TreeNode* node1 = nullptr;
        TreeNode* node2 = nullptr;

        for (int i = 0; i < arr.size() - 1; i++) {
            if (arr[i]->val > arr[i + 1]->val) {
                node2 = arr[i + 1];
                if (!node1) node1 = arr[i];
                else break;
            }
        }

        swap(node1->val, node2->val);
    }

    void inorder(TreeNode* node, vector<TreeNode*>& arr) {
        if (!node) return;
        inorder(node->left, arr);
        arr.push_back(node);
        inorder(node->right, arr);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Iterative Inorder Traversal

This approach uses the same logic as the recursive inorder traversal but implements it iteratively using an explicit stack. The advantage is that we can detect inversions on the fly during traversal rather than collecting all nodes first.

By keeping track of the previously visited node, we can immediately detect when the current node's value is less than the previous node's value, signaling an inversion. This allows us to identify the swapped nodes in a single pass through the tree.

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
    void recoverTree(TreeNode* root) {
        stack<TreeNode*> stack;
        TreeNode *node1 = nullptr, *node2 = nullptr, *prev = nullptr, *curr = root;

        while (!stack.empty() || curr) {
            while (curr) {
                stack.push(curr);
                curr = curr->left;
            }

            curr = stack.top(); stack.pop();
            if (prev && prev->val > curr->val) {
                node2 = curr;
                if (!node1) node1 = prev;
                else break;
            }
            prev = curr;
            curr = curr->right;
        }

        swap(node1->val, node2->val);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Morris Traversal

Morris traversal allows us to perform inorder traversal without using a stack or recursion, achieving `O(1)` space complexity. The technique works by temporarily modifying the tree structure: for each node with a left child, we find its inorder predecessor and create a temporary link back to the current node.

This temporary threading allows us to return to ancestor nodes after processing the left subtree without needing a stack. We can detect inversions during this traversal just like in the iterative approach, but without the extra space for a stack.

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
    void recoverTree(TreeNode* root) {
        TreeNode* node1 = nullptr;
        TreeNode* node2 = nullptr;
        TreeNode* prev = nullptr;
        TreeNode* curr = root;

        while (curr) {
            if (!curr->left) {
                if (prev && prev->val > curr->val) {
                    node2 = curr;
                    if (!node1) node1 = prev;
                }
                prev = curr;
                curr = curr->right;
            } else {
                TreeNode* pred = curr->left;
                while (pred->right && pred->right != curr) {
                    pred = pred->right;
                }

                if (!pred->right) {
                    pred->right = curr;
                    curr = curr->left;
                } else {
                    pred->right = nullptr;
                    if (prev && prev->val > curr->val) {
                        node2 = curr;
                        if (!node1) node1 = prev;
                    }
                    prev = curr;
                    curr = curr->right;
                }
            }
        }

        swap(node1->val, node2->val);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
