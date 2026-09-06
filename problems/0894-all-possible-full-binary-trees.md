# 894. All Possible Full Binary Trees

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/all-possible-full-binary-trees/>  
- **NeetCode:** <https://neetcode.io/problems/all-possible-full-binary-trees>  
- **Video:** <https://www.youtube.com/watch?v=nZtrZPTTCAo>  

[← Back to index](../INDEX.md)

## 1. Recursion

A full binary tree has every node with either 0 or 2 children. If we have `n` nodes, one becomes the root, and we split the remaining `n-1` nodes between the left and right subtrees. Each subtree must also be a full binary tree.

We try all possible ways to distribute `n-1` nodes between left and right. For each valid split, we recursively generate all possible left subtrees and all possible right subtrees, then combine each left-right pair under a new root.

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
    vector<TreeNode*> allPossibleFBT(int n) {
        return backtrack(n);
    }

private:
    vector<TreeNode*> backtrack(int n) {
        if (n == 0) {
            return {};
        }
        if (n == 1) {
            return {new TreeNode(0)};
        }

        vector<TreeNode*> res;
        for (int l = 0; l < n; l++) {
            int r = n - 1 - l;
            vector<TreeNode*> leftTrees = backtrack(l);
            vector<TreeNode*> rightTrees = backtrack(r);

            for (auto& t1 : leftTrees) {
                for (auto& t2 : rightTrees) {
                    res.push_back(new TreeNode(0, t1, t2));
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n * 2 ^ n)$

## 2. Recursion (Optimal)

A full binary tree with `n` nodes only exists when `n` is odd. Every full binary tree has one root plus pairs of nodes in the subtrees, so the total must be odd. This lets us prune impossible cases immediately.

Additionally, we only need to try odd values for the `left` subtree size since each subtree must also form a valid full binary tree (requiring an odd count). This cuts the search space roughly in half.

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
    vector<TreeNode*> allPossibleFBT(int n) {
        if (n % 2 == 0) {
            return {};
        }
        if (n == 1) {
            return {new TreeNode(0)};
        }

        vector<TreeNode*> res;
        for (int left = 1; left < n; left += 2) {
            vector<TreeNode*> leftSubTree = allPossibleFBT(left);
            vector<TreeNode*> rightSubTree = allPossibleFBT(n - 1 - left);
            for (auto& l : leftSubTree) {
                for (auto& r : rightSubTree) {
                    TreeNode* root = new TreeNode(0, l, r);
                    res.push_back(root);
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n * 2 ^ n)$

## 3. Dynamic Programming (Top-Down)

The recursive solution recomputes the same subproblems multiple times. For example, when building trees of size 7, we compute trees of size 3 several times across different branches.

By caching results in a hash map or array, we ensure each subproblem is solved only once. The first time we compute all trees for a given `n`, we store them. Future calls simply return the cached `dp` result.

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
private:
    vector<vector<TreeNode*>> dp;

public:
    vector<TreeNode*> allPossibleFBT(int n) {
        dp.resize(n + 1);
        return dfs(n);
    }

    vector<TreeNode*> dfs(int n) {
        if (n % 2 == 0) {
            return {};
        }
        if (n == 1) {
            return {new TreeNode(0)};
        }
        if (!dp[n].empty()) {
            return dp[n];
        }

        vector<TreeNode*> res;
        for (int left = 1; left < n; left += 2) {
            vector<TreeNode*> leftSubTree = dfs(left);
            vector<TreeNode*> rightSubTree = dfs(n - 1 - left);
            for (auto& l : leftSubTree) {
                for (auto& r : rightSubTree) {
                    res.push_back(new TreeNode(0, l, r));
                }
            }
        }

        return dp[n] = res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n * 2 ^ n)$

## 4. Dynamic Programming (Bottom-Up)

Instead of recursing from `n` down and caching, we can build solutions bottom-up. We start with the base case (`n=1`), then iteratively compute solutions for `n=3, 5, 7, ...` up to the target.

For each odd value, we combine previously computed smaller trees to form larger ones. Since we only ever need results for smaller odd numbers, and we compute them in order, all dependencies are satisfied when we need them.

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
    vector<TreeNode*> allPossibleFBT(int n) {
        if (n % 2 == 0) {
            return {};
        }

        vector<vector<TreeNode*>> dp(n + 1);
        dp[1].push_back(new TreeNode(0));

        for (int nodes = 3; nodes <= n; nodes += 2) {
            vector<TreeNode*> res;
            for (int left = 1; left < nodes; left += 2) {
                int right = nodes - 1 - left;
                for (auto& t1 : dp[left]) {
                    for (auto& t2 : dp[right]) {
                        res.push_back(new TreeNode(0, t1, t2));
                    }
                }
            }
            dp[nodes] = res;
        }

        return dp[n];
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n * 2 ^ n)$
