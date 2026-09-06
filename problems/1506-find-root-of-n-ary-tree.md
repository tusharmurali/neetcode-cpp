# 1506. Find Root of N-Ary Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-root-of-n-ary-tree/>  
- **NeetCode:** <https://neetcode.io/problems/find-root-of-n-ary-tree>  

[← Back to index](../INDEX.md)

## 1. O(n) Space

The root of a tree is the only node that is never a child of any other node. By collecting all child nodes into a set, we can identify the root as the node whose value does not appear in the set. Every non-root node will appear exactly once as someone's child, but the root never will.

```cpp
class Solution {
public:
    Node* findRoot(vector<Node*> tree) {
        // set that contains all the child nodes.
        unordered_set<int> seen;

        // add all the child nodes into the set
        for (Node* node : tree) {
            for (Node* child : node->children) {
                // we could either add the value or the node itself.
                seen.insert(child->val);
            }
        }

        Node* root = nullptr;
        // find the node that is not in the child node set.
        for (Node* node : tree) {
            if (seen.find(node->val) == seen.end()) {
                root = node;
                break;
            }
        }

        return root;
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(N)$

> Where $N$ is the length of the input list, which is also the number of nodes in the N-ary tree.

## 2. O(1) Space

Every node except the root appears exactly once as a parent and exactly once as a child. If we add each node's value as a parent and subtract each child's value, all non-root nodes will cancel out (added once, subtracted once). The root is only added as a parent but never subtracted as a child, so the final sum equals the root's value.

```cpp
class Solution {
public:
    Node* findRoot(vector<Node*> tree) {
        int value_sum = 0;

        for (Node* node : tree) {
            // the value is added as a parent node
            value_sum += node->val;
            for (Node* child : node->children) {
                // the value is deducted as a child node.
                value_sum -= child->val;
            }
        }

        // the value of the root node is `value_sum`
        for (Node* node : tree) {
            if (node->val == value_sum) {
                return node;
            }
        }
        return nullptr;
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(1)$

> Where $N$ is the length of the input list, which is also the number of nodes in the N-ary tree.
