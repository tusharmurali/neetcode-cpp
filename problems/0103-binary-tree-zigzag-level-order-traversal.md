# 103. Binary Tree Zigzag Level Order Traversal

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/>  
- **NeetCode:** <https://neetcode.io/problems/binary-tree-zigzag-level-order-traversal>  
- **Video:** <https://www.youtube.com/watch?v=igbboQbiwqw>  

[← Back to index](../INDEX.md)

## 1. Breadth First Search

Level order traversal naturally suggests using BFS with a queue. The zigzag pattern means we alternate the direction we read each level: left-to-right for even levels, right-to-left for odd levels. We can achieve this by collecting each level normally and then reversing it when needed based on the level index.

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
    vector<vector<int>> zigzagLevelOrder(TreeNode* root) {
        vector<vector<int>> res;
        if (!root) return res;

        queue<TreeNode*> q;
        q.push(root);

        while (!q.empty()) {
            vector<int> level;
            for (int i = q.size(); i > 0; i--) {
                TreeNode* node = q.front();
                q.pop();
                level.push_back(node->val);
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
            if (res.size() % 2) reverse(level.begin(), level.end());
            res.push_back(level);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Breadth First Search (Optimal)

Instead of reversing the list after collecting values, we can place each value directly at its correct position. For even levels, values go from index `0` to `size-1`. For odd levels, values go from index `size-1` to `0`. This avoids the extra reversal operation.

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
    vector<vector<int>> zigzagLevelOrder(TreeNode* root) {
        vector<vector<int>> res;
        if (!root) return res;

        queue<TreeNode*> q;
        q.push(root);

        while (!q.empty()) {
            int size = q.size();
            vector<int> level(size);
            for (int i = 0; i < size; ++i) {
                TreeNode* node = q.front();
                q.pop();
                int idx = (res.size() % 2 == 0) ? i : size - i - 1;
                level[idx] = node->val;
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
            res.push_back(level);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Depth First Search

DFS can also solve this problem by tracking the depth during traversal. We recursively visit nodes in a standard preorder manner (root, left, right), appending values to the appropriate level's list. After the traversal completes, we reverse the odd-indexed levels to achieve the zigzag pattern.

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
    vector<vector<int>> zigzagLevelOrder(TreeNode* root) {
        vector<vector<int>> res;
        dfs(root, 0, res);
        for (int i = 0; i < res.size(); ++i) {
            if (i & 1) {
                reverse(res[i].begin(), res[i].end());
            }
        }
        return res;
    }

private:
    void dfs(TreeNode* node, int depth, vector<vector<int>>& res) {
        if (!node) return;
        if (depth == res.size()) {
            res.push_back({});
        }
        res[depth].push_back(node->val);
        dfs(node->left, depth + 1, res);
        dfs(node->right, depth + 1, res);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Iterative DFS

This approach converts the recursive DFS to an iterative version using an explicit stack. Each stack entry stores both the node and its depth. We process nodes in the same order as recursive DFS by pushing the right child before the left child (so left is processed first). After collecting all values, we reverse the odd levels.

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
    vector<vector<int>> zigzagLevelOrder(TreeNode* root) {
        if (!root) return {};

        vector<vector<int>> res;
        stack<pair<TreeNode*, int>> s;
        s.push({root, 0});

        while (!s.empty()) {
            auto [node, depth] = s.top();
            s.pop();

            if (depth == res.size()) {
                res.push_back({});
            }
            res[depth].push_back(node->val);

            if (node->right) s.push({node->right, depth + 1});
            if (node->left) s.push({node->left, depth + 1});
        }

        for (int i = 0; i < res.size(); i++) {
            if (i % 2 == 1) {
                reverse(res[i].begin(), res[i].end());
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0103-binary-tree-zigzag-level-order-traversal.cpp` in the NeetCode repo)

```cpp
/*
  Given the root of a binary tree, return the zigzag level order traversal of its nodes' values. 
  (i.e., from left to right, then right to left for the next level and alternate between).

  Ex. Input: root = [3,9,20,null,null,15,7]
      Output: [[3],[20,9],[15,7]]

  Time  : O(N)
  Space : O(N)
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
    vector<vector<int>> zigzagLevelOrder(TreeNode* root) {
        vector <vector <int>> v;
        if(root == NULL)
            return v;
      
        queue <TreeNode *> q;
        q.push(root);
        bool changeDirection = true;
      
        while(!q.empty()) {
            vector <int> v1;
            int siz = q.size();
          
            for(int i = 0 ; i < siz ; i++) {
                if(changeDirection)
                    v1.push_back(q.front() -> val);
                else 
                    v1.insert(v1.begin(), q.front() -> val);
              
                if(q.front() -> left != NULL)
                    q.push(q.front() -> left);
                if(q.front() -> right != NULL)
                    q.push(q.front() -> right);
              
                q.pop();
            }
            changeDirection = !changeDirection;
            v.push_back(v1);
        }
        return v;
    }
};
```
