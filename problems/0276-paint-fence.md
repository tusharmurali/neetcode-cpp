# 276. Paint Fence

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/paint-fence/>  
- **NeetCode:** <https://neetcode.io/problems/paint-fence>  

[← Back to index](../INDEX.md)

## 1. Top-Down Dynamic Programming (Recursion + Memoization)

The constraint is that no more than two consecutive posts can have the same color. For each post, we can either paint it a different color from the previous post, or paint it the same color (but only if the two previous posts are different).

This leads to a recurrence: `totalWays(i) = (k - 1) * (totalWays(i - 1) + totalWays(i - 2))`. The first term handles painting post `i` differently from post `i - 1` (k - 1 choices). The second term handles painting post `i` the same as post `i - 1`, which requires post `i - 1` to be different from post `i - 2`.

```cpp
class Solution {
private:
    unordered_map<int, int> memo;

    int totalWays(int i, int k) {
        if (i == 1) return k;

        if (i == 2) return k * k;

        // Check if we have already calculated totalWays(i)
        if (memo.find(i) != memo.end()) {
            return memo[i];
        }

        // Use the recurrence relation to calculate totalWays(i)
        memo[i] = (k - 1) * (totalWays(i - 1, k) + totalWays(i - 2, k));
        return memo[i];
    }

public:
    int numWays(int n, int k) {
        return totalWays(n, k);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the number of fence posts.

## 2. Bottom-Up Dynamic Programming (Tabulation)

The same recurrence can be computed iteratively instead of recursively. We fill an array from the base cases up to n, which avoids recursion overhead and stack depth issues.

This approach is often more efficient in practice since it avoids function call overhead and naturally iterates through states in order.

```cpp
class Solution {
public:
    int numWays(int n, int k) {
        // Base cases for the problem to avoid index out of bound issues
        if (n == 1) return k;
        if (n == 2) return k * k;

        int totalWays[n + 1];
        totalWays[1] = k;
        totalWays[2] = k * k;

        for (int i = 3; i <= n; i++) {
            totalWays[i] = (k - 1) * (totalWays[i - 1] + totalWays[i - 2]);
        }

        return totalWays[n];
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the number of fence posts.

## 3. Bottom-Up, Constant Space

Since the recurrence only depends on the previous two values, we do not need to store the entire array. We can use two variables to track `totalWays(i - 1)` and `totalWays(i - 2)`, updating them as we iterate.

This optimization reduces space complexity from O(n) to O(1).

```cpp
class Solution {
public:
    int numWays(int n, int k) {
        if (n == 1) return k;

        int twoPostsBack = k;
        int onePostBack = k * k;

        for (int i = 3; i <= n; i++) {
            int curr = (k - 1) * (onePostBack + twoPostsBack);
            twoPostsBack = onePostBack;
            onePostBack = curr;
        }

        return onePostBack;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ constant space

> Where $n$ is the number of fence posts.
