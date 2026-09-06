# 298. Binary Tree Longest Consecutive Sequence

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/binary-tree-longest-consecutive-sequence/>  
- **NeetCode:** <https://neetcode.io/problems/binary-tree-longest-consecutive-sequence>  

[← Back to index](../INDEX.md)

## 1. Top Down Depth-first Search

We traverse the tree from root to leaves, passing down the current consecutive sequence length to each child. At each node, we check if it continues the sequence from its parent (value is exactly one more than the parent). If so, we extend the sequence; otherwise, we start a new sequence. We track the maximum length seen across all nodes.

```cpp
class Solution {
private:
    int maxLength = 0;

    void dfs(TreeNode* p, TreeNode* parent, int length) {
        if (p == nullptr) return;

        length = (parent != nullptr && p->val == parent->val + 1) ? length + 1 : 1;
        maxLength = max(maxLength, length);

        dfs(p->left, p, length);
        dfs(p->right, p, length);
    }

public:
    int longestConsecutive(TreeNode* root) {
        dfs(root, nullptr, 0);
        return maxLength;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the number of nodes in the input tree

## 2. Bottom Up Depth-first Search

Instead of passing information down, we can compute the consecutive sequence length from leaves up to the root. Each node returns the length of the longest consecutive sequence starting from itself going downward. The parent then checks if it can extend this sequence by verifying that its value is exactly one less than its child's value.

```cpp
class Solution {
private:
    int maxLength = 0;

    int dfs(TreeNode* p) {
        if (p == nullptr) return 0;

        int L = dfs(p->left) + 1;
        int R = dfs(p->right) + 1;

        if (p->left != nullptr && p->val + 1 != p->left->val) {
            L = 1;
        }

        if (p->right != nullptr && p->val + 1 != p->right->val) {
            R = 1;
        }

        int length = max(L, R);
        maxLength = max(maxLength, length);

        return length;
    }

public:
    int longestConsecutive(TreeNode* root) {
        dfs(root);
        return maxLength;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the number of nodes in the input tree
