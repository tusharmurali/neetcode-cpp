# 662. Maximum Width of Binary Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-width-of-binary-tree/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-width-of-binary-tree>  
- **Video:** <https://www.youtube.com/watch?v=FPzLE2L7uHs>  

[← Back to index](../INDEX.md)

## 1. Breadth First Search

The width of a level is defined by the distance between the leftmost and rightmost non-null nodes, including any null nodes in between. To measure this, we assign each node a position number: the root is `1`, and for any node at position `p`, its left child is at `2 * p` and right child at `2 * p + 1`. Using BFS, we traverse level by level and compute the width as the difference between the last and first position on each level, plus one.

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
    int widthOfBinaryTree(TreeNode* root) {
        if (!root) return 0;

        int res = 0;
        queue<tuple<TreeNode*, uint, int>> q; // [node, num, level]
        q.push({root, 1, 0});
        int prevLevel = 0, prevNum = 1;

        while (!q.empty()) {
            auto [node, num, level] = q.front();
            q.pop();

            if (level > prevLevel) {
                prevLevel = level;
                prevNum = num;
            }

            res = max(res, int(num - prevNum) + 1);
            if (node->left) {
                q.push({node->left, 2 * num, level + 1});
            }
            if (node->right) {
                q.push({node->right, 2 * num + 1, level + 1});
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Breadth First Search (Optimal)

Position numbers can grow large in deep skewed trees, potentially causing overflow. To prevent this, we normalize positions at each level by subtracting the starting position of that level. This keeps the numbers small while still correctly computing the width as the difference between the rightmost and leftmost positions on each level.

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
    int widthOfBinaryTree(TreeNode* root) {
        int res = 0;
        queue<pair<TreeNode*, uint>> q;
        q.push({root, 0});

        while (!q.empty()) {
            int start = q.front().second;

            for (int i = q.size(); i > 0; --i) {
                auto [node, num] = q.front();
                q.pop();
                uint curNum = num - start;
                res = max(res, int(curNum) + 1);
                if (node->left) {
                    q.push({node->left, 2 * curNum});
                }
                if (node->right) {
                    q.push({node->right, 2 * curNum + 1});
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Depth First Search

We can also solve this with DFS by recording the first position encountered at each level. As we traverse, whenever we visit a node, we check if its level has been seen before. If not, we record its position as the first for that level. The width at any node is computed as the difference from the first position on its level. We normalize child positions to avoid overflow.

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
    unordered_map<int, unsigned long long> first;

public:
    int widthOfBinaryTree(TreeNode* root) {
        unsigned long long res = 0;

        dfs(root, 0, 0, res);
        return int(res);
    }

private:
    void dfs(TreeNode* node, int level, unsigned long long num, unsigned long long& res) {
        if (!node) {
            return;
        }

        if (!first.count(level)) {
            first[level] = num;
        }

        res = max(res, num - first[level] + 1);
        dfs(node->left, level + 1, 2 * (num - first[level]), res);
        dfs(node->right, level + 1, 2 * (num - first[level]) + 1, res);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
