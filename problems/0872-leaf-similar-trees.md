# 872. Leaf-Similar Trees

- **Difficulty:** Easy  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/leaf-similar-trees/>  
- **NeetCode:** <https://neetcode.io/problems/leaf-similar-trees>  
- **Video:** <https://www.youtube.com/watch?v=Nr8dbnL0_cM>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

Two trees are leaf-similar if their leaf nodes, read from left to right, form the same sequence. We can collect the leaf values from each tree using a depth-first traversal. A node is a leaf if it has no children. By traversing left before right, we naturally encounter leaves in left-to-right order.

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
    bool leafSimilar(TreeNode* root1, TreeNode* root2) {
        vector<int> leaf1, leaf2;
        dfs(root1, leaf1);
        dfs(root2, leaf2);
        return leaf1 == leaf2;
    }

private:
    void dfs(TreeNode* root, vector<int>& leaf) {
        if (!root) return;
        if (!root->left && !root->right) {
            leaf.push_back(root->val);
            return;
        }
        dfs(root->left, leaf);
        dfs(root->right, leaf);
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$

> Where $n$ and $m$ are the number of nodes in the given trees.

## 2. Depth First Search (Space Optimized)

Instead of storing both leaf sequences and comparing at the end, we can collect leaves from the first tree and then verify them against the second tree on the fly. By traversing the second tree in reverse order (right to left) and using a stack, we can pop leaves one by one and compare them immediately. This saves space when one tree has significantly fewer leaves than expected.

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
    bool leafSimilar(TreeNode* root1, TreeNode* root2) {
        vector<int> leaf1;
        dfs(root1, leaf1);
        return dfs1(root2, leaf1) && leaf1.empty();
    }

private:
    void dfs(TreeNode* root, vector<int>& leaf) {
        if (!root) return;
        if (!root->left && !root->right) {
            leaf.push_back(root->val);
            return;
        }
        dfs(root->left, leaf);
        dfs(root->right, leaf);
    }

    bool dfs1(TreeNode* root, vector<int>& leaf) {
        if (!root) return true;
        if (!root->left && !root->right) {
            if (leaf.empty() || leaf.back() != root->val) {
                return false;
            }
            leaf.pop_back();
            return true;
        }
        return dfs1(root->right, leaf) && dfs1(root->left, leaf);
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$

> Where $n$ and $m$ are the number of nodes in the given trees.

## 3. Iterative DFS

Rather than collecting all leaves first, we can compare leaves one at a time using two parallel iterative traversals. Each tree maintains its own stack. We advance each stack until we find the next leaf, compare the two leaves, and continue. This approach can exit early if a mismatch is found without traversing the entire trees.

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
    bool leafSimilar(TreeNode* root1, TreeNode* root2) {
        stack<TreeNode*> stack1, stack2;
        stack1.push(root1);
        stack2.push(root2);

        while (!stack1.empty() && !stack2.empty()) {
            if (getPathLeaf(stack1) != getPathLeaf(stack2)) {
                return false;
            }
        }
        return stack1.empty() && stack2.empty();
    }

private:
    int getPathLeaf(stack<TreeNode*>& stack) {
        while (!stack.empty()) {
            TreeNode* node = stack.top();
            stack.pop();
            if (node->right) {
                stack.push(node->right);
            }
            if (node->left) {
                stack.push(node->left);
            }
            if (!node->left && !node->right) {
                return node->val;
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$

> Where $n$ and $m$ are the number of nodes in the given trees.
