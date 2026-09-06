# 108. Convert Sorted Array to Binary Search Tree

- **Difficulty:** Easy  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/>  
- **NeetCode:** <https://neetcode.io/problems/convert-sorted-array-to-binary-search-tree>  
- **Video:** <https://www.youtube.com/watch?v=0K0uCMYq5ng>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

To create a height-balanced BST from a sorted array, we need to ensure that for every node, the left and right subtrees have roughly equal heights. Since the array is sorted, the middle element should become the root. All elements before the middle go to the left subtree, and all elements after go to the right subtree. Applying this recursively builds a balanced tree.

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
    TreeNode* sortedArrayToBST(vector<int>& nums) {
        if (nums.empty()) {
            return nullptr;
        }

        int mid = nums.size() / 2;
        TreeNode* root = new TreeNode(nums[mid]);
        vector<int> left(nums.begin(), nums.begin() + mid);
        vector<int> right(nums.begin() + mid + 1, nums.end());
        root->left = sortedArrayToBST(left);
        root->right = sortedArrayToBST(right);
        return root;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Depth First Search (Optimal)

The previous approach creates new array copies for each recursive call, which is inefficient. Instead, we can pass indices (left and right boundaries) to indicate the current segment of the array. This avoids array slicing and reduces both time and space overhead while maintaining the same logic of choosing the middle element as root.

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
    TreeNode* sortedArrayToBST(vector<int>& nums) {
        return helper(nums, 0, nums.size() - 1);
    }

private:
    TreeNode* helper(vector<int>& nums, int l, int r) {
        if (l > r) {
            return nullptr;
        }
        int m = (l + r) / 2;
        TreeNode* root = new TreeNode(nums[m]);
        root->left = helper(nums, l, m - 1);
        root->right = helper(nums, m + 1, r);
        return root;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(\log n)$ space for recursion stack.
    - $O(n)$ space for the output.

## 3. Iterative DFS

The recursive approach can be converted to an iterative one using an explicit stack. We store pending work items on the stack, where each item contains a node to be filled and the array bounds it should use. This simulates the recursive call stack and processes each subtree systematically without recursion.

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
    TreeNode* sortedArrayToBST(vector<int>& nums) {
        if (nums.empty()) return nullptr;

        TreeNode* root = new TreeNode(0);
        stack<tuple<TreeNode*, int, int>> stack;
        stack.push({root, 0, (int)nums.size() - 1});

        while (!stack.empty()) {
            auto [node, l, r] = stack.top();
            stack.pop();
            int m = (l + r) / 2;
            node->val = nums[m];

            if (l <= m - 1) {
                node->left = new TreeNode(0);
                stack.push({node->left, l, m - 1});
            }
            if (m + 1 <= r) {
                node->right = new TreeNode(0);
                stack.push({node->right, m + 1, r});
            }
        }

        return root;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(\log n)$ space for the stack.
    - $O(n)$ space for the output.
