# 105. Construct Binary Tree From Preorder And Inorder Traversal

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/>  
- **NeetCode:** <https://neetcode.io/problems/binary-tree-from-preorder-and-inorder-traversal>  
- **Video:** <https://www.youtube.com/watch?v=ihj4IQGZ2zc>  
- **Video approach:** 1. Depth First Search  

[← Back to index](../INDEX.md)

## 1. Depth First Search ▶ video

The first element of the `preorder` array is always the root. We can find this root's position in the `inorder` array, which divides `inorder` into left and right subtrees. Elements before the root in `inorder` belong to the left subtree, and elements after belong to the right subtree. The same split applies to `preorder`. We recursively build left and right subtrees using the corresponding portions of both arrays.

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
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        if (preorder.empty() || inorder.empty()) {
            return nullptr;
        }

        TreeNode* root = new TreeNode(preorder[0]);
        auto mid = find(inorder.begin(), inorder.end(), preorder[0]) - inorder.begin();
        vector<int> leftPre(preorder.begin() + 1, preorder.begin() + mid + 1);
        vector<int> rightPre(preorder.begin() + mid + 1, preorder.end());
        vector<int> leftIn(inorder.begin(), inorder.begin() + mid);
        vector<int> rightIn(inorder.begin() + mid + 1, inorder.end());
        root->left = buildTree(leftPre, leftIn);
        root->right = buildTree(rightPre, rightIn);
        return root;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Hash Map + Depth First Search

In the basic DFS approach, we search for the root's position in `inorder` using linear search, which takes O(n) time per node. By precomputing a hash map from values to their indices in `inorder`, we can find the root's position in O(1) time. We also avoid creating new arrays by passing indices that define the current subarray boundaries.

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
    int pre_idx = 0;
    unordered_map<int, int> indices;

    TreeNode* dfs(vector<int>& preorder, int l, int r) {
        if (l > r) return nullptr;
        int root_val = preorder[pre_idx++];
        TreeNode* root = new TreeNode(root_val);
        int mid = indices[root_val];
        root->left = dfs(preorder, l, mid - 1);
        root->right = dfs(preorder, mid + 1, r);
        return root;
    }

public:
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        for (int i = 0; i < inorder.size(); ++i) {
            indices[inorder[i]] = i;
        }
        return dfs(preorder, 0, inorder.size() - 1);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Depth First Search (Optimal)

We can avoid the hash map entirely by using a limit-based approach. Instead of explicitly finding the root's position, we pass a "limit" value that tells us when to stop building the left subtree. When we encounter the limit value in `inorder`, we know the left subtree is complete. The `preorder` index tells us which node to create next, and the `inorder` index tells us when we have finished a subtree.

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
    int preIdx = 0;
    int inIdx = 0;

    TreeNode* dfs(vector<int>& preorder, vector<int>& inorder, int limit) {
        if (preIdx >= preorder.size()) return nullptr;
        if (inorder[inIdx] == limit) {
            inIdx++;
            return nullptr;
        }

        TreeNode* root = new TreeNode(preorder[preIdx++]);
        root->left = dfs(preorder, inorder, root->val);
        root->right = dfs(preorder, inorder, limit);
        return root;
    }

public:
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        return dfs(preorder, inorder, INT_MAX);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 4. Morris Traversal

Morris traversal allows us to build the tree iteratively without using a recursion stack. The idea is to use the right pointers of nodes to temporarily store parent references, simulating the call stack. We build nodes as we iterate through `preorder`, connecting them via left/right pointers. When we finish a left subtree (detected by matching the `inorder` sequence), we restore the original structure by clearing temporary links and moving up the tree.

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
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        TreeNode* head = new TreeNode(0);
        TreeNode* curr = head;
        int i = 0, j = 0, n = preorder.size();

        while (i < n && j < n) {
            curr->right = new TreeNode(preorder[i], nullptr, curr->right);
            curr = curr->right;
            i++;
            while (i < n && curr->val != inorder[j]) {
                curr->left = new TreeNode(preorder[i], nullptr, curr);
                curr = curr->left;
                i++;
            }
            j++;
            while (curr->right && j < n && curr->right->val == inorder[j]) {
                TreeNode* prev = curr->right;
                curr->right = nullptr;
                curr = prev;
                j++;
            }
        }
        return head->right;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ for the output tree.

## Standalone solution file (`cpp/0105-construct-binary-tree-from-preorder-and-inorder-traversal.cpp` in the NeetCode repo)

```cpp
/*
    Given 2 integer arrays preorder & inorder, construct & return the binary tree
    Ex. preorder = [3,9,20,15,7], inorder = [9,3,15,20,7] -> [3,9,20,null,null,15,7]

    Preorder dictates nodes, inorder dictates subtrees (preorder values, inorder positions)

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
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        int index = 0;
        return build(preorder, inorder, index, 0, inorder.size() - 1);
    }
private:
    TreeNode* build(vector<int>& preorder, vector<int>& inorder, int& index, int i, int j) {
        if (i > j) {
            return NULL;
        }
        
        TreeNode* root = new TreeNode(preorder[index]);
        
        int split = 0;
        for (int i = 0; i < inorder.size(); i++) {
            if (preorder[index] == inorder[i]) {
                split = i;
                break;
            }
        }
        index++;
        
        root->left = build(preorder, inorder, index, i, split - 1);
        root->right = build(preorder, inorder, index, split + 1, j);
        
        return root;
    }
};
```
