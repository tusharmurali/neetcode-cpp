# 1609. Even Odd Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/even-odd-tree/>  
- **NeetCode:** <https://neetcode.io/problems/even-odd-tree>  
- **Video:** <https://www.youtube.com/watch?v=FkNWN1Fj_TY>  

[← Back to index](../INDEX.md)

## 1. Breadth First Search

An Even-Odd tree has specific constraints on each level: even-indexed levels must have strictly increasing odd values, while odd-indexed levels must have strictly decreasing even values. BFS naturally processes the tree level by level, making it ideal for checking these per-level conditions.

As we process each level, we track whether it is even or odd and verify that every node satisfies both the parity constraint (odd values on even levels, even values on odd levels) and the ordering constraint (increasing or decreasing based on level).

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
    bool isEvenOddTree(TreeNode* root) {
        bool even = true;
        queue<TreeNode*> q;
        q.push(root);

        while (!q.empty()) {
            int prev = even ? INT_MIN : INT_MAX;
            for (int i = q.size(); i > 0; i--) {
                TreeNode* node = q.front();q.pop();

                if (even && (node->val % 2 == 0 || node->val <= prev)) return false;
                if (!even && (node->val % 2 == 1 || node->val >= prev)) return false;

                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);

                prev = node->val;
            }
            even = !even;
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Depth First Search

DFS can also solve this problem by tracking the last seen value at each level. As we traverse the tree in preorder (left to right), the first time we visit a level establishes the starting value. Subsequent visits to that level must satisfy the ordering constraint relative to the previous value we recorded.

We maintain an array where `levels[i]` stores the most recently seen value at level `i`. This lets us check ordering across a level even though DFS does not process levels sequentially.

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
    vector<int> levels;

    bool dfs(TreeNode* node, int level) {
        if (!node) return true;

        bool even = level % 2 == 0;
        if ((even && node->val % 2 == 0) ||
            (!even && node->val % 2 == 1)) {
            return false;
        }

        if (levels.size() == level) {
            levels.push_back(node->val);
        } else {
            if ((even && node->val <= levels[level]) ||
                (!even && node->val >= levels[level])) {
                return false;
            }
            levels[level] = node->val;
        }

        return dfs(node->left, level + 1) && dfs(node->right, level + 1);
    }

    bool isEvenOddTree(TreeNode* root) {
        return dfs(root, 0);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Iterative DFS

This approach mimics recursive DFS using an explicit stack, which can help avoid stack overflow for very deep trees. We store `(node, level)` pairs on the stack and process nodes in a similar order to recursive DFS.

The same `levels` array tracks the last seen value at each depth. By pushing the `right` child before the `left` child, we ensure left-to-right traversal order when popping.

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
    bool isEvenOddTree(TreeNode* root) {
        stack<pair<TreeNode*, int>> stack;
        stack.push({root, 0});
        vector<int> levels;

        while (!stack.empty()) {
            auto [node, level] = stack.top();
            stack.pop();

            bool even = level % 2 == 0;
            if ((even && node->val % 2 == 0) ||
                (!even && node->val % 2 == 1))
                return false;

            if (levels.size() == level) {
                levels.push_back(node->val);
            } else {
                if ((even && node->val <= levels[level]) ||
                    (!even && node->val >= levels[level]))
                    return false;
                levels[level] = node->val;
            }

            if (node->right) stack.push({node->right, level + 1});
            if (node->left) stack.push({node->left, level + 1});
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
