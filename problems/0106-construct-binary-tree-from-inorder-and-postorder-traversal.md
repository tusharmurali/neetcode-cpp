# 106. Construct Binary Tree from Inorder and Postorder Traversal

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/>  
- **NeetCode:** <https://neetcode.io/problems/construct-binary-tree-from-inorder-and-postorder-traversal>  
- **Video:** <https://www.youtube.com/watch?v=vm63HuIU7kw>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

The last element of postorder is always the root. Once we identify the root, we find it in the inorder array. Everything to the left of the root in inorder belongs to the left subtree, and everything to the right belongs to the right subtree. We recursively apply this logic, slicing the arrays accordingly.

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
    TreeNode* buildTree(vector<int>& inorder, vector<int>& postorder) {
        if (postorder.empty() || inorder.empty()) {
            return nullptr;
        }

        TreeNode* root = new TreeNode(postorder.back());
        auto it = find(inorder.begin(), inorder.end(), postorder.back());
        int mid = distance(inorder.begin(), it);

        vector<int> leftInorder(inorder.begin(), inorder.begin() + mid);
        vector<int> rightInorder(inorder.begin() + mid + 1, inorder.end());
        vector<int> leftPostorder(postorder.begin(), postorder.begin() + mid);
        vector<int> rightPostorder(postorder.begin() + mid, postorder.end() - 1);

        root->left = buildTree(leftInorder, leftPostorder);
        root->right = buildTree(rightInorder, rightPostorder);

        return root;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Hash Map + Depth First Search

The previous approach has O(n) lookup time when finding the root in `inorder`. By precomputing a hash map that stores each value's index in `inorder`, we achieve O(1) lookups. We also avoid creating new arrays by using index boundaries instead.

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
    unordered_map<int, int> inorderIdx;
    int postIdx;

    TreeNode* buildTree(vector<int>& inorder, vector<int>& postorder) {
        for (int i = 0; i < inorder.size(); i++) {
            inorderIdx[inorder[i]] = i;
        }
        postIdx = postorder.size() - 1;

        return dfs(0, inorder.size() - 1, postorder);
    }

private:
    TreeNode* dfs(int l, int r, vector<int>& postorder) {
        if (l > r) {
            return nullptr;
        }

        TreeNode* root = new TreeNode(postorder[postIdx--]);
        int idx = inorderIdx[root->val];
        root->right = dfs(idx + 1, r, postorder);
        root->left = dfs(l, idx - 1, postorder);
        return root;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Depth First Search (Optimal)

We can eliminate the hash map by using a boundary-based approach. Instead of explicitly finding the root's position, we pass a "limit" value that tells us when to stop building the current subtree. When we encounter the limit in `inorder`, we know the current subtree is complete. This approach processes both arrays from right to left.

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
    int postIdx;
    int inIdx;

    TreeNode* buildTree(vector<int>& inorder, vector<int>& postorder) {
        postIdx = postorder.size() - 1;
        inIdx = inorder.size() - 1;

        return dfs(postorder, inorder, numeric_limits<int>::max());
    }

private:
    TreeNode* dfs(vector<int>& postorder, vector<int>& inorder, int limit) {
        if (postIdx < 0) {
            return nullptr;
        }

        if (inorder[inIdx] == limit) {
            inIdx--;
            return nullptr;
        }

        TreeNode* root = new TreeNode(postorder[postIdx--]);
        root->right = dfs(postorder, inorder, root->val);
        root->left = dfs(postorder, inorder, limit);
        return root;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.
