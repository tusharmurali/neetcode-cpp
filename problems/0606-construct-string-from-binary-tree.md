# 606. Construct String From Binary Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/construct-string-from-binary-tree/>  
- **NeetCode:** <https://neetcode.io/problems/construct-string-from-binary-tree>  
- **Video:** <https://www.youtube.com/watch?v=b1WpYxnuebQ>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

We need to create a string representation using preorder traversal with parentheses. The key observation is handling empty subtrees: we must include empty parentheses `()` for a missing left child only when a right child exists (to preserve the tree structure), but we can omit parentheses for a missing right child entirely.

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
    string tree2str(TreeNode* root) {
        if (!root) {
            return "";
        }

        string cur = to_string(root->val);
        string left = tree2str(root->left);
        string right = tree2str(root->right);

        if (!left.empty() && !right.empty()) {
            return cur + "(" + left + ")(" + right + ")";
        }

        if (!right.empty()) {
            return cur + "()(" + right + ")";
        }

        if (!left.empty()) {
            return cur + "(" + left + ")";
        }

        return cur;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Depth First Search (Optimal)

The previous approach creates many intermediate strings during concatenation, which is inefficient. Instead, we can use a StringBuilder (or list) to accumulate characters. We always add an opening parenthesis before processing a node and a closing parenthesis after, then trim the outermost parentheses at the end.

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
    string tree2str(TreeNode* root) {
        string res;
        preorder(root, res);
        return res.substr(1, res.size() - 2);
    }

private:
    void preorder(TreeNode* root, string& res) {
        if (!root) return;

        res += "(" + to_string(root->val);
        if (!root->left && root->right) {
            res += "()";
        }
        preorder(root->left, res);
        preorder(root->right, res);
        res += ")";
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Iterative DFS

We can convert the recursive approach to iterative using an explicit stack. The challenge is knowing when we have finished processing a node's subtrees so we can add the closing parenthesis. We track the last visited node to determine whether we are returning from the right subtree.

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
    string tree2str(TreeNode* root) {
        if (!root) {
            return "";
        }

        string res;
        stack<TreeNode*> stack;
        TreeNode* lastVisited = nullptr;
        TreeNode* cur = root;

        while (cur || !stack.empty()) {
            if (cur) {
                res += "(" + to_string(cur->val);
                if (!cur->left && cur->right) {
                    res += "()";
                }

                stack.push(cur);
                cur = cur->left;
            } else {
                TreeNode* top = stack.top();
                if (top->right && lastVisited != top->right) {
                    cur = top->right;
                } else {
                    stack.pop();
                    res += ")";
                    lastVisited = top;
                }
            }
        }

        return res.substr(1, res.size() - 2);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0606-construct-string-from-binary-tree.cpp` in the NeetCode repo)

```cpp
/*
0606-construct-string-from-binary-tree.cpp

Algorithm Used: Preorder

Time Complexity: O(n)
n is number of nodes

Space Complexity: O(h)
h is height of binary tree

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
    string tree2str(TreeNode* root) {
        if (!root) return "";
        string ans = to_string(root->val);
        if (root->right) {
            ans = ans + "(" + tree2str(root->left) + ")";
            ans = ans + "(" + tree2str(root->right) + ")";
        } else if (root->left) {
            ans = ans + "(" + tree2str(root->left) + ")";
        }
        return ans;
    }
};
```
