# 513. Find Bottom Left Tree Value

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-bottom-left-tree-value/>  
- **NeetCode:** <https://neetcode.io/problems/find-bottom-left-tree-value>  
- **Video:** <https://www.youtube.com/watch?v=u_by_cTsNJA>  

[← Back to index](../INDEX.md)

## 1. Breadth First Search

We need the leftmost value in the bottom row of the tree. A clever BFS trick handles this: instead of traversing left-to-right, we process nodes right-to-left. This way, the last node we visit in the entire traversal is exactly the bottom-left node. No need to track levels or compare positions.

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
    int findBottomLeftValue(TreeNode* root) {
        queue<TreeNode*> q;
        q.push(root);
        TreeNode* node = nullptr;

        while (!q.empty()) {
            node = q.front();
            q.pop();
            if (node->right) q.push(node->right);
            if (node->left) q.push(node->left);
        }
        return node->val;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Depth First Search

Using DFS, we track the maximum depth seen so far. Whenever we reach a new maximum depth, we update our result with the current node's value. By visiting the left subtree before the right subtree, the first node we encounter at any given depth is guaranteed to be the leftmost one at that level.

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
    int maxDepth = -1, res;

    int findBottomLeftValue(TreeNode* root) {
        res = root->val;
        dfs(root, 0);
        return res;
    }

private:
    void dfs(TreeNode* node, int depth) {
        if (!node) return;
        if (depth > maxDepth) {
            maxDepth = depth;
            res = node->val;
        }

        dfs(node->left, depth + 1);
        dfs(node->right, depth + 1);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 3. Iterative DFS

This is the same logic as recursive DFS, but uses an explicit stack instead of the call stack. We push nodes along with their depths and process them in LIFO order. By pushing the right child before the left child, we ensure left children are processed first at each level, maintaining the leftmost-first property.

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
    int findBottomLeftValue(TreeNode* root) {
        int res = root->val, maxDepth = -1;
        stack<pair<TreeNode*, int>> stack;
        stack.push({root, 0});

        while (!stack.empty()) {
            auto [node, depth] = stack.top();stack.pop();
            if (depth > maxDepth) {
                maxDepth = depth;
                res = node->val;
            }

            if (node->right) {
                stack.push({node->right, depth + 1});
            }
            if (node->left) {
                stack.push({node->left, depth + 1});
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Morris Traversal

Morris traversal lets us traverse the tree without using extra space for a stack or recursion. We temporarily modify the tree by threading right pointers of predecessor nodes back to their successors, creating a way to return after visiting the left subtree. We track depth manually by counting steps down and back up, updating our result whenever we reach a new maximum depth.

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
    int findBottomLeftValue(TreeNode* root) {
        int res = root->val, maxDepth = -1, curDepth = 0;
        TreeNode* cur = root;

        while (cur) {
            if (!cur->left) {
                if (curDepth > maxDepth) {
                    maxDepth = curDepth;
                    res = cur->val;
                }
                cur = cur->right;
                curDepth++;
            } else {
                TreeNode* prev = cur->left;
                int steps = 1;
                while (prev->right && prev->right != cur) {
                    prev = prev->right;
                    steps++;
                }

                if (!prev->right) {
                    prev->right = cur;
                    cur = cur->left;
                    curDepth++;
                } else {
                    prev->right = nullptr;
                    curDepth -= steps;
                    cur = cur->right;
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
