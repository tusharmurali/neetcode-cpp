# 144. Binary Tree Preorder Traversal

- **Difficulty:** Easy  
- **Pattern:** Trees  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/binary-tree-preorder-traversal/>  
- **NeetCode:** <https://neetcode.io/problems/binary-tree-preorder-traversal>  
- **Video:** <https://www.youtube.com/watch?v=afTpieEZXck>  
- **Video approach:** 2. Iterative Depth First Search  

[← Back to index](../INDEX.md)

## 1. Depth First Search

Preorder traversal visits nodes in this exact order:

**1. Node itself → 2. Left subtree → 3. Right subtree**

So we simply start at the root and:

- Record its value,
- Recursively explore the left child,
- Then recursively explore the right child.

This naturally follows the preorder definition, and recursion handles the tree structure automatically.

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
    vector<int> preorderTraversal(TreeNode* root) {
        preorder(root);
        return res;
    }

private:
    void preorder(TreeNode* node) {
        if (!node) {
            return;
        }
        res.push_back(node->val);
        preorder(node->left);
        preorder(node->right);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(n)$ space for the recursion stack.
    - $O(n)$ space for the output array.

## 2. Iterative Depth First Search ▶ video

Preorder traversal follows the pattern:

**Visit Node → Left → Right**

Using a stack, we can simulate recursion.  
The trick:

- Whenever we visit a node, we immediately record its value (preorder rule).
- Then we push the **right child first**, because the stack is LIFO and we want to process the left child next.
- Move to the left child and repeat.
- If we reach a null left child, pop from the stack to continue with the right subtree.

This preserves the exact preorder sequence without recursion.

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
    vector<int> preorderTraversal(TreeNode* root) {
        vector<int> res;
        stack<TreeNode*> stack;
        TreeNode* cur = root;

        while (cur || !stack.empty()) {
            if (cur) {
                res.push_back(cur->val);
                stack.push(cur->right);
                cur = cur->left;
            } else {
                cur = stack.top();
                stack.pop();
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(n)$ space for the stack.
    - $O(n)$ space for the output array.

## 3. Morris Traversal

Morris Traversal lets us do preorder traversal **without recursion and without a stack**, using **O(1) extra space**.

The key idea:

- For every node with a left child, find its **inorder predecessor** (rightmost node in the left subtree).
- Normally, after finishing the left subtree, we would return back to the root.  
  Since we have no stack, we temporarily **create a thread**:  
  `predecessor.right = current`
- On the first time we reach a node, we **record its value** (because preorder = Node → Left → Right).
- When we come back through the created thread, we **restore the tree** by removing the thread and then continue to the right child.

This modifies the tree temporarily but restores it fully at the end.

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
    vector<int> preorderTraversal(TreeNode* root) {
        vector<int> res;
        TreeNode* cur = root;

        while (cur) {
            if (!cur->left) {
                res.push_back(cur->val);
                cur = cur->right;
            } else {
                TreeNode* prev = cur->left;
                while (prev->right && prev->right != cur) {
                    prev = prev->right;
                }

                if (!prev->right) {
                    res.push_back(cur->val);
                    prev->right = cur;
                    cur = cur->left;
                } else {
                    prev->right = nullptr;
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
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output array.

## Standalone solution file (`cpp/0144-binary-tree-preorder-traversal.cpp` in the NeetCode repo)

```cpp
/*
  Given the root of a binary tree, return the preorder traversal of its nodes' values.

  Ex. Input: root = [1,null,2,3]
      Output: [1,2,3]

  Time  : O(N)
  Space : O(H) -> H = Height of the binary tree
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
    vector <int> res;

    vector<int> preorderTraversal(TreeNode* root) {
        if(root != NULL) {
            res.push_back(root -> val);
            preorderTraversal(root -> left);
            preorderTraversal(root -> right);
        }
        return res;
    }
};
```
