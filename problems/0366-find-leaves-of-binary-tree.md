# 366. Find Leaves of Binary Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-leaves-of-binary-tree/>  
- **NeetCode:** <https://neetcode.io/problems/find-leaves-of-binary-tree>  

[← Back to index](../INDEX.md)

## 1. DFS (Depth-First Search) with sorting

Leaves are nodes with no children, and they have height `0`. Their parents have height `1`, and so on. If we compute the height of each node (where height is the distance to the farthest leaf in its subtree), nodes with the same height should be grouped together. By collecting all (height, value) pairs and sorting by height, we can form the required groups.

```cpp
class Solution {
public:

    vector<pair<int, int>> pairs;

    int getHeight(TreeNode *root) {

        // return -1 for null nodes
        if (!root) return -1;

        // first calculate the height of the left and right children
        int leftHeight = getHeight(root->left);
        int rightHeight = getHeight(root->right);

        // based on the height of the left and right children, obtain the height of the current (parent) node
        int currHeight = max(leftHeight, rightHeight) + 1;

        // collect the pair -> (height, val)
        this->pairs.push_back({currHeight, root->val});

        // return the height of the current node
        return currHeight;
    }

    vector<vector<int>> findLeaves(TreeNode* root) {
        this->pairs.clear();

        getHeight(root);

        // sort all the (height, val) pairs
        sort(this->pairs.begin(), this->pairs.end());

        int n = this->pairs.size(), height = 0, i = 0;
        vector<vector<int>> solution;
        while (i < n) {
            vector<int> nums;
            while (i < n && this->pairs[i].first == height) {
                nums.push_back(this->pairs[i].second);
                i++;
            }
            solution.push_back(nums);
            height++;
        }
        return solution;
    }
};
```

**Complexity**

- Time complexity: $O(N \log N)$
- Space complexity: $O(N)$

> Where $N$ is the total number of nodes in the binary tree

## 2. DFS (Depth-First Search) without sorting

Instead of collecting pairs and sorting, we can directly place each node into the correct group during the DFS. When we compute a node's height, we use that height as an index into the result list. If the list doesn't have enough sublists yet, we create a new one.

```cpp
class Solution {
private:

    vector<vector<int>> solution;

public:

    int getHeight(TreeNode *root) {

        if (!root) {
            return -1;
        }

        int leftHeight = getHeight(root->left);
        int rightHeight = getHeight(root->right);

        int currHeight = max(leftHeight, rightHeight) + 1;

        if (this->solution.size() == currHeight) {
            this->solution.push_back({});
        }

        this->solution[currHeight].push_back(root->val);

        return currHeight;
    }

    vector<vector<int>> findLeaves(TreeNode* root) {
        this->solution.clear();

        getHeight(root);

        return this->solution;
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(N)$

> Where $N$ is the total number of nodes in the binary tree
