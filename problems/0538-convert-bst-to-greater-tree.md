# 538. Convert Bst to Greater Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/convert-bst-to-greater-tree/>  
- **NeetCode:** <https://neetcode.io/problems/convert-bst-to-greater-tree>  
- **Video:** <https://www.youtube.com/watch?v=7vVEJwVvAlI>  

[← Back to index](../INDEX.md)

## 1. Depth First Search (Two Pass)

For each node in a BST, the Greater Tree value should be the sum of all nodes with values greater than or equal to the current node. In a BST, all greater values are found in the right subtree and ancestors that are greater. A simple two-pass approach first calculates the total sum of all nodes, then traverses in-order (left to right). As we visit each node, we update its value to the remaining sum and subtract its original value from the total.

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
    int totalSum;

    TreeNode* convertBST(TreeNode* root) {
        totalSum = getSum(root);
        dfs(root);
        return root;
    }

private:
    int getSum(TreeNode* node) {
        if (!node) return 0;
        return node->val + getSum(node->left) + getSum(node->right);
    }

    void dfs(TreeNode* node) {
        if (!node) return;

        dfs(node->left);
        int tmp = node->val;
        node->val = totalSum;
        totalSum -= tmp;
        dfs(node->right);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Depth First Search (One Pass)

We can do this in a single pass by traversing the tree in reverse in-order (right, current, left). In a BST, this visits nodes from largest to smallest. We maintain a running sum of all nodes visited so far. When we visit a node, all previously visited nodes have greater values, so we add the current node's value to our running sum and update the node to this sum.

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
    int curSum = 0;

    TreeNode* convertBST(TreeNode* root) {
        dfs(root);
        return root;
    }

private:
    void dfs(TreeNode* node) {
        if (!node) return;

        dfs(node->right);
        int tmp = node->val;
        node->val += curSum;
        curSum += tmp;
        dfs(node->left);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 3. Iterative DFS

The recursive reverse in-order traversal can be converted to an iterative version using a stack. We simulate the call stack explicitly, pushing nodes as we traverse right, then processing them in order. This achieves the same result as the recursive one-pass solution but avoids recursion overhead and potential stack overflow for very deep trees.

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
    TreeNode* convertBST(TreeNode* root) {
        int curSum = 0;
        stack<TreeNode*> st;
        TreeNode* node = root;

        while (!st.empty() || node) {
            while (node) {
                st.push(node);
                node = node->right;
            }

            node = st.top(); st.pop();
            curSum += node->val;
            node->val = curSum;
            node = node->left;
        }
        return root;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Morris Traversal

Morris traversal allows us to traverse a tree without using extra space for a stack or recursion. It works by temporarily modifying the tree structure to create links back to ancestor nodes, then restoring the original structure. For this problem, we use reverse Morris in-order traversal to visit nodes from largest to smallest while maintaining only O(1) extra space.

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
    TreeNode* convertBST(TreeNode* root) {
        int curSum = 0;
        TreeNode* cur = root;

        while (cur) {
            if (cur->right) {
                TreeNode* prev = cur->right;
                while (prev->left && prev->left != cur) {
                    prev = prev->left;
                }

                if (!prev->left) {
                    prev->left = cur;
                    cur = cur->right;
                } else {
                    prev->left = nullptr;
                    curSum += cur->val;
                    cur->val = curSum;
                    cur = cur->left;
                }
            } else {
                curSum += cur->val;
                cur->val = curSum;
                cur = cur->left;
            }
        }
        return root;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0538-convert-bst-to-greater-tree.cpp` in the NeetCode repo)

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
    TreeNode* convertBST(TreeNode* root) {
        int currSum=0;
        reversed(root,currSum);
        return root;
    }

private:

    // just do a inorder treversal starting from right
    // maintain a current sum
    // change the root->val to the curr sum

    void reversed(TreeNode* root,int &currSum){
        if(root==NULL){
            return;
        }

        reversed(root->right,currSum);
        currSum+=root->val;
        root->val=currSum;
        reversed(root->left,currSum);
    }
};
```
