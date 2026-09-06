# 270. Closest Binary Search Tree Value

- **Difficulty:** Easy  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/closest-binary-search-tree-value/>  
- **NeetCode:** <https://neetcode.io/problems/closest-binary-search-tree-value>  

[← Back to index](../INDEX.md)

## 1. Recursive Inorder + Linear search, O(N) time

An inorder traversal of a BST produces values in sorted order. By collecting all values first, we can then find the one closest to the target using a simple linear search. While not the most efficient approach, it clearly demonstrates the relationship between inorder traversal and sorted order.

```cpp
class Solution {
public:
    int closestValue(TreeNode* root, double target) {
        vector<int> nums;
        inorder(root, nums);
        return *min_element(nums.begin(), nums.end(), [&](int a, int b) {
            return abs(a - target) < abs(b - target);
        });
    }

    void inorder(TreeNode* root, vector<int>& nums) {
        if (!root) return;
        inorder(root->left, nums);
        nums.push_back(root->val);
        inorder(root->right, nums);
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(N)$

> Where $N$ is the total number of nodes in the binary tree

## 2. Iterative Inorder, O(k) time

Since inorder traversal gives sorted values, we can stop early once we find the first value greater than or equal to the target. At that point, the answer is either the current value or the previous value we visited (the predecessor). This avoids traversing the entire tree when the target is small.

```cpp
class Solution {
public:
    int closestValue(TreeNode* root, double target) {
        stack<TreeNode*> stk;
        long long pred = LLONG_MIN;

        while (!stk.empty() || root) {
            while (root) {
                stk.push(root);
                root = root->left;
            }
            root = stk.top();
            stk.pop();

            if (pred <= target && target < root->val) {
                return abs(pred - target) <= abs(root->val - target) ? pred : root->val;
            }

            pred = root->val;
            root = root->right;
        }
        return pred;
    }
};
```

**Complexity**

- Time complexity: $O(k)$ in the average case and $O(H+k)$ in the worst case,
- Space complexity: $O(H)$

> Where $k$ is an index of the closest element and $H$ is the height of the tree.

## 3. Binary Search, O(H) time

The BST property allows us to use binary search. At each node, we compare the target with the current value to decide whether to go left or right. We track the closest value seen so far. If the target is smaller, we go left (there might be a closer smaller value). If the target is larger, we go right (there might be a closer larger value). This approach only visits nodes along a single path from root to leaf.

```cpp
class Solution {
public:
    int closestValue(TreeNode* root, double target) {
        int val, closest = root->val;

        while (root != nullptr) {
            val = root->val;
            closest = abs(val - target) < abs(closest - target)
                || (abs(val - target) == abs(closest - target) && val < closest) ? val : closest;
            root = target < root->val ? root->left : root->right;
        }

        return closest;
    }
};
```

**Complexity**

- Time complexity: $O(H)$
- Space complexity: $O(1)$

> Where $H$ is the height of the tree.
