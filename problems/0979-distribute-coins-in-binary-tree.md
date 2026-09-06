# 979. Distribute Coins in Binary Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/distribute-coins-in-binary-tree/>  
- **NeetCode:** <https://neetcode.io/problems/distribute-coins-in-binary-tree>  
- **Video:** <https://www.youtube.com/watch?v=YfdfIOeV_RU>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

Each node needs exactly one coin. If a subtree has more coins than nodes, the excess must flow up to the parent. If it has fewer coins than nodes, the deficit must be supplied from the parent. The number of moves across each edge equals the absolute difference between the subtree size and its total coins. By computing size and coins for each subtree during a post-order traversal, we can sum up all the required moves.

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
    int res;

    vector<int> dfs(TreeNode* cur) {
        if (!cur) {
            return {0, 0}; // [size, coins]
        }

        vector<int> left = dfs(cur->left);
        vector<int> right = dfs(cur->right);

        int size = 1 + left[0] + right[0];
        int coins = cur->val + left[1] + right[1];
        res += abs(size - coins);

        return {size, coins};
    }

public:
    int distributeCoins(TreeNode* root) {
        res = 0;
        dfs(root);
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Depth First Search (Optimal)

We can simplify the previous approach by tracking only the "extra coins" at each node. A node with `val` coins has `val - 1` extra coins (positive means surplus, negative means deficit). Each node's extra coins include its own plus what flows up from its children. The absolute value of extra coins at each node represents exactly how many coins must cross the edge to its parent.

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
    int res;

    int dfs(TreeNode* cur) {
        if (!cur) {
            return 0; // extra_coins
        }

        int lExtra = dfs(cur->left);
        int rExtra = dfs(cur->right);

        int extraCoins = cur->val - 1 + lExtra + rExtra;
        res += abs(extraCoins);
        return extraCoins;
    }

public:
    int distributeCoins(TreeNode* root) {
        res = 0;
        dfs(root);
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ fo recursion stack.

## 3. Breadth First Search

We can avoid recursion by using BFS to collect nodes level by level, then processing them in reverse order (leaves first). For each node, we transfer its extra coins (`val - 1`) to its parent and count the moves. Processing in reverse BFS order ensures children are handled before their parents, mimicking the post-order behavior of DFS.

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
    int distributeCoins(TreeNode* root) {
        int res = 0;
        queue<TreeNode*> q;
        unordered_map<TreeNode*, TreeNode*> parentMap;
        vector<TreeNode*> nodes;

        q.push(root);
        while (!q.empty()) {
            TreeNode* node = q.front();
            q.pop();
            nodes.push_back(node);
            if (node->left) {
                parentMap[node->left] = node;
                q.push(node->left);
            }
            if (node->right) {
                parentMap[node->right] = node;
                q.push(node->right);
            }
        }

        for (int i = nodes.size() - 1; i >= 0; i--) {
            TreeNode* node = nodes[i];
            if (parentMap.count(node)) {
                TreeNode* parent = parentMap[node];
                parent->val += node->val - 1;
                res += abs(node->val - 1);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Iterative DFS

This approach simulates recursive DFS using an explicit stack. We use a `visit` set to distinguish between the first visit (when we push children) and the second visit (when we process the node after its children are done). On the second visit, we accumulate coins from children, compute the extra coins, and add the absolute value to our result.

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
    int distributeCoins(TreeNode* root) {
        stack<TreeNode*> stack;
        unordered_set<TreeNode*> visit;
        stack.push(root);
        int res = 0;

        while (!stack.empty()) {
            TreeNode* node = stack.top();
            stack.pop();

            if (visit.find(node) == visit.end()) {
                stack.push(node);
                visit.insert(node);

                if (node->right) {
                    stack.push(node->right);
                }
                if (node->left) {
                    stack.push(node->left);
                }
            } else {
                if (node->left) {
                    node->val += node->left->val;
                }
                if (node->right) {
                    node->val += node->right->val;
                }

                visit.erase(node);
                node->val -= 1;
                res += abs(node->val);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
