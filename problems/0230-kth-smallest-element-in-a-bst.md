# 230. Kth Smallest Element In a Bst

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/kth-smallest-element-in-a-bst/>  
- **NeetCode:** <https://neetcode.io/problems/kth-smallest-integer-in-bst>  
- **Video:** <https://www.youtube.com/watch?v=5LUXSvjmGCw>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A Binary Search Tree (BST) has a special property:

- **Left subtree < root < right subtree**  
  But this brute-force method does **not** use the BST property.

We simply:

1. Traverse the entire tree and collect all node values.
2. Sort the collected values.
3. The k-th smallest element is at index `k-1` in the sorted list.

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
    int kthSmallest(TreeNode* root, int k) {
        vector<int> arr;
        dfs(root, arr);
        sort(arr.begin(), arr.end());
        return arr[k - 1];
    }

    void dfs(TreeNode* node, vector<int>& arr) {
        if (!node) return;
        arr.push_back(node->val);
        dfs(node->left, arr);
        dfs(node->right, arr);
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Inorder Traversal

A Binary Search Tree (BST) has an important property:

**Inorder Traversal (Left → Node → Right) always gives values in sorted order.**

So instead of collecting all values and sorting them manually, we can:

1. Do an inorder traversal.
2. This automatically produces values in ascending order.
3. The k-th element in this inorder list is the answer.

This makes the solution more efficient and uses the BST’s inherent structure.

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
    int kthSmallest(TreeNode* root, int k) {
        vector<int> arr;
        dfs(root, arr);
        return arr[k - 1];
    }

    void dfs(TreeNode* node, vector<int>& arr) {
        if (!node) return;
        dfs(node->left, arr);
        arr.push_back(node->val);
        dfs(node->right, arr);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Recursive DFS (Optimal)

In a BST, the **inorder traversal** (Left → Node → Right) naturally visits nodes in **sorted order**.

So instead of storing all values, we can:

- Traverse the tree in inorder,
- Count nodes as we visit them,
- Stop as soon as we visit the k-th smallest node.

This avoids storing all node values, and the early return lets us stop once the k-th smallest node is found.

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
    int kthSmallest(TreeNode* root, int k) {
        vector<int> tmp(2);
        tmp[0] = k;
        dfs(root, tmp);
        return tmp[1];
    }

    void dfs(TreeNode* node, vector<int>& tmp) {
        if (!node) return;

        dfs(node->left, tmp);
        if (tmp[0] == 0) return;

        tmp[0]--;
        if (tmp[0] == 0) {
            tmp[1] = node->val;
            return;
        }

        dfs(node->right, tmp);
    }
};
```

**Complexity**

- Time complexity: $O(h + k)$ in terms of nodes visited, worst-case $O(n)$
- Space complexity: $O(h)$ for the recursion stack, worst-case $O(n)$

## 4. Iterative DFS (Optimal)

In a BST, an **inorder traversal** (left -> node -> right) gives nodes in **sorted order**.
Instead of recursion, we simulate this traversal with a **stack**:

- Push all left nodes (go as deep as possible).
- Pop the top node - this is the next smallest value.
- Move to its right subtree and repeat.
- When we pop the k-th node, that's our answer.

This way, we only visit nodes until we reach the k-th smallest — no need to traverse the whole tree.

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
    int kthSmallest(TreeNode* root, int k) {
        stack<TreeNode*> stack;
        TreeNode* curr = root;

        while (!stack.empty() || curr != nullptr) {
            while (curr != nullptr) {
                stack.push(curr);
                curr = curr->left;
            }
            curr = stack.top();
            stack.pop();
            k--;
            if (k == 0) {
                return curr->val;
            }
            curr = curr->right;
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 5. Morris Traversal

Inorder traversal of a BST gives values in **sorted order**, so the k-th visited node is the k-th smallest.
But recursion and stacks use extra space.

**Morris Traversal** allows us to perform inorder traversal using **`O(1)` extra space**, by temporarily creating
a "thread" (a right pointer) from a node's predecessor back to the node.

For each node:

- If it has no left child - visit it directly.
- If it has a left child - find its inorder predecessor.
    - If the predecessor's right pointer is empty - create a temporary link to the current node and move left.
    - If the predecessor's right pointer already points to the current node - remove the link, visit the node, and move right.

We decrement `k` each time we "visit" a node.
The node where `k` becomes `0` is the **k-th smallest**.

This works because we simulate the inorder order without extra memory.

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
    int kthSmallest(TreeNode* root, int k) {
        TreeNode* curr = root;

        while (curr) {
            if (!curr->left) {
                k--;
                if (k == 0) return curr->val;
                curr = curr->right;
            } else {
                TreeNode* pred = curr->left;
                while (pred->right && pred->right != curr)
                    pred = pred->right;

                if (!pred->right) {
                    pred->right = curr;
                    curr = curr->left;
                } else {
                    pred->right = nullptr;
                    k--;
                    if (k == 0) return curr->val;
                    curr = curr->right;
                }
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0230-kth-smallest-element-in-a-bst.cpp` in the NeetCode repo)

```cpp
/*
    Given root of BST & int k, return kth smallest value (1-indexed) of all values in tree
    Ex. root = [3,1,4,null,2] k = 1 -> 1, root = [5,3,6,2,4,null,null,1] k = 3 -> 3

    Inorder traversal, each visit decrement k, when k = 0 return, works because inorder

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
    int kthSmallest(TreeNode* root, int k) {
        int result = 0;
        inorder(root, k, result);
        return result;
    }
private:
    void inorder(TreeNode* root, int& k, int& result) {
        if (root == NULL) {
            return;
        }
        inorder(root->left, k, result);
        k--;
        if (k == 0) {
            result = root->val;
            return;
        }
        inorder(root->right, k, result);
    }
};
```
