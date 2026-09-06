# 1325. Delete Leaves With a Given Value

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/delete-leaves-with-a-given-value/>  
- **NeetCode:** <https://neetcode.io/problems/delete-leaves-with-a-given-value>  
- **Video:** <https://www.youtube.com/watch?v=FqAoYAwbwV8>  

[← Back to index](../INDEX.md)

## 1. Recursion (Postorder Traversal)

When we delete a leaf with the target value, its parent might become a new leaf. This means we need to process children before parents, which is exactly what postorder traversal does. By recursively processing left and right subtrees first, any newly exposed leaves are handled automatically when we return to the parent.

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
    TreeNode* removeLeafNodes(TreeNode* root, int target) {
        if (!root) {
            return nullptr;
        }

        root->left = removeLeafNodes(root->left, target);
        root->right = removeLeafNodes(root->right, target);

        if (!root->left && !root->right && root->val == target) {
            return nullptr;
        }

        return root;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Iterative Postorder Traversal

We can simulate postorder traversal using a stack and a set to track visited nodes. We also need to maintain parent pointers so that when we delete a leaf, we can update its parent's child reference. A node is processed only after both its children have been visited.

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
    TreeNode* removeLeafNodes(TreeNode* root, int target) {
        stack<TreeNode*> stack;
        unordered_set<TreeNode*> visit;
        unordered_map<TreeNode*, TreeNode*> parents;
        parents[root] = nullptr;
        stack.push(root);

        while (!stack.empty()) {
            TreeNode* node = stack.top();
            stack.pop();
            if (!node->left && !node->right) {
                if (node->val == target) {
                    TreeNode* p = parents[node];
                    if (!p) {
                        return nullptr;
                    }
                    if (p->left == node) {
                        p->left = nullptr;
                    }
                    if (p->right == node) {
                        p->right = nullptr;
                    }
                }
            } else if (visit.find(node) == visit.end()) {
                visit.insert(node);
                stack.push(node);
                if (node->left) {
                    stack.push(node->left);
                    parents[node->left] = node;
                }
                if (node->right) {
                    stack.push(node->right);
                    parents[node->right] = node;
                }
            }
        }

        return root;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Iterative Postorder Traversal (Optimal)

We can optimize the iterative approach by using a standard postorder traversal pattern without maintaining a separate parent map. The stack itself naturally tracks the parent: after processing a node, the next item on the stack is its parent. We use a `visited` pointer to avoid reprocessing the right subtree.

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
    TreeNode* removeLeafNodes(TreeNode* root, int target) {
        if (!root) return nullptr;

        stack<TreeNode*> stack;
        TreeNode* cur = root;
        TreeNode* visited = nullptr;

        while (!stack.empty() || cur) {
            while (cur) {
                stack.push(cur);
                cur = cur->left;
            }

            cur = stack.top();
            if (cur->right && cur->right != visited) {
                cur = cur->right;
                continue;
            }

            stack.pop();
            if (!cur->left && !cur->right && cur->val == target) {
                if (stack.empty()) return nullptr;

                TreeNode* parent = stack.top();
                if (parent->left == cur) {
                    parent->left = nullptr;
                } else if (parent->right == cur) {
                    parent->right = nullptr;
                }
            } else {
                visited = cur;
            }

            cur = nullptr;
        }

        return root;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
