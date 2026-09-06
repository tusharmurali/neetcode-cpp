# 337. House Robber III

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/house-robber-iii/>  
- **NeetCode:** <https://neetcode.io/problems/house-robber-iii>  
- **Video:** <https://www.youtube.com/watch?v=nHR8ytpzz7c>  

[← Back to index](../INDEX.md)

## 1. Recursion

This is a tree version of the classic house robber problem.
At each node, we have two choices: rob it or skip it.
If we rob the current node, we cannot rob its immediate children, so we must skip to the grandchildren.
If we skip the current node, we can consider robbing its children.
We take the maximum of these two options.

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
    int rob(TreeNode* root) {
        if (!root) {
            return 0;
        }

        int res = root->val;
        if (root->left) {
            res += rob(root->left->left) + rob(root->left->right);
        }
        if (root->right) {
            res += rob(root->right->left) + rob(root->right->right);
        }

        res = max(res, rob(root->left) + rob(root->right));
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Dynamic Programming (Memoization)

The recursive solution recomputes results for the same nodes multiple times.
By storing computed results in a cache (hash map), we avoid redundant work.
Each node is processed at most once, significantly improving efficiency.

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
    unordered_map<TreeNode*, int> cache;

public:
    int rob(TreeNode* root) {
        cache[nullptr] = 0;
        return dfs(root);
    }

private:
    int dfs(TreeNode* root) {
        if (cache.find(root) != cache.end()) {
            return cache[root];
        }

        int res = root->val;
        if (root->left) {
            res += rob(root->left->left) + rob(root->left->right);
        }
        if (root->right) {
            res += rob(root->right->left) + rob(root->right->right);
        }

        res = max(res, rob(root->left) + rob(root->right));
        cache[root] = res;
        return res;

    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Optimal)

Instead of caching all nodes, we can return two values from each subtree: the maximum if we rob this node, and the maximum if we skip it.
This eliminates the need for a hash map.
For each node, "with root" equals the node value plus the "without" values of both children.
"Without root" equals the sum of the maximum values (either with or without) from both children.

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
    int rob(TreeNode* root) {
        auto result = dfs(root);
        return max(result.first, result.second);
    }

private:
    pair<int, int> dfs(TreeNode* root) {
        if (!root) {
            return {0, 0};
        }

        auto leftPair = dfs(root->left);
        auto rightPair = dfs(root->right);

        int withRoot = root->val + leftPair.second + rightPair.second;
        int withoutRoot = max(leftPair.first, leftPair.second) +
                          max(rightPair.first, rightPair.second);

        return {withRoot, withoutRoot};
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.
