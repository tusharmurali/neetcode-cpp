# 515. Find Largest Value in Tree Row

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-largest-value-in-each-tree-row/>  
- **NeetCode:** <https://neetcode.io/problems/find-largest-value-in-each-tree-row>  
- **Video:** <https://www.youtube.com/watch?v=wB9JOh7Z_cY>  

[← Back to index](../INDEX.md)

## 1. Breadth First Search

To find the largest value in each row, we need to visit all nodes level by level. BFS naturally processes nodes in level order using a queue. For each level, we track the maximum value seen among all nodes at that depth.

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
    vector<int> largestValues(TreeNode* root) {
        if (!root) return {};

        vector<int> res;
        queue<TreeNode*> q;
        q.push(root);

        while (!q.empty()) {
            int rowMax = q.front()->val;
            for (int i = q.size(); i > 0; i--) {
                TreeNode* node = q.front(); q.pop();
                rowMax = max(rowMax, node->val);
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
            res.push_back(rowMax);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Depth First Search

We can also solve this with DFS by tracking the current depth as we traverse. When we reach a node, if it's the first node at that depth, we add it to the result. Otherwise, we compare it with the existing maximum for that depth and update if necessary.

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
    vector<int> largestValues(TreeNode* root) {
        vector<int> res;
        dfs(root, 0, res);
        return res;
    }

private:
    void dfs(TreeNode* node, int level, vector<int>& res) {
        if (!node) return;
        if (level == res.size()) {
            res.push_back(node->val);
        } else {
            res[level] = max(res[level], node->val);
        }

        dfs(node->left, level + 1, res);
        dfs(node->right, level + 1, res);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 3. Iterative DFS

The recursive DFS can be converted to an iterative approach using a stack. Each stack entry stores both the node and its level. This avoids recursion overhead while maintaining the same logic.

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
    vector<int> largestValues(TreeNode* root) {
        if (!root) return {};

        vector<int> res;
        stack<pair<TreeNode*, int>> stk;
        stk.push({root, 0});
        while (!stk.empty()) {
            auto [node, level] = stk.top();stk.pop();
            if (level == res.size()) {
                res.push_back(node->val);
            } else {
                res[level] = max(res[level], node->val);
            }

            if (node->right) stk.push({node->right, level + 1});
            if (node->left) stk.push({node->left, level + 1});
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
