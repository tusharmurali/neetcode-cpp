# 129. Sum Root to Leaf Numbers

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/sum-root-to-leaf-numbers/>  
- **NeetCode:** <https://neetcode.io/problems/sum-root-to-leaf-numbers>  
- **Video:** <https://www.youtube.com/watch?v=Jk16lZGFWxE>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

Each root-to-leaf path in the tree represents a number, where digits are concatenated from root to leaf. As we traverse down the tree, we build the number by multiplying the accumulated value by 10 and adding the current node's value. When we reach a leaf node, we have a complete number to add to our sum. DFS naturally follows paths from root to leaf, making it ideal for this problem.

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
    int sumNumbers(TreeNode* root) {
        return dfs(root, 0);
    }

private:
    int dfs(TreeNode* cur, int num) {
        if (!cur) return 0;

        num = num * 10 + cur->val;
        if (!cur->left && !cur->right) return num;

        return dfs(cur->left, num) + dfs(cur->right, num);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(h)$ for recursion stack.

> Where $n$ is the number of nodes and $h$ is the height of the given tree.

## 2. Breadth First Search

Instead of going deep first, we can process the tree level by level using a queue. Each entry in the queue stores both a node and the number accumulated along the path to reach that node. When we dequeue a leaf node, we add its accumulated number to the total. BFS ensures we visit all nodes while tracking each path's value independently.

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
    int sumNumbers(TreeNode* root) {
        int res = 0;
        queue<pair<TreeNode*, int>> q;
        q.push({root, 0});
        while (!q.empty()) {
            auto [cur, num] = q.front();q.pop();
            num = num * 10 + cur->val;
            if (!cur->left && !cur->right) {
                res += num;
                continue;
            }

            if (cur->left) q.push({cur->left, num});
            if (cur->right) q.push({cur->right, num});
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Iterative DFS

We can simulate the recursive DFS using an explicit stack instead of the call stack. This avoids potential stack overflow for very deep trees. The key insight is to always go left while tracking right children on the stack for later processing. Each stack entry remembers the accumulated number at that point so we can correctly continue building path values.

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
    int sumNumbers(TreeNode* root) {
        int res = 0;
        stack<pair<TreeNode*, int>> st;
        TreeNode* cur = root;
        int num = 0;

        while (cur || !st.empty()) {
            if (cur) {
                num = num * 10 + cur->val;
                if (!cur->left && !cur->right)
                    res += num;

                st.push({cur->right, num});
                cur = cur->left;
            } else {
                cur = st.top().first;
                num = st.top().second;
                st.pop();
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(h)$

> Where $n$ is the number of nodes and $h$ is the height of the given tree.

## 4. Morris Traversal

Morris traversal allows us to traverse the tree without using extra space for a stack or recursion. It temporarily modifies the tree by creating links from predecessors back to their successors. The challenge here is tracking the accumulated number: when we return to a node via a temporary link, we need to "undo" the digits we added while going down the left subtree. We track the number of steps taken to reach the predecessor and divide by the corresponding power of `10` to remove those digits.

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
    int sumNumbers(TreeNode* root) {
        int res = 0, num = 0;
        int power[10] = {1};
        for (int i = 1; i < 10; i++) {
            power[i] = power[i - 1] * 10;
        }

        TreeNode* cur = root;
        while (cur) {
            if (!cur->left) {
                num = num * 10 + cur->val;
                if (!cur->right) res += num;
                cur = cur->right;
            } else {
                TreeNode* prev = cur->left;
                int steps = 1;
                while (prev->right && prev->right != cur) {
                    prev = prev->right;
                    steps++;
                }

                if (!prev->right) {
                    prev->right = cur;
                    num = num * 10 + cur->val;
                    cur = cur->left;
                } else {
                    prev->right = nullptr;
                    if (!prev->left) res += num;
                    num /= power[steps];
                    cur = cur->right;
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/0129-sum-root-to-leaf-numbers.cpp` in the NeetCode repo)

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
    int sumNumbers(TreeNode* root) {
        if (!root)
            return 0;
        stack<pair<TreeNode*, int> > stk;
        stk.push(make_pair(root, root->val));

        int sum = 0;
        while (!stk.empty()) {
            pair<TreeNode*, int> elm = stk.top();
            stk.pop();
            TreeNode* node = elm.first;
            int num = elm.second;
            if (!node->left && !node->right) {
                sum += num;
                continue;
            }
            if (node->left)
                stk.push(make_pair(node->left, num * 10 + node->left->val));
            if (node->right)
                stk.push(make_pair(node->right, num * 10 + node->right->val));
        }
        return sum;
    }  
};
```
