# 1457. Pseudo-Palindromic Paths in a Binary Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/pseudo-palindromic-paths-in-a-binary-tree/>  
- **NeetCode:** <https://neetcode.io/problems/pseudo-palindromic-paths-in-a-binary-tree>  
- **Video:** <https://www.youtube.com/watch?v=MBsSpQnaFzg>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

A path can form a palindrome if at most one digit has an odd count (that digit would go in the middle). As we traverse from root to leaf, we track the count of each digit and maintain a running count of how many digits have odd frequency. At each leaf, we check if the odd count is at most `1`.

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
    int pseudoPalindromicPaths(TreeNode* root) {
        unordered_map<int, int> count;
        int odd = 0;
        return dfs(root, count, odd);
    }

private:
    int dfs(TreeNode* cur, unordered_map<int, int>& count, int& odd) {
        if (!cur) return 0;

        count[cur->val]++;
        int odd_change = (count[cur->val] % 2 == 1) ? 1 : -1;
        odd += odd_change;

        int res;
        if (!cur->left && !cur->right) {
            res = (odd <= 1) ? 1 : 0;
        } else {
            res = dfs(cur->left, count, odd) + dfs(cur->right, count, odd);
        }

        odd -= odd_change;
        count[cur->val]--;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(h)$ for recursion stack.

> Where $n$ is the number of nodes and $h$ is the height of the given tree.

## 2. Depth First Search (Using Array)

Instead of a hash map, we use a fixed-size array since node values are limited to 1-9. We track odd/even counts using XOR: toggling a bit each time a digit appears. This gives a cleaner way to track parity while maintaining the same core logic of counting odd-frequency digits.

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
    int pseudoPalindromicPaths(TreeNode* root) {
        int count[10] = {};
        return dfs(root, count, 0);
    }

private:
    int dfs(TreeNode* cur, int count[], int odd) {
        if (!cur) return 0;

        count[cur->val] ^= 1;
        odd += (count[cur->val] == 1) ? 1 : -1;

        int res = (!cur->left && !cur->right && odd <= 1) ? 1
                  : dfs(cur->left, count, odd) + dfs(cur->right, count, odd);

        odd += (count[cur->val] == 1) ? 1 : -1;
        count[cur->val] ^= 1;

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(h)$ for recursion stack.

> Where $n$ is the number of nodes and $h$ is the height of the given tree.

## 3. Depth First Search (Bit Mask)

We can encode all parity information in a single integer using bits. Each bit position represents a digit, and the bit is 1 if that digit has appeared an odd number of times. XOR toggles the bit on each occurrence. At a leaf, if the path is pseudo-palindromic, at most one bit should be set. We check this with the trick: `path & (path - 1) == 0` (true for 0 or exactly one bit set).

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
    int pseudoPalindromicPaths(TreeNode* root) {
        return dfs(root, 0);
    }

private:
    int dfs(TreeNode* node, int path) {
        if (!node) return 0;

        path ^= (1 << node->val);
        if (!node->left && !node->right) {
            return (path & (path - 1)) == 0 ? 1 : 0;
        }

        return dfs(node->left, path) + dfs(node->right, path);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(h)$ for recursion stack.

> Where $n$ is the number of nodes and $h$ is the height of the given tree.

## 4. Breadth First Search

BFS traverses level by level using a queue. We pair each node with its current path bitmask. When we reach a leaf, we check if the path can form a palindrome using the same bit trick. This approach uses more space than DFS but processes nodes in breadth-first order.

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
    int pseudoPalindromicPaths(TreeNode* root) {
        int res = 0;
        queue<pair<TreeNode*, int>> q;
        q.push({root, 0});
        while (!q.empty()) {
            auto [node, path] = q.front();q.pop();
            path ^= (1 << node->val);

            if (!node->left && !node->right) {
                if ((path & (path - 1)) == 0) res++;
                continue;
            }

            if (node->left) q.push({node->left, path});
            if (node->right) q.push({node->right, path});
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 5. Iterative DFS

We can simulate recursive DFS using an explicit stack. Each stack entry contains a node and the path bitmask accumulated so far. This avoids recursion overhead and potential stack overflow for very deep trees, while maintaining the same DFS traversal order.

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
    int pseudoPalindromicPaths(TreeNode* root) {
        stack<pair<TreeNode*, int>> s;
        s.push({root, 0});
        int count = 0;

        while (!s.empty()) {
            auto [node, path] = s.top();
            s.pop();
            path ^= (1 << node->val);

            if (!node->left && !node->right) {
                if ((path & (path - 1)) == 0) count++;
            } else {
                if (node->right) s.push({node->right, path});
                if (node->left) s.push({node->left, path});
            }
        }

        return count;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(h)$

> Where $n$ is the number of nodes and $h$ is the height of the given tree.
