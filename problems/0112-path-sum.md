# 112. Path Sum

- **Difficulty:** Easy  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/path-sum/>  
- **NeetCode:** <https://neetcode.io/problems/path-sum>  
- **Video:** <https://www.youtube.com/watch?v=LSKQyOz_P8I>  

[← Back to index](../INDEX.md)

## 1. Depth First Search - I

We traverse the tree from root to leaves, accumulating the sum along the way. When we reach a leaf node, we check if the accumulated sum equals the target. `dfs` naturally explores all root-to-leaf paths, making it ideal for this problem.

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
    bool hasPathSum(TreeNode* root, int targetSum) {
        return dfs(root, 0, targetSum);
    }

private:
    bool dfs(TreeNode* node, int curSum, int targetSum) {
        if (node == nullptr) return false;

        curSum += node->val;
        if (node->left == nullptr && node->right == nullptr) {
            return curSum == targetSum;
        }

        return dfs(node->left, curSum, targetSum) || dfs(node->right, curSum, targetSum);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Depth First Search - II

Instead of accumulating a sum, we subtract each node's value from the target. When we reach a leaf, we check if the remaining target is zero. This approach avoids passing an extra parameter and keeps the logic clean.

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
    bool hasPathSum(TreeNode* root, int targetSum) {
        if (!root) return false;
        targetSum -= root->val;
        return hasPathSum(root->left, targetSum) ||
               hasPathSum(root->right, targetSum) ||
               (targetSum == 0 && !root->left && !root->right);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 3. Iterative DFS

We can simulate the recursive `dfs` using an explicit stack. Each stack entry stores a node and the remaining sum needed to reach the target from that node. This approach avoids recursion depth issues for very deep trees.

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
    bool hasPathSum(TreeNode* root, int targetSum) {
        if (!root) return false;

        stack<pair<TreeNode*, int>> s;
        s.push({root, targetSum - root->val});

        while (!s.empty()) {
            auto [node, currSum] = s.top();
            s.pop();

            if (!node->left && !node->right && currSum == 0) {
                return true;
            }

            if (node->right) {
                s.push({node->right, currSum - node->right->val});
            }

            if (node->left) {
                s.push({node->left, currSum - node->left->val});
            }
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Breadth First Search

`bfs` explores the tree level by level. We use a queue to store each node along with the remaining sum needed. When we reach a leaf, we check if the target has been met. BFS guarantees we explore all paths systematically.

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
    bool hasPathSum(TreeNode* root, int targetSum) {
        if (!root) return false;

        queue<pair<TreeNode*, int>> q;
        q.push({root, targetSum - root->val});

        while (!q.empty()) {
            auto [node, currSum] = q.front();
            q.pop();

            if (!node->left && !node->right && currSum == 0) {
                return true;
            }

            if (node->left) {
                q.push({node->left, currSum - node->left->val});
            }

            if (node->right) {
                q.push({node->right, currSum - node->right->val});
            }
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0112-path-sum.cpp` in the NeetCode repo)

```cpp
/*
0112-path-sum.cpp
Given the root of a binary tree and an integer targetSum, return true if the tree has a root-to-leaf path such that adding up all the values along the path equals targetSum.

A leaf is a node with no children.

Algorithm Used : DFS

Time Complexity : O(n)
n = number of nodes in binary tree

Space Complexity : O(h)
h = height of binary tree

*/

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
    bool hasPathSum(TreeNode* root, int targetSum) {
        if (!root) return false;

        targetSum -= root->val;

        if (!root->left && !root->right && (targetSum == 0)) return true;

        return hasPathSum(root->left, targetSum) || hasPathSum(root->right, targetSum);
    }
};
```
