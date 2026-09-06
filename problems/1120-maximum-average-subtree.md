# 1120. Maximum Average Subtree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-average-subtree/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-average-subtree>  

[← Back to index](../INDEX.md)

## 1. Postorder Traversal

To find the subtree with the maximum average, we need to know each subtree's sum and node count. A key observation is that a subtree's values depend entirely on its children's values. This makes postorder traversal the natural choice: we process children first, then use their results to compute the parent's values.

For each node, we track three things: the number of nodes in its subtree, the sum of values in its subtree, and the maximum average found so far. By bubbling these values up from leaves to the root, we can compute the average at every node and keep track of the best one.

```cpp
class Solution {
public:
    double maximumAverageSubtree(TreeNode* root) {
        return maxAverage(root).maxAverage;
    }

private:
    struct State {
        // count of nodes in the subtree
        int nodeCount;

        // sum of values in the subtree
        int valueSum;

        // max average found in the subtree
        double maxAverage;
    };

    State maxAverage(TreeNode* root) {
        if (!root) return {0, 0, 0};

        // postorder traversal, solve for both child nodes first.
        State left = maxAverage(root->left);
        State right = maxAverage(root->right);

        // now find nodeCount, valueSum and maxAverage for current node `root`
        int nodeCount = left.nodeCount + right.nodeCount + 1;
        int sum = left.valueSum + right.valueSum + root->val;
        double maxAverage = max(
                (1.0 * (sum)) / nodeCount, // average for current node
                max(right.maxAverage, left.maxAverage) // max average from child nodes
        );

        return {nodeCount, sum, maxAverage};
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(N)$

> Where $N$ is the number of nodes in the tree
