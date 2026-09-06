# 545. Boundary of Binary Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/boundary-of-binary-tree/>  
- **NeetCode:** <https://neetcode.io/problems/boundary-of-binary-tree>  

[← Back to index](../INDEX.md)

## 1. Simple Solution

The boundary of a binary tree consists of three parts traversed in order: the left boundary (top to bottom, excluding leaves), all leaf nodes (left to right), and the right boundary (bottom to top, excluding leaves). We handle each part separately: traverse down the left edge, collect all leaves via recursion, and traverse down the right edge while using a stack to reverse the order.

```cpp
class Solution {
public:
    bool isLeaf(TreeNode* t) {
        return t->left == nullptr && t->right == nullptr;
    }

    void addLeaves(vector<int>& res, TreeNode* root) {
        if (isLeaf(root)) {
            res.push_back(root->val);
        } else {
            if (root->left != nullptr) {
                addLeaves(res, root->left);
            }
            if (root->right != nullptr) {
                addLeaves(res, root->right);
            }
        }
    }

    vector<int> boundaryOfBinaryTree(TreeNode* root) {
        vector<int> res;
        if (root == nullptr) {
            return res;
        }

        if (!isLeaf(root)) {
            res.push_back(root->val);
        }

        TreeNode* t = root->left;
        while (t != nullptr) {
            if (!isLeaf(t)) {
                res.push_back(t->val);
            }
            if (t->left != nullptr) {
                t = t->left;
            } else {
                t = t->right;
            }
        }

        addLeaves(res, root);

        stack<int> s;
        t = root->right;
        while (t != nullptr) {
            if (!isLeaf(t)) {
                s.push(t->val);
            }
            if (t->right != nullptr) {
                t = t->right;
            } else {
                t = t->left;
            }
        }

        while (!s.empty()) {
            res.push_back(s.top());
            s.pop();
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the number of nodes in the tree

## 2. Using PreOrder Traversal

We can collect all boundary nodes in a single preorder traversal by tracking where each node belongs. Using a flag system, we mark nodes as: root (`0`), left boundary (`1`), right boundary (`2`), or internal (`3`). During traversal, we determine each child's flag based on the parent's flag and whether siblings exist. Left boundary nodes go directly to the result, right boundary nodes are collected in reverse order, and leaves are gathered separately.

```cpp
class Solution {
public:
    vector<int> boundaryOfBinaryTree(TreeNode* root) {
        vector<int> left_boundary, right_boundary, leaves;
        preorder(root, left_boundary, right_boundary, leaves, 0);
        left_boundary.insert(left_boundary.end(), leaves.begin(), leaves.end());
        left_boundary.insert(left_boundary.end(), right_boundary.begin(), right_boundary.end());
        return left_boundary;
    }

private:
    bool isLeaf(TreeNode* cur) {
        return cur->left == nullptr && cur->right == nullptr;
    }

    bool isRightBoundary(int flag) {
        return flag == 2;
    }

    bool isLeftBoundary(int flag) {
        return flag == 1;
    }

    bool isRoot(int flag) {
        return flag == 0;
    }

    int leftChildFlag(TreeNode* cur, int flag) {
        if (isLeftBoundary(flag) || isRoot(flag)) {
            return 1;
        } else if (isRightBoundary(flag) && cur->right == nullptr) {
            return 2;
        } else {
            return 3;
        }
    }

    int rightChildFlag(TreeNode* cur, int flag) {
        if (isRightBoundary(flag) || isRoot(flag)) {
            return 2;
        } else if (isLeftBoundary(flag) && cur->left == nullptr) {
            return 1;
        } else {
            return 3;
        }
    }

    void preorder(TreeNode* cur, vector<int>& left_boundary, vector<int>& right_boundary, vector<int>& leaves, int flag) {
        if (cur == nullptr) {
            return;
        }

        if (isRightBoundary(flag)) {
            right_boundary.insert(right_boundary.begin(), cur->val);
        } else if (isLeftBoundary(flag) || isRoot(flag)) {
            left_boundary.push_back(cur->val);
        } else if (isLeaf(cur)) {
            leaves.push_back(cur->val);
        }

        preorder(cur->left, left_boundary, right_boundary, leaves, leftChildFlag(cur, flag));
        preorder(cur->right, left_boundary, right_boundary, leaves, rightChildFlag(cur, flag));
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the number of nodes in the tree
