# 333. Largest BST Subtree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/largest-bst-subtree/>  
- **NeetCode:** <https://neetcode.io/problems/largest-bst-subtree>  

[← Back to index](../INDEX.md)

## 1. Pre-Order Traversal

The most direct approach is to check every subtree: if a subtree is a valid BST, count its nodes. To verify the BST property, we need to ensure that every node in the left subtree is smaller than the current node, and every node in the right subtree is larger. We do this by finding the maximum value in the left subtree and the minimum value in the right subtree, then comparing them against the current node.

```cpp
class Solution {
public:
    // Function to check if given tree is a valid Binary Search Tree or not.
    bool isValidBST(TreeNode* root) {
        // An empty tree is a valid Binary Search Tree.
        if (!root) {
            return true;
        }

        // Find the max node in the left subtree of current node.
        int leftMax = findMax(root->left);

        // If the left subtree has a node greater than or equal to the current node,
        // then it is not a valid Binary Search Tree.
        if (leftMax >= root->val) {
            return false;
        }

        // Find the min node in the right subtree of current node.
        int rightMin = findMin(root->right);

        // If the right subtree has a value less than or equal to the current node,
        // then it is not a valid Binary Search Tree.
        if (rightMin <= root->val) {
            return false;
        }

        // If the left and right subtrees of current tree are also valid BST.
        // then the whole tree is a BST.
        if (isValidBST(root->left) && isValidBST(root->right)) {
            return true;
        }

        return false;
    }

    int findMax(TreeNode* root) {
        // Max node in a empty tree should be smaller than parent.
        if (!root) {
            return INT_MIN;
        }

        // Check the maximum node from the current node, left and right subtree of the current tree
        return max({ root->val, findMax(root->left), findMax(root->right) });
    }

    int findMin(TreeNode* root) {
        // Min node in a empty tree should be larger than parent.
        if (!root) {
            return INT_MAX;
        }

        // Check the minimum node from the current node, left and right subtree of the current tree
        return min({ root->val, findMin(root->left), findMin(root->right) });
    }

    int countNodes(TreeNode* root) {
        // Empty tree has 0 nodes.
        if (!root) {
            return 0;
        }

        // Add nodes in left and right subtree.
        // Add 1 and return total size.
        return 1 + countNodes(root->left) + countNodes(root->right);
    }

    int largestBSTSubtree(TreeNode* root) {
        if (!root) {
            return 0;
        }

        // If current subtree is a validBST, its children will have smaller size BST.
        if (isValidBST(root)) {
            return countNodes(root);
        }

        // Find BST in left and right subtrees of current nodes.
        return max(largestBSTSubtree(root->right), largestBSTSubtree(root->left));
    }
};
```

**Complexity**

- Time complexity: $O(N^3)$
- Space complexity: $O(N)$
    - The recursion call stack can take at most $O(H)$ space; in the worst-case scenario, the height of the tree will equal $N$.

> Where $N$ and $H$ are the number of nodes and the max height of the given tree respectively

## 2. Pre-Order Traversal Optimized

Instead of finding the min/max of entire subtrees, we can validate the BST using in-order traversal. In a valid BST, an in-order traversal visits nodes in strictly increasing order. By tracking the previously visited node during the traversal, we can verify the BST property in a single pass through each subtree, which reduces redundant work.

```cpp
class Solution {
public:
    // Track previous node while doing inorder traversal.
    TreeNode* previous = NULL;

    // Function to check if given tree is a valid Binary Search Tree or not.
    bool isValidBST(TreeNode* root) {
        // An empty tree is a valid Binary Search Tree.
        if (!root) {
            return true;
        }

        // If left subtree is not a valid BST return false.
        if(!isValidBST(root->left)) {
            return false;
        }

        // If current node's value is not greater than the previous
        // node's value in the in-order traversal return false.
        if (previous && previous->val >= root->val) {
            return false;
        }

        // Update previous node to current node.
        previous = root;

        // If right subtree is not a valid BST return false.
        return isValidBST(root->right);
    }

    int countNodes(TreeNode* root) {
        if (!root) {
            return 0;
        }

        // Add nodes in left and right subtree.
        // Add 1 and return total size.
        return 1 + countNodes(root->left) + countNodes(root->right);
    }

    int largestBSTSubtree(TreeNode* root) {
        if (!root) {
            return 0;
        }

        // Set previous node to NULL initially.
        previous = NULL;

        // If current subtree is a validBST, its children will have smaller size BST.
        if (isValidBST(root)) {
            return countNodes(root);
        }

        // Find BST in left and right subtrees of current nodes.
        return max(largestBSTSubtree(root->left), largestBSTSubtree(root->right));
    }
};
```

**Complexity**

- Time complexity: $O(N^2)$
- Space complexity: $O(N)$
    - The recursion call stack can take at most $O(H)$ space; in the worst-case scenario, the height of the tree will equal $N$.

> Where $N$ and $H$ are the number of nodes and the max height of the given tree respectively

## 3. Post-Order Traversal

The key insight is that we can determine if a subtree is a valid BST by looking at information from its children. If we process nodes bottom-up (post-order), each node can inherit the min/max values and sizes from its children. A node forms a valid BST if the maximum value in its left subtree is less than the node, and the minimum value in its right subtree is greater than the node. By returning both the valid range and size from each recursive call, we avoid redundant traversals.

```cpp
// Each node will return min node value, max node value, max size
class NodeValue {
public:
    int maxNode, minNode, maxSize;

    NodeValue(int minNode, int maxNode, int maxSize) {
        this->maxNode = maxNode;
        this->minNode = minNode;
        this->maxSize = maxSize;
    }
};

class Solution {
public:
    NodeValue largestBSTSubtreeHelper(TreeNode* root) {
        // An empty tree is a BST of size 0.
        if (!root) {
            return NodeValue(INT_MAX, INT_MIN, 0);
        }

        // Get values from left and right subtree of current tree.
        auto left = largestBSTSubtreeHelper(root->left);
        auto right = largestBSTSubtreeHelper(root->right);

        // Current node is greater than max in left AND smaller than min in right, it is a BST.
        if (left.maxNode < root->val && root->val < right.minNode) {
            // It is a BST.
            return NodeValue(min(root->val, left.minNode), max(root->val, right.maxNode),
                            left.maxSize + right.maxSize + 1);
        }

        // Otherwise, return [-inf, inf] so that parent can't be valid BST
        return NodeValue(INT_MIN, INT_MAX, max(left.maxSize, right.maxSize));
    }

    int largestBSTSubtree(TreeNode* root) {
        return largestBSTSubtreeHelper(root).maxSize;
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(N)$
    - The recursion call stack can take at most $O(H)$ space; in the worst-case scenario, the height of the tree will equal $N$.

> Where $N$ and $H$ are the number of nodes and the max height of the given tree respectively
