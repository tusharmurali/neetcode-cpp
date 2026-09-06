# 250. Count Univalue Subtrees

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/count-univalue-subtrees/>  
- **NeetCode:** <https://neetcode.io/problems/count-univalue-subtrees>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

A uni-value subtree is one where all nodes have the same value. We can use DFS to check each subtree from the bottom up. For a node to be the root of a uni-value subtree, both its children must be roots of uni-value subtrees, and the node's value must match its children's values (if they exist). Leaf nodes are always uni-value subtrees.

```cpp
class Solution {
public:
    int count = 0;

    bool dfs(TreeNode* node) {
        if (node == nullptr) {
            return true;
        }

        bool isLeftUniValue = dfs(node->left);
        bool isRightUniValue = dfs(node->right);

        // If both the children form uni-value subtrees, we compare the value of
        // chidren's node with the node value.
        if (isLeftUniValue && isRightUniValue) {
            if (node->left != nullptr && node->left->val != node->val) {
                return false;
            }
            if (node->right != nullptr && node->right->val != node->val) {
                return false;
            }
            count++;
            return true;
        }
        // Else if any of the child does not form a uni-value subtree, the subtree
        // rooted at node cannot be a uni-value subtree.
        return false;
    }

    int countUnivalSubtrees(TreeNode* root) {
        dfs(root);
        return count;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the number of nodes in the given binary tree

## 2. Depth First Search Without Using The Global Variable

The previous solution uses a global or instance variable to track the count. We can avoid this by passing a mutable container (like an array or reference) through the recursion. This makes the function more self-contained and easier to test, while keeping the same logic.

```cpp
class Solution {
public:
    bool dfs(TreeNode* node, int& count) {
        if (node == nullptr) {
            return true;
        }

        bool isLeftUniValue = dfs(node->left, count);
        bool isRightUniValue = dfs(node->right, count);

        // If both the children form uni-value subtrees, we compare the value of
        // chidren's node with the node value.
        if (isLeftUniValue && isRightUniValue) {
            if (node->left != nullptr && node->left->val != node->val) {
                return false;
            }
            if (node->right != nullptr && node->right->val != node->val) {
                return false;
            }
            count++;
            return true;
        }
        // Else if any of the child does not form a uni-value subtree, the subtree
        // rooted at node cannot be a uni-value subtree.
        return false;
    }

    int countUnivalSubtrees(TreeNode* root) {
        int count = 0;
        dfs(root, count);
        return count;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the number of nodes in the given binary tree
