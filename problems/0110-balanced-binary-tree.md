# 110. Balanced Binary Tree

- **Difficulty:** Easy  
- **Pattern:** Trees  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/balanced-binary-tree/>  
- **NeetCode:** <https://neetcode.io/problems/balanced-binary-tree>  
- **Video:** <https://www.youtube.com/watch?v=QfJsau0ItOY>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A tree is balanced if **every node’s left and right subtree heights differ by at most 1**.

The brute-force approach directly follows the definition:

- For every node, compute the height of its left subtree.
- Compute the height of its right subtree.
- Check if their difference is ≤ 1.
- Recursively repeat this check for all nodes.

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
    bool isBalanced(TreeNode* root) {
        if (!root) return true;

        int left = height(root->left);
        int right = height(root->right);
        if (abs(left - right) > 1) return false;
        return isBalanced(root->left) && isBalanced(root->right);
    }

    int height(TreeNode* root) {
        if (root == nullptr) {
            return 0;
        }

        return 1 + max(height(root->left), height(root->right));
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Depth First Search

The brute-force solution wastes time by repeatedly recomputing subtree heights.  
We fix this by doing **one DFS that returns two things at once** for every node:

1. **Is the subtree balanced?** (`True`/`False`)
2. **What is its height?**

This way, each subtree is processed only once.  
If at any node the height difference > 1, we mark it as unbalanced and stop worrying about deeper levels.

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
    bool isBalanced(TreeNode* root) {
        return dfs(root)[0] == 1;
    }

private:
    vector<int> dfs(TreeNode* root) {
        if (!root) {
            return {1, 0};
        }

        vector<int> left = dfs(root->left);
        vector<int> right = dfs(root->right);

        bool balanced = (left[0] == 1 && right[0] == 1) &&
                        (abs(left[1] - right[1]) <= 1);
        int height = 1 + max(left[1], right[1]);

        return {balanced ? 1 : 0, height};
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(h)$
    - Best Case ([balanced tree](https://www.geeksforgeeks.org/balanced-binary-tree/)): $O(log(n))$
    - Worst Case ([degenerate tree](https://www.geeksforgeeks.org/introduction-to-degenerate-binary-tree/)): $O(n)$

> Where $n$ is the number of nodes in the tree and $h$ is the height of the tree.

## 3. Iterative DFS

The recursive DFS solution computes height and balance in one postorder traversal.  
This iterative version does **the same thing**, but simulates recursion using a stack.

The idea:

- We must visit each node **after** its children (postorder).
- Once both children of a node are processed, we already know their heights.
- Then we:
    1. Check if the height difference ≤ `1`
    2. Save the node's height (`1 + max(left, right)`)

If any node is unbalanced, return `false` immediately.

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
    bool isBalanced(TreeNode* root) {
        stack<TreeNode*> stack;
        TreeNode* node = root;
        TreeNode* last = nullptr;
        unordered_map<TreeNode*, int> depths;

        while (!stack.empty() || node != nullptr) {
            if (node != nullptr) {
                stack.push(node);
                node = node->left;
            } else {
                node = stack.top();
                if (node->right == nullptr || last == node->right) {
                    stack.pop();
                    int left = depths[node->left];
                    int right = depths[node->right];
                    if (abs(left - right) > 1) return false;
                    depths[node] = 1 + max(left, right);
                    last = node;
                    node = nullptr;
                } else {
                    node = node->right;
                }
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0110-balanced-binary-tree.cpp` in the NeetCode repo)

```cpp
/*
    Given binary tree, determine if height-balanced (all left & right subtrees height diff <= 1)

    Check if subtrees are balanced, if so, use their heights to determine further balance

    Time: O(n)
    Space: O(n)
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
    bool isBalanced(TreeNode* root) {
        int height = 0;
        return dfs(root, height);
    }
private:
    bool dfs(TreeNode* root, int& height) {
        if (root == NULL) {
            height = -1;
            return true;
        }
        
        int left = 0;
        int right = 0;
        
        if (!dfs(root->left, left) || !dfs(root->right, right)) {
            return false;
        }
        if (abs(left - right) > 1) {
            return false;
        }
        
        height = 1 + max(left, right);
        return true;
    }
};
```
