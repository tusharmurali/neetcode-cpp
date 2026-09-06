# 652. Find Duplicate Subtrees

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-duplicate-subtrees/>  
- **NeetCode:** <https://neetcode.io/problems/find-duplicate-subtrees>  
- **Video:** <https://www.youtube.com/watch?v=kn0Z5_qPPzY>  

[← Back to index](../INDEX.md)

## 1. Brute Force (DFS)

The most straightforward way to find duplicate subtrees is to compare every subtree with every other subtree. We first collect all nodes using DFS, then for each pair of nodes, we check if their subtrees are structurally identical with matching values. When we find a match, we add one representative to the result and mark both as seen to avoid duplicates.

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
    vector<TreeNode*> findDuplicateSubtrees(TreeNode* root) {
        vector<TreeNode*> res;
        unordered_set<TreeNode*> seen;
        vector<TreeNode*> subTree;
        dfs(root, subTree);

        for (int i = 0; i < subTree.size(); i++) {
            if (seen.count(subTree[i])) continue;
            for (int j = i + 1; j < subTree.size(); j++) {
                if (seen.count(subTree[j])) continue;

                if (same(subTree[i], subTree[j])) {
                    if (!seen.count(subTree[i])) {
                        res.push_back(subTree[i]);
                        seen.insert(subTree[i]);
                    }
                    seen.insert(subTree[j]);
                }
            }
        }
        return res;
    }

private:
    bool same(TreeNode* node1, TreeNode* node2) {
        if (!node1 && !node2) return true;
        if (!node1 || !node2) return false;
        return node1->val == node2->val &&
               same(node1->left, node2->left) &&
               same(node1->right, node2->right);
    }

    void dfs(TreeNode* root, vector<TreeNode*>& subTree) {
        if (!root) return;
        subTree.push_back(root);
        dfs(root->left, subTree);
        dfs(root->right, subTree);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(n)$

## 2. DFS + Serialization

Instead of comparing subtrees pairwise, we can serialize each subtree into a unique string representation. Two subtrees are identical if and only if they produce the same serialization. By storing these strings in a hash map, we can detect duplicates in a single pass through the tree. When we see the same serialization for the second time, we know we have found a duplicate.

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
    unordered_map<string, vector<TreeNode*>> subtrees;
    vector<TreeNode*> res;

public:
    vector<TreeNode*> findDuplicateSubtrees(TreeNode* root) {
        dfs(root);
        return res;
    }

private:
    string dfs(TreeNode* node) {
        if (!node) return "null";
        string s = to_string(node->val) + "," + dfs(node->left) + "," + dfs(node->right);
        if (subtrees[s].size() == 1) {
            res.push_back(node);
        }
        subtrees[s].push_back(node);
        return s;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Depth First Search (Optimal)

The serialization approach has quadratic space complexity because string concatenation creates long strings for large trees. We can optimize by assigning a unique integer ID to each distinct subtree structure. Instead of storing full serialization strings, we represent each subtree as a tuple of `(left_id, value, right_id)` and map this tuple to a unique ID. This keeps the key size constant regardless of subtree depth.

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
    unordered_map<string, int> idMap;
    unordered_map<int, int> count;
    vector<TreeNode*> res;

public:
    vector<TreeNode*> findDuplicateSubtrees(TreeNode* root) {
        dfs(root);
        return res;
    }

private:
    int dfs(TreeNode* node) {
        if (!node) return -1;
        string cur = to_string(dfs(node->left)) + "," +
                     to_string(node->val) + "," +
                     to_string(dfs(node->right));
        if (idMap.find(cur) == idMap.end()) {
            idMap[cur] = idMap.size();
        }
        int curId = idMap[cur];
        count[curId]++;
        if (count[curId] == 2) {
            res.push_back(node);
        }
        return curId;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
