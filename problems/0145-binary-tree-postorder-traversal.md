# 145. Binary Tree Postorder Traversal

- **Difficulty:** Easy  
- **Pattern:** Trees  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/binary-tree-postorder-traversal/>  
- **NeetCode:** <https://neetcode.io/problems/binary-tree-postorder-traversal>  
- **Video:** <https://www.youtube.com/watch?v=QhszUQhGGlA>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

Postorder traversal visits nodes in the order: left subtree, right subtree, current node. This is useful when we need to process children before their parent, such as when deleting nodes or evaluating expression trees. Recursion naturally handles this by processing both subtrees before adding the current node's value.

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
    vector<int> res;

public:
    vector<int> postorderTraversal(TreeNode* root) {
        postorder(root);
        return res;
    }

private:
    void postorder(TreeNode* node) {
        if (!node) {
            return;
        }
        postorder(node->left);
        postorder(node->right);
        res.push_back(node->val);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(n)$ space for the recursion stack.
    - $O(n)$ space for the output array.

## 2. Iterative Depth First Search - I

We use a stack with a `visited` flag to track whether we've already processed a node's children. When we first encounter a node, we push it back with a `visited` flag set to `true`, then push its children. On the second visit (when the flag is `true`), we know both children have been processed, so we add the node's value to the result.

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
    vector<int> postorderTraversal(TreeNode* root) {
        stack<TreeNode*> stk;
        stack<bool> visit;
        vector<int> res;

        stk.push(root);
        visit.push(false);

        while (!stk.empty()) {
            TreeNode* cur = stk.top();
            bool v = visit.top();
            stk.pop();
            visit.pop();

            if (cur) {
                if (v) {
                    res.push_back(cur->val);
                } else {
                    stk.push(cur);
                    visit.push(true);
                    stk.push(cur->right);
                    visit.push(false);
                    stk.push(cur->left);
                    visit.push(false);
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(n)$ space for the stacks.
    - $O(n)$ space for the output array.

## 3. Iterative Depth First Search - II

Postorder is the reverse of a modified preorder traversal. If we traverse in the order: current, right, left (instead of current, left, right), and then reverse the result, we get the postorder sequence. This avoids the complexity of tracking visited nodes.

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
    vector<int> postorderTraversal(TreeNode* root) {
        vector<int> res;
        stack<TreeNode*> stack;
        TreeNode* cur = root;

        while (cur || !stack.empty()) {
            if (cur) {
                res.push_back(cur->val);
                stack.push(cur);
                cur = cur->right;
            } else {
                cur = stack.top();
                stack.pop();
                cur = cur->left;
            }
        }

        reverse(res.begin(), res.end());
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(n)$ space for the stack.
    - $O(n)$ space for the output array.

## 4. Morris Traversal

Similar to the iterative approach that reverses a modified preorder, Morris Traversal for postorder works by performing a reverse preorder traversal (current, right, left) without using extra space for a stack. We use temporary thread links from the leftmost node of the right subtree back to the current node. After the traversal, we reverse the result.

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
    vector<int> postorderTraversal(TreeNode* root) {
        vector<int> res;
        TreeNode* cur = root;

        while (cur) {
            if (!cur->right) {
                res.push_back(cur->val);
                cur = cur->left;
            } else {
                TreeNode* prev = cur->right;
                while (prev->left && prev->left != cur) {
                    prev = prev->left;
                }

                if (!prev->left) {
                    res.push_back(cur->val);
                    prev->left = cur;
                    cur = cur->right;
                } else {
                    prev->left = nullptr;
                    cur = cur->left;
                }
            }
        }

        reverse(res.begin(), res.end());
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output array.

## Standalone solution file (`cpp/0145-binary-tree-postorder-traversal.cpp` in the NeetCode repo)

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
    vector<int> postorderTraversal(TreeNode* root) {
        if(!root) return {}; 

        postorderTraversal(root->left);
        postorderTraversal(root->right);
        result.push_back(root->val);
        
        return result;
    }
private:
    vector<int> result;
};
```
