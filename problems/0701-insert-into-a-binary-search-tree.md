# 701. Insert into a Binary Search Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/insert-into-a-binary-search-tree/>  
- **NeetCode:** <https://neetcode.io/problems/insert-into-a-binary-search-tree>  
- **Video:** <https://www.youtube.com/watch?v=Cpg8f79luEA>  

[← Back to index](../INDEX.md)

## 1. Recursion

In a BST, every node's left subtree contains only values smaller than the node, and the right subtree contains only values larger. This property tells us exactly where to go when inserting: compare the value with the current node and recurse left or right accordingly.
We keep traversing until we hit a null position, which is exactly where the new node belongs. The recursion naturally handles this by returning a new node when we reach an empty spot.
The beauty of this approach is that we don't need to track parent nodes explicitly; the recursive call stack handles the linking automatically.

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
    TreeNode* insertIntoBST(TreeNode* root, int val) {
        if (!root) {
            return new TreeNode(val);
        }

        if (val > root->val) {
            root->right = insertIntoBST(root->right, val);
        } else {
            root->left = insertIntoBST(root->left, val);
        }

        return root;
    }
};
```

**Complexity**

- Time complexity: $O(h)$
- Space complexity: $O(h)$ for the recursion stack.

> Where $h$ is the height of the given binary search tree.

## 2. Iteration

The iterative approach follows the same logic as recursion but uses a loop instead of the call stack. We traverse down the tree, comparing values at each node to decide which direction to go.
When we find a null child in the direction we need to go, we've found the insertion point. We create the new node and attach it directly.
This approach uses O(1) extra space since we don't need the recursion stack, making it more memory-efficient for deep trees.

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
    TreeNode* insertIntoBST(TreeNode* root, int val) {
        if (!root) {
            return new TreeNode(val);
        }

        TreeNode* cur = root;
        while (true) {
            if (val > cur->val) {
                if (!cur->right) {
                    cur->right = new TreeNode(val);
                    return root;
                }
                cur = cur->right;
            } else {
                if (!cur->left) {
                    cur->left = new TreeNode(val);
                    return root;
                }
                cur = cur->left;
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(h)$
- Space complexity: $O(1)$ extra space.

> Where $h$ is the height of the given binary search tree.

## Standalone solution file (`cpp/0701-insert-into-a-binary-search-tree.cpp` in the NeetCode repo)

```cpp
/*
    You are given the root node of a binary search tree (BST) and a value to insert into the tree. 
    Return the root node of the BST after the insertion. It is guaranteed that the new value does not exist in the original BST.

    Notice that there may exist multiple valid ways for the insertion, as long as the tree remains a BST after insertion. 
    You can return any of them.

    Ex. Input: root = [4,2,7,1,3], val = 5
        Output: [4,2,7,1,3,5]

    Time  : O(N)
    Space : O(N)
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
    TreeNode * create(int val) {
        TreeNode *n = new TreeNode;
        n -> val = val;
        n -> left = n -> right = NULL;
        return n;
    }

    TreeNode* insertIntoBST(TreeNode* root, int val) {
        if(root == NULL) 
		    return create(val);

        else if(val > root -> val)
		    root -> right = insertIntoBST(root -> right, val); 
        else if(val < root -> val)
		    root -> left = insertIntoBST(root -> left, val);
	    return root;
    }
};
```
