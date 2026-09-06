# 314. Binary Tree Vertical Order Traversal

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/binary-tree-vertical-order-traversal/>  
- **NeetCode:** <https://neetcode.io/problems/binary-tree-vertical-order-traversal>  
- **Video:** <https://www.youtube.com/watch?v=-JFngYs21Y8>  

[← Back to index](../INDEX.md)

## 1. Breadth First Search + Sorting

We assign each node a column index where the root is at column `0`, left children are at `column - 1`, and right children are at `column + 1`. Using BFS ensures we visit nodes level by level, so nodes in the same column appear in top-to-bottom order. We group nodes by their column index and sort the columns to get the final result.

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
    vector<vector<int>> verticalOrder(TreeNode* root) {
        if (!root) return {};
        map<int, vector<int>> cols;
        queue<pair<TreeNode*, int>> q;
        q.push({root, 0});

        while (!q.empty()) {
            auto [node, pos] = q.front(); q.pop();
            cols[pos].push_back(node->val);
            if (node->left) q.push({node->left, pos - 1});
            if (node->right) q.push({node->right, pos + 1});
        }

        vector<vector<int>> res;
        for (auto& [_, vec] : cols)
            res.push_back(vec);
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Depth First Search + Sorting

DFS can also solve this problem, but we need to track each node's row to maintain the correct vertical order within columns. Since DFS doesn't naturally visit nodes in level order, we store both the row and value for each node. After traversal, we sort each column by row index to ensure nodes appear in top-to-bottom order.

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
    map<int, vector<pair<int, int>>> cols;

    void dfs(TreeNode* node, int row, int col) {
        if (!node) return;
        cols[col].push_back({row, node->val});
        dfs(node->left, row + 1, col - 1);
        dfs(node->right, row + 1, col + 1);
    }

public:
    vector<vector<int>> verticalOrder(TreeNode* root) {
        dfs(root, 0, 0);
        vector<vector<int>> res;

        for (auto& [col, vec] : cols) {
            stable_sort(vec.begin(), vec.end(),
                        [](const pair<int, int>& a, const pair<int, int>& b) {
                            return a.first < b.first;  // sort ONLY by row
                        });

            vector<int> colVals;
            for (auto& [_, val] : vec)
                colVals.push_back(val);
            res.push_back(colVals);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n \log n)$

## 3. Breadth First Search (Optimal)

Instead of sorting all column keys at the end, we can track the minimum and maximum column indices during traversal. This allows us to iterate from the leftmost to rightmost column directly without sorting, reducing the time complexity.

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
    vector<vector<int>> verticalOrder(TreeNode* root) {
        if (!root) return {};

        unordered_map<int, vector<int>> cols;
        queue<pair<TreeNode*, int>> q;
        q.push({root, 0});
        int minCol = 0, maxCol = 0;

        while (!q.empty()) {
            auto [node, col] = q.front(); q.pop();
            cols[col].push_back(node->val);
            minCol = min(minCol, col);
            maxCol = max(maxCol, col);

            if (node->left) q.push({node->left, col - 1});
            if (node->right) q.push({node->right, col + 1});
        }

        vector<vector<int>> res;
        for (int c = minCol; c <= maxCol; ++c)
            res.push_back(cols[c]);

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Depth First Search (Optimal)

Similar to the optimal BFS approach, we track min and max column indices during DFS to avoid sorting columns. However, we still need to store row information and sort within each column since DFS doesn't visit nodes in level order. This approach reduces the complexity of iterating over columns while still requiring per-column sorting.

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
    unordered_map<int, vector<pair<int, int>>> cols;
    int minCol = 0, maxCol = 0;

    void dfs(TreeNode* node, int row, int col) {
        if (!node) return;
        cols[col].emplace_back(row, node->val);
        minCol = min(minCol, col);
        maxCol = max(maxCol, col);
        dfs(node->left, row + 1, col - 1);
        dfs(node->right, row + 1, col + 1);
    }

public:
    vector<vector<int>> verticalOrder(TreeNode* root) {
        if (!root) return {};
        dfs(root, 0, 0);
        vector<vector<int>> res;

        for (int c = minCol; c <= maxCol; ++c) {
            auto& vec = cols[c];
            stable_sort(vec.begin(), vec.end(),
                        [](const pair<int, int>& a, const pair<int, int>& b) {
                            return a.first < b.first; // sort by row only
                        });
            vector<int> colVals;
            for (auto& [_, val] : vec)
                colVals.push_back(val);
            res.push_back(colVals);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(w * h \log h)$
- Space complexity: $O(n)$

> Where $n$ is the number of nodes, $h$ is the height of the tree (i.e. maximum number of nodes in any vertical line of the tree), and $w$ is the width of the tree (i.e. maximum number of nodes in any of the levels of the tree).
