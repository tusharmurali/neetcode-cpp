# 104. Maximum Depth of Binary Tree

- **Difficulty:** Easy  
- **Pattern:** Trees  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/maximum-depth-of-binary-tree/>  
- **NeetCode:** <https://neetcode.io/problems/depth-of-binary-tree>  
- **Video:** <https://www.youtube.com/watch?v=hTM3phVI6YQ>  

[← Back to index](../INDEX.md)

## 1. Recursive DFS

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
    int maxDepth(TreeNode* root) {
        if (root == nullptr) {
            return 0;
        }

        return 1 + max(maxDepth(root->left), maxDepth(root->right));
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(h)$
    - Best Case ([balanced tree](https://www.geeksforgeeks.org/balanced-binary-tree/)): $O(log(n))$
    - Worst Case ([degenerate tree](https://www.geeksforgeeks.org/introduction-to-degenerate-binary-tree/)): $O(n)$

> Where $n$ is the number of nodes in the tree and $h$ is the height of the tree.

## 2. Iterative DFS (Stack)

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
    int maxDepth(TreeNode* root) {
        stack<pair<TreeNode*, int>> stack;
        stack.push({root, 1});
        int res = 0;

        while (!stack.empty()) {
            pair<TreeNode*, int> current = stack.top();
            stack.pop();
            TreeNode* node = current.first;
            int depth = current.second;

            if (node != nullptr) {
                res = max(res, depth);
                stack.push({node->left, depth + 1});
                stack.push({node->right, depth + 1});
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Breadth First Search

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
    int maxDepth(TreeNode* root) {
        queue<TreeNode*> q;
        if (root != nullptr) {
            q.push(root);
        }

        int level = 0;
        while (!q.empty()) {
            int size = q.size();
            for (int i = 0; i < size; i++) {
                TreeNode* node = q.front();
                q.pop();
                if (node->left != nullptr) {
                    q.push(node->left);
                }
                if (node->right != nullptr) {
                    q.push(node->right);
                }
            }
            level++;
        }
        return level;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0104-maximum-depth-of-binary-tree.cpp` in the NeetCode repo)

```cpp
/*
    Given root of binary tree, return max depth (# nodes along longest path from root to leaf)

    At every node, max depth is the max depth between its left & right children + 1

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
    int maxDepth(TreeNode* root) {
        // return maxDepthRecur(root);          // recursive DFS - preorder - easiest    
        // return maxDepthStkInorder(root);     // iterative DFS - inorder 
        return maxDepthStkPreorder(root);    // iterative DFS - preorder - easier
        // return maxDepthQueueLevelorder(root);   // iterative BFS - levelorder - easy
    }

    int maxDepthQueueLevelorder(TreeNode* root) {
        if (root == NULL) return 0;

        queue<TreeNode*> q;
        int ans = 0, depth = 0;
        q.push(root);

        while (!q.empty()) 
        {            
            int s = q.size();
            for(int i = 0; i < s; i++) 
            {
                root = q.front();
                q.pop();
                
                if (root->left) q.push(root->left);
                if (root->right) q.push(root->right);
            }
            depth += 1;
            ans = max(ans, depth);
        }
        return ans;
    }


    int maxDepthStkPreorder(TreeNode* root) {
        if (root == NULL) return 0;

        stack<pair<TreeNode*, int>> s;
        int ans = 1, depth = 1;
        s.push({root, depth});
        while (!s.empty()) 
        {
            root = s.top().first;
            depth = s.top().second;

            ans = max(ans, depth);
            s.pop();
            if (root->left) s.push({root->left, depth + 1});
            if (root->right) s.push({root->right, depth + 1});
        }
        return ans;
    }

    int maxDepthStkInorder(TreeNode* root) {
        stack<pair<TreeNode*, int>> s;
        int ans = 0, depth = 0;

        while (root || !s.empty())
        {
            while (root != NULL)
            {
                s.push(make_pair(root, ++depth));
                root = root->left;
            }

            root = s.top().first; 
            ans = max(ans, depth);
            
            depth = s.top().second;
            s.pop();
            
            root = root->right;
        }
        return ans;
    }

    int maxDepthRecur(TreeNode* root) {
        // recursive DFS
        if (root == NULL) return 0;

        // we should inc. the depth by 1 here
        // and check for max in left and right subtrees 

        return 1 + max(maxDepthRecur(root->left), maxDepthRecur(root->right));
    }
}
```
