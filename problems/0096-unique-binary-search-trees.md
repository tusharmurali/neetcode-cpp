# 96. Unique Binary Search Trees

- **Difficulty:** Medium  
- **Pattern:** Trees  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/unique-binary-search-trees/>  
- **NeetCode:** <https://neetcode.io/problems/unique-binary-search-trees>  
- **Video:** <https://www.youtube.com/watch?v=Ox0TenN3Zpg>  

[← Back to index](../INDEX.md)

## 1. Recursion

To count all unique BSTs with values `1` to `n`, we need to consider each value as the root. When we choose `i` as the root, all values less than `i` must go in the left subtree, and all values greater than `i` go in the right subtree. The total number of unique BSTs with root `i` is the product of unique BSTs that can be formed from the left and right subtrees.

This gives us a recursive structure: the count for `n` nodes equals the sum over all possible roots of (count for left subtree) times (count for right subtree).

```cpp
class Solution {
public:
    int numTrees(int n) {
        if (n <= 1) {
            return 1;
        }

        int res = 0;
        for (int i = 1; i <= n; i++) {
            res += numTrees(i - 1) * numTrees(n - i);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(3 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Dynamic Programming (Top-Down)

The recursive solution recalculates the same values multiple times. For instance, `numTrees(3)` might be computed several times when calculating `numTrees(5)`. We can use memoization to cache results and avoid redundant work.

```cpp
class Solution {
private:
    unordered_map<int, int> dp;

public:
    int numTrees(int n) {
        if (n <= 1) {
            return 1;
        }
        if (dp.find(n) != dp.end()) {
            return dp[n];
        }

        int res = 0;
        for (int i = 1; i <= n; i++) {
            res += numTrees(i - 1) * numTrees(n - i);
        }

        dp[n] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

Instead of recursion, we can build the solution iteratively from smaller subproblems. Since the count for `n` nodes depends only on counts for fewer nodes, we compute `numTree[0]`, `numTree[1]`, ..., `numTree[n]` in order.

```cpp
class Solution {
public:
    int numTrees(int n) {
        vector<int> numTree(n + 1, 1);

        for (int nodes = 2; nodes <= n; ++nodes) {
            int total = 0;
            for (int root = 1; root <= nodes; ++root) {
                int left = root - 1;
                int right = nodes - root;
                total += numTree[left] * numTree[right];
            }
            numTree[nodes] = total;
        }

        return numTree[n];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 4. Catalan Numbers - I

The number of unique BSTs with `n` nodes is the nth Catalan number. Catalan numbers have a closed-form formula that can be computed directly without iterating through all subproblems. The formula involves calculating a product of fractions.

```cpp
class Solution {
public:
    int numTrees(int n) {
        long long res = 1;
        for (int i = 1; i < n; i++) {
            res *= (n + i + 1);
            res /= i;
        }
        return res / n;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 5. Catalan Numbers - II

Another formula for Catalan numbers uses a recurrence relation: `C(n+1) = C(n) * (4n + 2) / (n + 2)`. This allows us to compute each Catalan number from the previous one with a single multiplication and division.

```cpp
class Solution {
public:
    int numTrees(int n) {
        long long res = 1;
        for (int i = 0; i < n; i++) {
            res *= (4 * i + 2) / (i + 2.0);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
