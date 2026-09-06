# 173. Binary Search Tree Iterator

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/binary-search-tree-iterator/>  
- **NeetCode:** <https://neetcode.io/problems/binary-search-tree-iterator>  
- **Video:** <https://www.youtube.com/watch?v=RXy5RzGF5wo>  

[← Back to index](../INDEX.md)

## 1. Flattening the BST (DFS)

The simplest approach is to perform an inorder traversal of the BST upfront and store all values in an array. Since inorder traversal of a BST visits nodes in ascending order, the array will be sorted. Then, `next()` simply returns the next element from the array, and `hasNext()` checks if there are more elements remaining.

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
class BSTIterator {
private:
    vector<int> arr;
    int itr;

    void dfs(TreeNode* node) {
        if (!node) {
            return;
        }
        dfs(node->left);
        arr.push_back(node->val);
        dfs(node->right);
    }

public:
    BSTIterator(TreeNode* root) {
        itr = 0;
        dfs(root);
    }

    int next() {
        return arr[itr++];
    }

    bool hasNext() {
        return itr < arr.size();
    }
};
```

**Complexity**

- Time complexity:
    - $O(n)$ time for initialization.
    - $O(1)$ time for each $next()$ and $hasNext()$ function call.
- Space complexity: $O(n)$

## 2. Flatten the BST (Iterative DFS)

This is the same approach as the recursive version, but implemented iteratively using an explicit stack. We simulate the recursion by pushing nodes onto the stack, going left as far as possible, then processing nodes and going right. The result is the same sorted array of values.

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
class BSTIterator {
private:
    vector<int> arr;
    int itr;

public:
    BSTIterator(TreeNode* root) {
        itr = 0;
        stack<TreeNode*> stack;
        while (root || !stack.empty()) {
            while (root) {
                stack.push(root);
                root = root->left;
            }
            root = stack.top();
            stack.pop();
            arr.push_back(root->val);
            root = root->right;
        }
    }

    int next() {
        return arr[itr++];
    }

    bool hasNext() {
        return itr < arr.size();
    }
};
```

**Complexity**

- Time complexity:
    - $O(n)$ time for initialization.
    - $O(1)$ time for each $next()$ and $hasNext()$ function call.
- Space complexity: $O(n)$

## 3. Iterative DFS - I

Instead of flattening the entire tree upfront, we can save memory by only keeping track of the path from the root to the current position. We initialize the stack with all nodes along the leftmost path. When `next()` is called, we pop the top node, and if it has a right child, we push all nodes along the leftmost path of the right subtree. This way, the stack always contains the ancestors needed to continue the traversal.

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
class BSTIterator {
private:
    stack<TreeNode*> stack;

public:
    BSTIterator(TreeNode* root) {
        while (root) {
            stack.push(root);
            root = root->left;
        }
    }

    int next() {
        TreeNode* res = stack.top();
        stack.pop();
        TreeNode* cur = res->right;
        while (cur) {
            stack.push(cur);
            cur = cur->left;
        }
        return res->val;
    }

    bool hasNext() {
        return !stack.empty();
    }
};
```

**Complexity**

- Time complexity: $O(1)$ in average for each function call.
- Space complexity: $O(h)$

> Where $n$ is the number of nodes and $h$ is the height of the given tree.

## 4. Iterative DFS - II

This is a slight variation of the previous approach. Instead of initializing the stack in the constructor, we defer the leftward traversal to the `next()` method. We keep a pointer to the current node and only push nodes onto the stack when `next()` is called. This makes the constructor `O(1)` but the logic is essentially the same.

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
class BSTIterator {
private:
    TreeNode* cur;
    stack<TreeNode*> stack;

public:
    BSTIterator(TreeNode* root) {
        cur = root;
    }

    int next() {
        while (cur) {
            stack.push(cur);
            cur = cur->left;
        }

        TreeNode* node = stack.top();
        stack.pop();
        cur = node->right;
        return node->val;
    }

    bool hasNext() {
        return cur || !stack.empty();
    }
};
```

**Complexity**

- Time complexity: $O(1)$ in average for each function call.
- Space complexity: $O(h)$

> Where $n$ is the number of nodes and $h$ is the height of the given tree.
