# 101. Symmetric Tree

- **Difficulty:** Easy  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/symmetric-tree/>  
- **NeetCode:** <https://neetcode.io/problems/symmetric-tree>  
- **Video:** <https://www.youtube.com/watch?v=Mao9uzxwvmc>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

A tree is symmetric if its left subtree is a mirror reflection of its right subtree. Two trees are mirrors of each other if their roots have the same value, and the left subtree of one is a mirror of the right subtree of the other (and vice versa). We can check this recursively by comparing pairs of nodes that should be mirror images of each other.

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
    bool isSymmetric(TreeNode* root) {
        return dfs(root->left, root->right);
    }

private:
    bool dfs(TreeNode* left, TreeNode* right) {
        if (!left && !right) {
            return true;
        }
        if (!left || !right) {
            return false;
        }
        return (left->val == right->val) &&
                dfs(left->left, right->right) &&
                dfs(left->right, right->left);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Iterative DFS

The recursive solution can be converted to an iterative one using a stack. Instead of implicit recursive calls, we explicitly push pairs of nodes onto a stack. Each pair represents two nodes that should be mirror images. By processing pairs from the stack, we maintain the same comparison logic without recursion.

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
    bool isSymmetric(TreeNode* root) {
        if (!root) return true;

        std::stack<pair<TreeNode*, TreeNode*>> stack;
        stack.push({root->left, root->right});

        while (!stack.empty()) {
            auto [left, right] = stack.top();
            stack.pop();

            if (!left && !right) continue;
            if (!left || !right || left->val != right->val) {
                return false;
            }
            stack.push({left->left, right->right});
            stack.push({left->right, right->left});
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Breadth First Search

BFS processes nodes level by level using a queue. For symmetry checking, we enqueue pairs of nodes that should be mirrors. Processing the queue ensures we compare nodes at the same depth before moving deeper. This approach gives a level-by-level validation of the mirror property.

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
    bool isSymmetric(TreeNode* root) {
        if (!root) return true;

        queue<pair<TreeNode*, TreeNode*>> queue;
        queue.push({root->left, root->right});

        while (!queue.empty()) {
            for (int i = queue.size(); i > 0; i--) {
                auto [left, right] = queue.front();
                queue.pop();

                if (!left && !right) continue;
                if (!left || !right || left->val != right->val) {
                    return false;
                }
                queue.push({left->left, right->right});
                queue.push({left->right, right->left});
            }
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0101-symmetric-tree.cpp` in the NeetCode repo)

```cpp
/*
    Given the root of a binary tree, this function checks whether the tree is symmetric,
    i.e., whether it is a mirror of itself around its center.

    Time Complexity: O(n), where n is the number of nodes in the binary tree.
    Space Complexity: O(n), due to the recursive stack space.

    Approach:
    - If the root is NULL, return true (base case).
    - Recursively check if the left subtree of the root is mirrored with the right subtree.
    - To check if two subtrees are mirrored, compare their left and right children recursively.

    Example:
    Input: root = [1,2,2,3,4,4,3]
    Output: true

    Input: root = [1,2,2,null,3,null,3]
    Output: false
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
    bool isSymmetric(TreeNode* root) {
        return dfs(root, root);
    }

    bool dfs(TreeNode* left, TreeNode* right) {
        if (!left && !right)
            return true;
        if (!left || !right)
            return false;

        return left->val == right->val && dfs(left->left, right->right) && dfs(left->right, right->left);
    }
};
```
