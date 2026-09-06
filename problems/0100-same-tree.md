# 100. Same Tree

- **Difficulty:** Easy  
- **Pattern:** Trees  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/same-tree/>  
- **NeetCode:** <https://neetcode.io/problems/same-binary-tree>  
- **Video:** <https://www.youtube.com/watch?v=vRbbcKXCxOw>  

[← Back to index](../INDEX.md)

## 1. Depth First Search

Two binary trees are the same if:

1. Their structure is identical.
2. Their corresponding nodes have the same values.

So at every position:

- If both nodes are `null` → they match.
- If one is `null` but the other isn't → mismatch.
- If both exist but values differ → mismatch.
- Otherwise, compare their left subtrees and right subtrees recursively.

This is a direct structural + value-based DFS comparison.

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
    bool isSameTree(TreeNode* p, TreeNode* q) {
        if (!p && !q) {
            return true;
        }
        if (p && q && p->val == q->val) {
            return isSameTree(p->left, q->left) && isSameTree(p->right, q->right);
        } else {
            return false;
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(h)$
    - Best Case ([balanced tree](https://www.geeksforgeeks.org/balanced-binary-tree/)): $O(log(n))$
    - Worst Case ([degenerate tree](https://www.geeksforgeeks.org/introduction-to-degenerate-binary-tree/)): $O(n)$

> Where $n$ is the number of nodes in the tree and $h$ is the height of the tree.

## 2. Iterative DFS

Instead of using recursion, we can use an explicit stack to compare the two trees.
Each stack entry contains a pair of nodes—one from each tree—that should match.

For every pair:

- If both are `null`, they match → continue.
- If only one is `null`, or their values differ → trees are not the same.
- If they match, push their children in the same order:
    - Left child pair
    - Right child pair

If we finish processing all pairs with no mismatch, the trees are identical.

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
    bool isSameTree(TreeNode* p, TreeNode* q) {
        stack<pair<TreeNode*, TreeNode*>> stk;
        stk.push({p, q});

        while (!stk.empty()) {
            auto [node1, node2] = stk.top();
            stk.pop();

            if (!node1 && !node2) continue;
            if (!node1 || !node2 || node1->val != node2->val) return false;

            stk.push({node1->right, node2->right});
            stk.push({node1->left, node2->left});
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Breadth First Search

BFS (level-order traversal) lets us compare the two trees **level by level**.
We maintain two queues—one for each tree. At every step, we remove a pair of nodes
that should match:

- If both nodes are `null`, they match → continue.
- If only one is `null`, or their values differ → trees are not the same.
- If they match, we push their children into their respective queues
  **in the same order**: left child first, then right child.

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
    bool isSameTree(TreeNode* p, TreeNode* q) {
        queue<TreeNode*> q1;
        queue<TreeNode*> q2;
        q1.push(p);
        q2.push(q);

        while (!q1.empty() && !q2.empty()) {
            for (int i = q1.size(); i > 0; i--) {
                TreeNode* nodeP = q1.front(); q1.pop();
                TreeNode* nodeQ = q2.front(); q2.pop();

                if (!nodeP && !nodeQ) continue;
                if (!nodeP || !nodeQ || nodeP->val != nodeQ->val)
                    return false;

                q1.push(nodeP->left);
                q1.push(nodeP->right);
                q2.push(nodeQ->left);
                q2.push(nodeQ->right);
            }
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0100-same-tree.cpp` in the NeetCode repo)

```cpp
/*
    Given roots of 2 binary trees, check if they're the same or not (same structure & values)
    Ex. p = [1,2,3] q = [1,2,3] -> true, p = [1,2] q = [1,null,2] -> false

    Check: (1) matching nulls, (2) non-matching nulls, (3) non-matching values

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
    bool isSameTree(TreeNode* p, TreeNode* q) {
        if (p == NULL && q == NULL) {
            return true;
        }
        if (p == NULL || q == NULL) {
            return false;
        }
        if (p->val != q->val) {
            return false;
        }
        return isSameTree(p->left, q->left) && isSameTree(p->right, q->right);
    }
};
```
