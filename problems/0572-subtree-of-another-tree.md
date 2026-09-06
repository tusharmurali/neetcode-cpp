# 572. Subtree of Another Tree

- **Difficulty:** Easy  
- **Pattern:** Trees  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/subtree-of-another-tree/>  
- **NeetCode:** <https://neetcode.io/problems/subtree-of-a-binary-tree>  
- **Video:** <https://www.youtube.com/watch?v=E36O5SWp-LE>  
- **Video approach:** 1. Depth First Search (DFS)  

[← Back to index](../INDEX.md)

## 1. Depth First Search (DFS) ▶ video

To check whether one tree is a subtree of another, we do two things:

1. **Walk through every node** of the main tree (`root`) using DFS.
2. At each node, **check if the subtree starting here is exactly the same** as `subRoot`.

So for every node in the big tree:

- If its value matches `subRoot`'s root, we compare both subtrees fully.
- If they are identical, `subRoot` is a subtree.
- Otherwise, continue searching on the left and right children.

The helper `sameTree` simply checks whether two trees match **exactly**, node-for-node.

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
    bool isSubtree(TreeNode* root, TreeNode* subRoot) {
        if (!subRoot) {
            return true;
        }
        if (!root) {
            return false;
        }

        if (sameTree(root, subRoot)) {
            return true;
        }
        return isSubtree(root->left, subRoot) ||
               isSubtree(root->right, subRoot);
    }

    bool sameTree(TreeNode* root, TreeNode* subRoot) {
        if (!root && !subRoot) {
            return true;
        }
        if (root && subRoot && root->val == subRoot->val) {
            return sameTree(root->left, subRoot->left) &&
                   sameTree(root->right, subRoot->right);
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m + n)$

> Where $m$ is the number of nodes in $subRoot$ and $n$ is the number of nodes in $root$.

## 2. Serialization And Pattern Matching

Instead of comparing trees directly, we can first turn each tree into a **string** and then just check whether one string is contained in the other.

1. **Serialize** both `root` and `subRoot` into strings using the same traversal (for example, preorder).
2. While serializing, we **must include markers for `null` children** (like `#`) and separators (like `$`) so different shapes don't accidentally look the same in the string.
3. Once we have:
    - `S_root` = serialization of the main tree
    - `S_sub` = serialization of the subtree
      the problem becomes:
      **"Is `S_sub` a substring of `S_root`?"**

To efficiently check this, we can use a linear-time pattern matching algorithm (like **Z-function** or **KMP**) instead of naive substring search.

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
    string serialize(TreeNode* root) {
        string res;
        serialize(root, res);
        return res;
    }

    void serialize(TreeNode* root, string& res) {
        if (root == nullptr) {
            res += "$#";
            return;
        }

        res += "$";
        res += to_string(root->val);
        serialize(root->left, res);
        serialize(root->right, res);
    }

    vector<int> z_function(string s) {
        vector<int> z(s.length());
        int l = 0, r = 0, n = s.length();
        for (int i = 1; i < n; i++) {
            if (i <= r) {
                z[i] = min(r - i + 1, z[i - l]);
            }
            while (i + z[i] < n && s[z[i]] == s[i + z[i]]) {
                z[i]++;
            }
            if (i + z[i] - 1 > r) {
                l = i;
                r = i + z[i] - 1;
            }
        }
        return z;
    }

    bool isSubtree(TreeNode* root, TreeNode* subRoot) {
        string serialized_root = serialize(root);
        string serialized_subRoot = serialize(subRoot);
        string combined = serialized_subRoot + "|" + serialized_root;

        vector<int> z_values = z_function(combined);
        int sub_len = serialized_subRoot.length();

        for (int i = sub_len + 1; i < combined.length(); i++) {
            if (z_values[i] == sub_len) {
                return true;
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity: $O(m + n)$

> Where $m$ is the number of nodes in $subRoot$ and $n$ is the number of nodes in $root$.

## Standalone solution file (`cpp/0572-subtree-of-another-tree.cpp` in the NeetCode repo)

```cpp
/*
    Given the roots of 2 binary trees, return true if a tree has a subtree of the other tree

    Check at each node of the root tree if it's the same as the subRoot tree (structure + values)

    Time: O(m x n)
    Space: O(m)
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
    bool isSubtree(TreeNode* root, TreeNode* subRoot) {
        if (root == NULL) {
            return false;
        }
        if (isSame(root, subRoot)) {
            return true;
        }
        return isSubtree(root->left, subRoot) || isSubtree(root->right, subRoot);
    }
private:
    bool isSame(TreeNode* root, TreeNode* subRoot) {
        if (root == NULL && subRoot == NULL) {
            return true;
        }
        if (root == NULL || subRoot == NULL) {
            return false;
        }
        if (root->val != subRoot->val) {
            return false;
        }
        return isSame(root->left, subRoot->left) && isSame(root->right, subRoot->right);
    }
};
```
