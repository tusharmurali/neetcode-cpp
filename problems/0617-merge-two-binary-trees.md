# 617. Merge Two Binary Trees

- **Difficulty:** Easy  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/merge-two-binary-trees/>  
- **NeetCode:** <https://neetcode.io/problems/merge-two-binary-trees>  
- **Video:** <https://www.youtube.com/watch?v=QHH6rIK3dDQ>  

[← Back to index](../INDEX.md)

## 1. Depth First Search (Creating New Tree)

To merge two trees, we traverse both trees simultaneously. At each position, if both trees have a node, we create a new node with the sum of their values. If only one tree has a node at a position, we use that node's value. We recursively build the left and right subtrees the same way. This approach creates an entirely new tree without modifying the inputs.

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
    TreeNode* mergeTrees(TreeNode* root1, TreeNode* root2) {
        if (!root1 && !root2) {
            return nullptr;
        }

        int v1 = root1 ? root1->val : 0;
        int v2 = root2 ? root2->val : 0;
        TreeNode* root = new TreeNode(v1 + v2);

        root->left = mergeTrees(root1 ? root1->left : nullptr, root2 ? root2->left : nullptr);
        root->right = mergeTrees(root1 ? root1->right : nullptr, root2 ? root2->right : nullptr);

        return root;
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity:
    - $O(m + n)$ space for recursion stack.
    - $O(m + n)$ space for the output.

> Where $m$ and $n$ are the number of nodes in the given trees.

## 2. Depth First Search (In Place)

Instead of creating new nodes, we can modify the first tree in place. If one tree is missing at a position, we simply return the other tree's subtree. If both exist, we add the second tree's value to the first tree's node and recursively merge the children. This saves memory by reusing existing nodes.

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
    TreeNode* mergeTrees(TreeNode* root1, TreeNode* root2) {
        if (!root1) return root2;
        if (!root2) return root1;

        root1->val += root2->val;
        root1->left = mergeTrees(root1->left, root2->left);
        root1->right = mergeTrees(root1->right, root2->right);
        return root1;
    }
};
```

**Complexity**

- Time complexity: $O(min(m, n))$
- Space complexity: $O(min(m, n))$ for recursion stack.

> Where $m$ and $n$ are the number of nodes in the given trees.

## 3. Iterative DFS (Creating New Tree)

We can avoid recursion by using an explicit stack to traverse both trees. We push triplets of (`node1`, `node2`, `merged_node`) onto the stack. For each triplet, we create children for the merged node based on whether the corresponding children exist in either input tree. This creates a new tree while simulating the recursive approach iteratively.

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
    TreeNode* mergeTrees(TreeNode* root1, TreeNode* root2) {
        if (!root1 && !root2) return nullptr;

        int val = (root1 ? root1->val : 0) + (root2 ? root2->val : 0);
        TreeNode* root = new TreeNode(val);
        stack<tuple<TreeNode*, TreeNode*, TreeNode*>> st;
        st.push({root1, root2, root});

        while (!st.empty()) {
            auto [node1, node2, node] = st.top();
            st.pop();

            TreeNode* left1 = node1 ? node1->left : nullptr;
            TreeNode* left2 = node2 ? node2->left : nullptr;
            if (left1 || left2) {
                int leftVal = (left1 ? left1->val : 0) + (left2 ? left2->val : 0);
                node->left = new TreeNode(leftVal);
                st.push({left1, left2, node->left});
            }

            TreeNode* right1 = node1 ? node1->right : nullptr;
            TreeNode* right2 = node2 ? node2->right : nullptr;
            if (right1 || right2) {
                int rightVal = (right1 ? right1->val : 0) + (right2 ? right2->val : 0);
                node->right = new TreeNode(rightVal);
                st.push({right1, right2, node->right});
            }
        }

        return root;
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity:
    - $O(m + n)$ space for the stack.
    - $O(m + n)$ space for the output.

> Where $m$ and $n$ are the number of nodes in the given trees.

## 4. Iterative DFS (In Place)

Similar to the recursive in-place approach, we can modify the first tree iteratively using a stack. We push pairs of nodes from both trees. When both nodes exist, we add values and continue processing children. If only one tree has a child at a position, we directly attach that subtree to the first tree. This avoids creating new nodes.

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
    TreeNode* mergeTrees(TreeNode* root1, TreeNode* root2) {
        if (!root1) return root2;
        if (!root2) return root1;

        stack<pair<TreeNode*, TreeNode*>> stk;
        stk.push({root1, root2});

        while (!stk.empty()) {
            auto [node1, node2] = stk.top();
            stk.pop();

            if (!node2) continue;

            node1->val += node2->val;

            if (!node1->left) {
                node1->left = node2->left;
            } else {
                stk.push({node1->left, node2->left});
            }

            if (!node1->right) {
                node1->right = node2->right;
            } else {
                stk.push({node1->right, node2->right});
            }
        }

        return root1;
    }
};
```

**Complexity**

- Time complexity: $O(min(m, n))$
- Space complexity: $O(min(m, n))$ for the stack.

> Where $m$ and $n$ are the number of nodes in the given trees.

## Standalone solution file (`cpp/0617-merge-two-binary-trees.cpp` in the NeetCode repo)

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
    TreeNode* mergeTrees(TreeNode* root1, TreeNode* root2) {
        if (root1 == NULL && root2 == NULL) 
            return NULL;
        if (root1 != NULL && root2 == NULL) 
            return root1;
        if (root1 == NULL && root2 != NULL) 
            return root2;
        if (root1 != NULL && root2 != NULL) 
            root1->val += root2->val;

        root1->left = mergeTrees(root1->left, root2->left);
        root1->right = mergeTrees(root1->right, root2->right);
        return root1;
    }
};
```
