# 255. Verify Preorder Sequence in Binary Search Tree

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/verify-preorder-sequence-in-binary-search-tree/>  
- **NeetCode:** <https://neetcode.io/problems/verify-preorder-sequence-in-binary-search-tree>  

[← Back to index](../INDEX.md)

## 1. Monotonic Stack

In a BST preorder traversal, we visit root, then left subtree, then right subtree. When we move to a right subtree, all subsequent values must be greater than the ancestors we are leaving behind. The key insight is to use a decreasing stack to track ancestors. When we encounter a larger value, we pop smaller ancestors and update the minimum limit, as we are now in a right subtree.

```cpp
class Solution {
public:
    bool verifyPreorder(vector<int>& preorder) {
        int minLimit = INT_MIN;
        stack<int> stack;

        for (int num: preorder) {
            while (!stack.empty() && stack.top() < num) {
                minLimit = stack.top();
                stack.pop();
            }

            if (num <= minLimit) {
                return false;
            }

            stack.push(num);
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the length of `preorder`

## 2. Constant Auxiliary Space

We can optimize the stack approach by reusing the input array itself as our stack. Since we process elements left to right and the stack never grows larger than the elements we have processed, we can use the prefix of the preorder array to simulate the stack.

```cpp
class Solution {
public:
    bool verifyPreorder(vector<int>& preorder) {
        int minLimit = INT_MIN;
        int i = 0;

        for (int num: preorder) {
            while (i > 0 && preorder[i - 1] < num) {
                minLimit = preorder[i - 1];
                i--;
            }

            if (num <= minLimit) {
                return false;
            }

            preorder[i] = num;
            i++;
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ auxiliary
    - A common misconception is that modifying an input array for use in an algorithm leads to an $O(1)$ space complexity. In reality, you are still using $O(n)$ space, but $O(1)$ **auxiliary** space.

    - Because we are modifying the input to directly use in the algorithm, we must count it as part of the space complexity. However, we are not using any auxiliary space other than a few integers.
      The exception to this is in-place algorithms where the input is also returned as the output. For example: sorting algorithms.

> Where $n$ is the length of `preorder`

## 3. Recursion

We can verify the preorder sequence by simulating the construction of the BST. Each recursive call attempts to build a subtree within given bounds. The key insight is that for a valid preorder sequence, we can greedily consume elements that fall within the current subtree's valid range, recursively processing left and right subtrees.

```cpp
class Solution {
public:
    bool verifyPreorder(vector<int>& preorder) {
        int i = 0;
        return helper(preorder, i, INT_MIN, INT_MAX);
    }

    bool helper(vector<int>& preorder, int& i, int minLimit, int maxLimit) {
        if (i == preorder.size()) {
            return true;
        }

        int root = preorder[i];
        if (root <= minLimit || root >= maxLimit) {
            return false;
        }

        i++;
        bool left = helper(preorder, i, minLimit, root);
        bool right = helper(preorder, i, root, maxLimit);
        return left || right;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the length of `preorder`
