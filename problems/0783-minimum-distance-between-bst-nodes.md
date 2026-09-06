# 783. Minimum Distance between BST Nodes

- **Difficulty:** Easy  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-distance-between-bst-nodes/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-distance-between-bst-nodes>  
- **Video:** <https://www.youtube.com/watch?v=joxx4hTYwcw>  

[← Back to index](../INDEX.md)

## 1. Brute Force (DFS)

The most straightforward approach is to compare every pair of nodes in the tree. For each node, we traverse the entire tree to find the minimum absolute difference between this node's value and any other node's value. While simple to understand, this approach doesn't leverage the BST property and results in redundant comparisons.

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
    int minDiffInBST(TreeNode* root) {
        return dfs(root, root);
    }

private:
    int dfs(TreeNode* root, TreeNode* node) {
        if (!node) {
            return INT_MAX;
        }
        int res = dfs1(root, node);
        res = min(res, dfs(root, node->left));
        res = min(res, dfs(root, node->right));
        return res;
    }

    int dfs1(TreeNode* root, TreeNode* node) {
        if (!root) {
            return INT_MAX;
        }
        int res = INT_MAX;
        if (root != node) {
            res = abs(root->val - node->val);
        }
        res = min(res, dfs1(root->left, node));
        res = min(res, dfs1(root->right, node));
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Inorder Traversal

In a BST, an inorder traversal visits nodes in sorted order. The minimum difference between any two nodes must occur between consecutive elements in this sorted sequence. So we perform an inorder traversal to collect all values into an array, then scan through the array to find the minimum difference between adjacent elements.

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
    int minDiffInBST(TreeNode* root) {
        vector<int> arr;
        dfs(root, arr);

        int res = arr[1] - arr[0];
        for (int i = 2; i < arr.size(); i++) {
            res = min(res, arr[i] - arr[i - 1]);
        }
        return res;
    }

private:
    void dfs(TreeNode* node, vector<int>& arr) {
        if (!node) return;
        dfs(node->left, arr);
        arr.push_back(node->val);
        dfs(node->right, arr);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Inorder Traversal (Space Optimized)

Instead of storing all values in an array and then finding the minimum difference, we can compute the answer during the traversal itself. We keep track of the previously visited node during the inorder walk. At each step, we compare the current node's value with the previous node's value (since they are consecutive in sorted order) and update the minimum difference on the fly.

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
    int minDiffInBST(TreeNode* root) {
        TreeNode* prev = nullptr;
        int res = INT_MAX;

        dfs(root, prev, res);
        return res;
    }

private:
    void dfs(TreeNode* node, TreeNode*& prev, int& res) {
        if (!node) return;

        dfs(node->left, prev, res);
        if (prev) {
            res = min(res, node->val - prev->val);
        }
        prev = node;
        dfs(node->right, prev, res);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 4. Iterative DFS (Inorder Traversal)

The recursive inorder traversal can be converted to an iterative version using an explicit stack. This avoids recursion overhead and gives us more control over the traversal. The logic remains the same: we visit nodes in sorted order and compare each node with its predecessor.

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
    int minDiffInBST(TreeNode* root) {
        stack<TreeNode*> st;
        TreeNode* prev = nullptr;
        TreeNode* cur = root;
        int res = INT_MAX;

        while (!st.empty() || cur) {
            while (cur) {
                st.push(cur);
                cur = cur->left;
            }

            cur = st.top();
            st.pop();
            if (prev) {
                res = min(res, cur->val - prev->val);
            }
            prev = cur;
            cur = cur->right;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 5. Morris Traversal

Morris traversal allows us to perform inorder traversal without using a stack or recursion, achieving O(1) extra space. The idea is to temporarily modify the tree by creating links from predecessor nodes back to their successors, allowing us to navigate the tree without additional memory. We traverse the tree, comparing consecutive values as before.

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
    int minDiffInBST(TreeNode* root) {
        int prevVal = INT_MAX, res = INT_MAX;
        TreeNode* cur = root;

        while (cur) {
            if (!cur->left) {
                if (prevVal != INT_MAX) {
                    res = min(res, cur->val - prevVal);
                }
                prevVal = cur->val;
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
                    if (prevVal != INT_MAX) {
                        res = min(res, cur->val - prevVal);
                    }
                    prevVal = cur->val;
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
- Space complexity: $O(1)$ extra space.
