# 1522. Diameter of N-Ary Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/diameter-of-n-ary-tree/>  
- **NeetCode:** <https://neetcode.io/problems/diameter-of-n-ary-tree>  

[← Back to index](../INDEX.md)

## 1. Distance with Height

The diameter of a tree is the longest path between any two nodes. This path must pass through some node as the highest point (closest to root). At that node, the path goes down through two different children. So the longest path through any node equals the sum of the two largest heights among its children. By computing heights recursively and tracking the maximum path length, we find the diameter.

```cpp
class Solution {
protected:
    int dia = 0;

    int height(Node* node) {
        if (node->children.size() == 0)
            return 0;

        int maxHeight1 = 0, maxHeight2 = 0;
        for (Node* child : node->children) {
            int parentHeight = height(child) + 1;
            if (parentHeight > maxHeight1) {
                maxHeight2 = maxHeight1;
                maxHeight1 = parentHeight;
            } else if (parentHeight > maxHeight2) {
                maxHeight2 = parentHeight;
            }
            int distance = maxHeight1 + maxHeight2;
            dia = max(dia, distance);
        }
        return maxHeight1;
    }

public:
    int diameter(Node* root) {
        dia = 0;
        height(root);
        return dia;
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(N)$

> Where $N$ is the number of nodes in the tree.

## 2. Distance with Depth

Instead of tracking heights (distance down to leaves), we can track depths (distance from root). The diameter through a node equals the sum of the two deepest leaf paths minus twice the current node's depth. This accounts for the path going down to one leaf, back up to the current node, and down to another leaf.

```cpp
class Solution {
protected:
    int diameter = 0;

    /**
     * return the maximum depth of leaves nodes descending from the given node
     */
    int maxDepth(Node* node, int currDepth) {
        if (node->children.size() == 0)
            return currDepth;

        // select the top two largest depths
        int maxDepth1 = currDepth, maxDepth2 = 0;
        for (Node* child : node->children) {
            int depth = maxDepth(child, currDepth + 1);
            if (depth > maxDepth1) {
                maxDepth2 = maxDepth1;
                maxDepth1 = depth;
            } else if (depth > maxDepth2) {
                maxDepth2 = depth;
            }
            // calculate the distance between the two farthest leaves nodes.
            int distance = maxDepth1 + maxDepth2 - 2 * currDepth;
            this->diameter = max(this->diameter, distance);
        }
        return maxDepth1;
    }

public:
    int diameter(Node* root) {
        this->diameter = 0;
        maxDepth(root, 0);
        return diameter;
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(N)$

> Where $N$ is the number of nodes in the tree.
