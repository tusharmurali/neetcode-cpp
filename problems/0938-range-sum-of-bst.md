# 938. Range Sum of BST

- **Difficulty:** Easy  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/range-sum-of-bst/>  
- **NeetCode:** <https://neetcode.io/problems/range-sum-of-bst>  
- **Video:** <https://www.youtube.com/watch?v=uLVG45n4Sbg>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

We traverse the entire tree and sum up values that fall within the given range. For each node, we check if its value is between `low` and `high`, adding it to our sum if so. We then recursively process both children. This approach visits every node regardless of the BST property.

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
    int rangeSumBST(TreeNode* root, int low, int high) {
        if (!root) return 0;

        int res = (low <= root->val && root->val <= high) ? root->val : 0;
        res += rangeSumBST(root->left, low, high);
        res += rangeSumBST(root->right, low, high);
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Depth First Search (Optimal)

We can leverage the BST property to prune unnecessary branches. If the current node's value is greater than `high`, all values in the right subtree are also too large, so we only need to search left. Similarly, if the current value is less than `low`, we only search right. This eliminates entire subtrees that cannot contribute to the sum.

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
    int rangeSumBST(TreeNode* root, int low, int high) {
        if (!root) return 0;

        if (root->val > high) {
            return rangeSumBST(root->left, low, high);
        }
        if (root->val < low) {
            return rangeSumBST(root->right, low, high);
        }

        return root->val + rangeSumBST(root->left, low, high) +
                           rangeSumBST(root->right, low, high);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 3. Iterative DFS

The recursive solution can be converted to an iterative one using an explicit stack. We maintain the same pruning logic: only push children onto the stack if they might contain values in range. This avoids function call overhead while preserving the efficiency of the optimal approach.

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
    int rangeSumBST(TreeNode* root, int low, int high) {
        int res = 0;
        stack<TreeNode*> stack;
        stack.push(root);

        while (!stack.empty()) {
            TreeNode* node = stack.top();
            stack.pop();
            if (!node) continue;

            if (low <= node->val && node->val <= high) {
                res += node->val;
            }
            if (node->val > low) {
                stack.push(node->left);
            }
            if (node->val < high) {
                stack.push(node->right);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
