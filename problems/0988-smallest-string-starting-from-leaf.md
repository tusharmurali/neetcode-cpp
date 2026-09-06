# 988. Smallest String Starting From Leaf

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/smallest-string-starting-from-leaf/>  
- **NeetCode:** <https://neetcode.io/problems/smallest-string-starting-from-leaf>  
- **Video:** <https://www.youtube.com/watch?v=UvdWfxQ_ZDs>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

We need to find the lexicographically smallest string that starts at a leaf and ends at the root. Since strings are built from leaf to root, we traverse the tree while building the string by prepending each node's character. When we reach a leaf, we have a complete string to compare. By exploring all paths and keeping track of the minimum string found, we get our answer.

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
    string smallestFromLeaf(TreeNode* root) {
        return dfs(root, "");
    }

private:
    string dfs(TreeNode* root, string cur) {
        if (!root) return "";

        cur = char('a' + root->val) + cur;
        if (root->left && root->right) {
            return min(dfs(root->left, cur), dfs(root->right, cur));
        }

        if (root->right) return dfs(root->right, cur);
        if (root->left) return dfs(root->left, cur);
        return cur;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 2. Breadth First Search

Instead of recursion, we can use a queue to traverse the tree level by level. Each queue entry stores a node along with the string built from the root down to that node. When we encounter a leaf, we compare its complete string with the current minimum. BFS naturally explores all paths, and we simply track the smallest leaf-to-root string found.

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
    string smallestFromLeaf(TreeNode* root) {
        queue<pair<TreeNode*, string>> q;
        q.push({root, ""});
        string res;

        while (!q.empty()) {
            auto [node, cur] = q.front();
            q.pop();
            cur = char('a' + node->val) + cur;

            if (!node->left && !node->right) {
                if (res.empty() || cur < res) {
                    res = cur;
                }
            }

            if (node->left) q.push({node->left, cur});
            if (node->right) q.push({node->right, cur});
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Iterative DFS

This approach mirrors the recursive DFS but uses an explicit stack instead of the call stack. We push nodes along with their accumulated strings onto the stack. By processing nodes in LIFO order, we achieve depth-first traversal. The logic for building strings and comparing at leaves remains the same as the recursive version.

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
    string smallestFromLeaf(TreeNode* root) {
        stack<pair<TreeNode*, string>> stk;
        stk.push({root, ""});
        string res;

        while (!stk.empty()) {
            auto [node, cur] = stk.top();stk.pop();
            cur = char('a' + node->val) + cur;

            if (!node->left && !node->right) {
                if (res.empty() || cur < res) {
                    res = cur;
                }
            }

            if (node->right) stk.push({node->right, cur});
            if (node->left) stk.push({node->left, cur});
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$
