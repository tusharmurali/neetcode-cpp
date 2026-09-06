# 549. Binary Tree Longest Consecutive Sequence II

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/binary-tree-longest-consecutive-sequence-ii/>  
- **NeetCode:** <https://neetcode.io/problems/binary-tree-longest-consecutive-sequence-ii>  

[← Back to index](../INDEX.md)

## 1. Brute Force (Time Limit Exceeded)

The brute force approach considers every possible path in the tree and checks if it forms a consecutive sequence. For each node, we explore all paths passing through it by examining every possible starting and ending point in its subtrees.

```cpp
// NeetCode has no C++ version of this approach yet.
```

**Complexity**

- Time complexity: $O(n^3)$
- Space complexity: $O(n^3)$

> Where $n$ is the number of nodes in the input tree

## 2. Single traversal

We can find the longest consecutive path in a single traversal by tracking two values at each node: the length of the longest increasing path going down and the length of the longest decreasing path going down. A node can potentially be the turning point where an increasing path from one subtree meets a decreasing path from the other, forming a complete consecutive sequence. By combining these two lengths at each node, we find the longest path passing through that node.

```cpp
class Solution {
private:
    int maxval = 0;

    vector<int> longestPath(TreeNode* root) {
        if (root == nullptr) {
            return {0, 0};
        }

        int inr = 1, dcr = 1;

        if (root->left != nullptr) {
            vector<int> left = longestPath(root->left);
            if (root->val == root->left->val + 1) {
                dcr = left[1] + 1;
            } else if (root->val == root->left->val - 1) {
                inr = left[0] + 1;
            }
        }

        if (root->right != nullptr) {
            vector<int> right = longestPath(root->right);
            if (root->val == root->right->val + 1) {
                dcr = max(dcr, right[1] + 1);
            } else if (root->val == root->right->val - 1) {
                inr = max(inr, right[0] + 1);
            }
        }

        maxval = max(maxval, dcr + inr - 1);

        return {inr, dcr};
    }

public:
    int longestConsecutive(TreeNode* root) {
        longestPath(root);
        return maxval;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the number of nodes in the input tree
