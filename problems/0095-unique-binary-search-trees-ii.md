# 95. Unique Binary Search Trees II

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/unique-binary-search-trees-ii/>  
- **NeetCode:** <https://neetcode.io/problems/unique-binary-search-trees-ii>  
- **Video:** <https://www.youtube.com/watch?v=m907FlQa2Yc>  

[← Back to index](../INDEX.md)

## 1. Recursion

To generate all unique BSTs with values from `1` to `n`, we pick each value as the root and recursively generate all possible left and right subtrees. When `val` is the root, values `1` to `val-1` form the left subtree and values `val+1` to `n` form the right subtree. We combine every `leftTree` with every `rightTree` to create all unique trees with that root.

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
    vector<TreeNode*> generateTrees(int n) {
        return generate(1, n);
    }

private:
    vector<TreeNode*> generate(int left, int right) {
        if (left > right) return {nullptr};

        vector<TreeNode*> res;
        for (int val = left; val <= right; val++) {
            vector<TreeNode*> leftTrees = generate(left, val - 1);
            vector<TreeNode*> rightTrees = generate(val + 1, right);

            for (auto& leftTree : leftTrees) {
                for (auto& rightTree : rightTrees) {
                    res.push_back(new TreeNode(val, leftTree, rightTree));
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(\frac {4 ^ n}{\sqrt {n}})$
- Space complexity:
    - $O(n)$ space for recursion stack.
    - $O(\frac {4 ^ n}{\sqrt {n}})$ space for the output.

## 2. Dynamic Programming (Top-Down)

The recursive solution recomputes the same ranges multiple times. For example, `generate(2, 4)` might be called from different parent recursions. We can cache results for each `(left, right)` pair to avoid regenerating the same subtrees.

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
    vector<vector<vector<TreeNode*>>> dp;

    vector<TreeNode*> generateTrees(int n) {
        dp.resize(n + 1, vector<vector<TreeNode*>>(n + 1));
        return generate(1, n);
    }

private:
    vector<TreeNode*> generate(int left, int right) {
        if (left > right) return {nullptr};
        if (!dp[left][right].empty()) return dp[left][right];

        vector<TreeNode*> res;
        for (int val = left; val <= right; val++) {
            for (auto& leftTree : generate(left, val - 1)) {
                for (auto& rightTree : generate(val + 1, right)) {
                    res.push_back(new TreeNode(val, leftTree, rightTree));
                }
            }
        }
        return dp[left][right] = res;
    }
};
```

**Complexity**

- Time complexity: $O(\frac {4 ^ n}{\sqrt {n}})$
- Space complexity:
    - $O(n)$ space for recursion stack.
    - $O(n ^ 2)$ extra space.
    - $O(\frac {4 ^ n}{\sqrt {n}})$ space for the output.

## 3. Dynamic Programming (Bottom-Up)

We can build the solution iteratively by computing all BSTs for smaller ranges first. We process ranges by increasing length: first all ranges of length 1, then length 2, and so on up to length `n`. This ensures that when we compute `dp[left][right]`, all smaller subproblems are already solved.

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
    vector<TreeNode*> generateTrees(int n) {
        vector<vector<vector<TreeNode*>>> dp(n + 2, vector<vector<TreeNode*>>(n + 2));
        for (int i = 1; i <= n + 1; i++) {
            dp[i][i - 1].push_back(nullptr);
        }

        for (int length = 1; length <= n; length++) {
            for (int left = 1; left + length - 1 <= n; left++) {
                int right = left + length - 1;

                for (int val = left; val <= right; val++) {
                    for (auto& leftTree : dp[left][val - 1]) {
                        for (auto& rightTree : dp[val + 1][right]) {
                            dp[left][right].push_back(new TreeNode(val, leftTree, rightTree));
                        }
                    }
                }
            }
        }
        return dp[1][n];
    }
};
```

**Complexity**

- Time complexity: $O(\frac {4 ^ n}{\sqrt {n}})$
- Space complexity:
    - $O(n ^ 2)$ extra space.
    - $O(\frac {4 ^ n}{\sqrt {n}})$ space for the output.

## 4. Dynamic Programming (Space Optimized)

The number of unique BST structures depends only on the count of nodes, not their actual values. We can generate all BST structures for sizes `0, 1, 2, ..., n` and then adjust node values using a `shift` function. For a tree structure with nodes `1` to `k`, we can create a tree with nodes `offset+1` to `offset+k` by adding `offset` to each node's value.

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
    vector<TreeNode*> generateTrees(int n) {
        vector<vector<TreeNode*>> dp(n + 1);
        dp[0].push_back(nullptr);

        for (int length = 1; length <= n; length++) {
            for (int val = 1; val <= length; val++) {
                for (auto& leftTree : dp[val - 1]) {
                    for (auto& rightTree : dp[length - val]) {
                        TreeNode* root = new TreeNode(val);
                        root->left = leftTree;
                        root->right = shift(rightTree, val);
                        dp[length].push_back(root);
                    }
                }
            }
        }
        return dp[n];
    }

private:
    TreeNode* shift(TreeNode* node, int offset) {
        if (!node) return nullptr;
        TreeNode* root = new TreeNode(node->val + offset);
        root->left = shift(node->left, offset);
        root->right = shift(node->right, offset);
        return root;
    }
};
```

**Complexity**

- Time complexity: $O(\frac {4 ^ n}{\sqrt {n}})$
- Space complexity:
    - $O(n)$ for the recursion stack.
    - $O(n)$ extra space.
    - $O(\frac {4 ^ n}{\sqrt {n}})$ space for the output.
