# 951. Flip Equivalent Binary Trees

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/flip-equivalent-binary-trees/>  
- **NeetCode:** <https://neetcode.io/problems/flip-equivalent-binary-trees>  
- **Video:** <https://www.youtube.com/watch?v=izRDc1il9Pk>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

Two trees are flip equivalent if we can make them identical by swapping the left and right children of some nodes. At each node, the subtrees either match directly (left with left, right with right) or match when flipped (left with right, right with left). We recursively check both possibilities.

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
    bool flipEquiv(TreeNode* root1, TreeNode* root2) {
        if (!root1 || !root2)
            return !root1 && !root2;
        if (root1->val != root2->val)
            return false;

        return (flipEquiv(root1->left, root2->left) &&
                flipEquiv(root1->right, root2->right) ||
                flipEquiv(root1->left, root2->right) &&
                flipEquiv(root1->right, root2->left));
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Breadth First Search

We can solve this iteratively using a queue to process node pairs level by level. For each pair of nodes, we check if their values match. Then we determine whether to compare children directly or in flipped order by checking which pairing makes the left children's values match.

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
    bool flipEquiv(TreeNode* root1, TreeNode* root2) {
        queue<pair<TreeNode*, TreeNode*>> q;
        q.push({root1, root2});

        while (!q.empty()) {
            auto [node1, node2] = q.front();
            q.pop();

            if (!node1 || !node2) {
                if (node1 != node2) return false;
                continue;
            }

            if (node1->val != node2->val) return false;

            if ((node1->left && node2->left && node1->left->val == node2->left->val) ||
                (!node1->left && !node2->left)) {
                q.push({node1->left, node2->left});
                q.push({node1->right, node2->right});
            } else {
                q.push({node1->left, node2->right});
                q.push({node1->right, node2->left});
            }
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Iterative DFS

This is the iterative version of the recursive DFS approach, using an explicit stack instead of the call stack. We process node pairs from the stack, checking values and pushing child pairs in the appropriate order (direct or flipped).

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
    bool flipEquiv(TreeNode* root1, TreeNode* root2) {
        stack<pair<TreeNode*, TreeNode*>> stk;
        stk.push({root1, root2});

        while (!stk.empty()) {
            auto [node1, node2] = stk.top();stk.pop();

            if (!node1 || !node2) {
                if (node1 != node2) return false;
                continue;
            }

            if (node1->val != node2->val) return false;

            if ((node1->left && node2->left && node1->left->val == node2->left->val) ||
                (!node1->left && !node2->left)) {
                stk.push({node1->left, node2->left});
                stk.push({node1->right, node2->right});
            } else {
                stk.push({node1->left, node2->right});
                stk.push({node1->right, node2->left});
            }
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
