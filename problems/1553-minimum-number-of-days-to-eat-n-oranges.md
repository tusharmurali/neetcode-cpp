# 1553. Minimum Number of Days to Eat N Oranges

- **Difficulty:** Hard  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-number-of-days-to-eat-n-oranges/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-number-of-days-to-eat-n-oranges>  
- **Video:** <https://www.youtube.com/watch?v=LziQ6Qx9sks>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

At each step, we can eat one orange, half the oranges (if divisible by `2`), or two-thirds of the oranges (if divisible by `3`). A naive recursion explores all three options at each state and picks the minimum.

The challenge is that `n` can be very large, but memoization helps by caching results for previously computed values. However, this approach still explores too many states because eating one orange at a time creates many intermediate values.

```cpp
class Solution {
public:
    unordered_map<int, int> dp;

    int minDays(int n) {
        return dfs(n);
    }

    int dfs(int n) {
        if (n == 0) return 0;
        if (dp.count(n)) return dp[n];

        int res = 1 + dfs(n - 1);
        if (n % 3 == 0) res = min(res, 1 + dfs(n / 3));
        if (n % 2 == 0) res = min(res, 1 + dfs(n / 2));

        return dp[n] = res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Greedy + Dynamic Programming (Top-Down)

The key optimization is recognizing that we should always try to divide rather than subtract one repeatedly. Instead of exploring `n - 1` recursively (which creates exponentially many states), we can directly compute how many subtractions are needed to reach a divisible number.

To reach a number divisible by `2`, we need `n % 2` subtractions. To reach a number divisible by `3`, we need `n % 3` subtractions. By adding these remainder costs upfront, we only need to recurse on `n / 2` and `n / 3`, drastically reducing the state space to O(log `n`).

```cpp
class Solution {
public:
    unordered_map<int, int> dp;

    int minDays(int n) {
        dp[0] = 0;
        dp[1] = 1;
        return dfs(n);
    }

private:
    int dfs(int n) {
        if (dp.count(n)) return dp[n];

        int res = 1 + (n % 2) + dfs(n / 2);
        res = min(res, 1 + (n % 3) + dfs(n / 3));

        return dp[n] = res;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(\log n)$

## 3. Breadth First Search

BFS naturally finds the shortest path in an unweighted graph. Here, each state (number of oranges) is a node, and each valid operation is an edge. Since all edges have equal cost (one day), BFS will find the minimum days when we first reach `0`.

We use a visited set to avoid reprocessing the same orange count. From each state, we explore eating one orange, and optionally dividing by `2` or `3` if applicable.

```cpp
class Solution {
public:
    int minDays(int n) {
        queue<int> q;
        unordered_set<int> visit;
        q.push(n);
        int res = 0;

        while (!q.empty()) {
            res++;
            for (int i = q.size(); i > 0; i--) {
                int node = q.front(); q.pop();
                int nei = node - 1;
                if (nei == 0) return res;
                if (visit.find(nei) == visit.end()) {
                    visit.insert(nei);
                    q.push(nei);
                }
                for (int d = 2; d <= 3; d++) {
                    if (node % d == 0) {
                        nei = node / d;
                        if (nei == 0) return res;
                        if (visit.find(nei) == visit.end()) {
                            visit.insert(nei);
                            q.push(nei);
                        }
                    }
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(\log n)$
