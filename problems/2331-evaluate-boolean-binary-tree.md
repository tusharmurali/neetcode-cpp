# 2331. Evaluate Boolean Binary Tree

- **Difficulty:** Easy  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/evaluate-boolean-binary-tree/>  
- **NeetCode:** <https://neetcode.io/problems/evaluate-boolean-binary-tree>  
- **Video:** <https://www.youtube.com/watch?v=9a_cP54jn8Q>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

This is a classic tree evaluation problem. Leaf nodes hold boolean values (0 or 1), while internal nodes represent OR (2) or AND (3) operations. We recursively evaluate each subtree: leaf nodes return their value directly, and internal nodes combine their children's results using the appropriate operator. The tree structure naturally maps to the recursive call stack.

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
    bool evaluateTree(TreeNode* root) {
        if (!root->left) {
            return root->val == 1;
        }

        if (root->val == 2) {
            return evaluateTree(root->left) || evaluateTree(root->right);
        }

        if (root->val == 3) {
            return evaluateTree(root->left) && evaluateTree(root->right);
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Iterative DFS

We can avoid recursion by using an explicit stack and a hash map to store computed values. The key challenge is handling the post-order nature of evaluation: a node can only be evaluated after both its children are processed. We achieve this by pushing nodes back onto the stack if their children haven't been evaluated yet, effectively simulating the recursive call stack.

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
    bool evaluateTree(TreeNode* root) {
        stack<TreeNode*> stk;
        unordered_map<TreeNode*, bool> value;
        stk.push(root);

        while (!stk.empty()) {
            TreeNode* node = stk.top();
            stk.pop();

            if (!node->left) {
                value[node] = node->val == 1;
            } else if (value.count(node->left)) {
                bool leftValue = value[node->left];
                bool rightValue = value[node->right];

                if (node->val == 2) {
                    value[node] = leftValue || rightValue;
                } else if (node->val == 3) {
                    value[node] = leftValue && rightValue;
                }
            } else {
                stk.push(node);
                stk.push(node->right);
                stk.push(node->left);
            }
        }

        return value[root];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
