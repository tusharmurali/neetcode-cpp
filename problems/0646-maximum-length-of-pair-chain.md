# 646. Maximum Length of Pair Chain

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-length-of-pair-chain/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-length-of-pair-chain>  
- **Video:** <https://www.youtube.com/watch?v=LcNNorqMVTw>  

[← Back to index](../INDEX.md)

## 1. Recursion

A pair `[a, b]` can follow pair `[c, d]` in a chain only if `d < a`. To build the longest chain, we can use recursion to explore all possibilities: for each pair, we either include it in the chain (if valid) or skip it. Sorting by the second element helps us process pairs in an order that makes chain-building more intuitive.

```cpp
class Solution {
public:
    int findLongestChain(vector<vector<int>>& pairs) {
        int n = pairs.size();
        sort(pairs.begin(), pairs.end(), [](const auto& a, const auto& b) {
            return a[1] < b[1];
        });

        return dfs(pairs, 0, -1, n);
    }

private:
    int dfs(vector<vector<int>>& pairs, int i, int j, int n) {
        if (i == n) {
            return 0;
        }

        int res = dfs(pairs, i + 1, j, n);
        if (j == -1 || pairs[j][1] < pairs[i][0]) {
            res = max(res, 1 + dfs(pairs, i + 1, i, n));
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems since we may reach the same state `(i, j)` through different paths. By caching results in a 2D array, we avoid redundant computation. Each state represents the maximum chain length achievable starting from index `i` when the last included pair was at index `j`.

```cpp
class Solution {
public:
    vector<vector<int>> dp;

    int findLongestChain(vector<vector<int>>& pairs) {
        int n = pairs.size();
        sort(pairs.begin(), pairs.end(), [](const auto& a, const auto& b) {
            return a[1] < b[1];
        });

        dp = vector<vector<int>>(n, vector<int>(n + 1, -1));
        return dfs(pairs, 0, -1, n);
    }

private:
    int dfs(vector<vector<int>>& pairs, int i, int j, int n) {
        if (i == n) {
            return 0;
        }
        if (dp[i][j + 1] != -1) {
            return dp[i][j + 1];
        }

        int res = dfs(pairs, i + 1, j, n);
        if (j == -1 || pairs[j][1] < pairs[i][0]) {
            res = max(res, 1 + dfs(pairs, i + 1, i, n));
        }

        dp[i][j + 1] = res;
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Dynamic Programming (Bottom-Up)

We can build the solution iteratively. For each pair, we look at all previous pairs and find the longest chain that can be extended by the current pair. After sorting by end values, `dp[i]` represents the longest chain ending at pair `i`.

```cpp
class Solution {
public:
    int findLongestChain(vector<vector<int>>& pairs) {
        int n = pairs.size();
        sort(pairs.begin(), pairs.end(), [](const auto& a, const auto& b) {
            return a[1] < b[1];
        });

        vector<int> dp(n, 1);

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (pairs[j][1] < pairs[i][0]) {
                    dp[i] = max(dp[i], dp[j] + 1);
                }
            }
        }

        return *max_element(dp.begin(), dp.end());
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Binary Search)

This approach is similar to the Longest Increasing Subsequence optimization. We maintain a list where `dp[i]` stores the smallest end value of any chain of length `i+1`. When processing a new pair, we binary search to find where it can extend an existing chain. By keeping track of the smallest possible end values, we maximize opportunities for future extensions.

```cpp
class Solution {
public:
    int findLongestChain(vector<vector<int>>& pairs) {
        sort(pairs.begin(), pairs.end());
        vector<int> dp;

        for (auto& pair : pairs) {
            auto it = lower_bound(dp.begin(), dp.end(), pair[0]);
            if (it == dp.end()) {
                dp.push_back(pair[1]);
            } else {
                *it = min(*it, pair[1]);
            }
        }

        return dp.size();
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 5. Greedy

This problem is identical to the classic interval scheduling problem. By sorting pairs by their end values, we can greedily select pairs. The key insight is that choosing the pair with the smallest end value leaves the most room for subsequent pairs. Whenever we find a pair whose start is greater than our current chain's end, we add it to the chain.

```cpp
class Solution {
public:
    int findLongestChain(vector<vector<int>>& pairs) {
        sort(pairs.begin(), pairs.end(), [](const auto& a, const auto& b) {
            return a[1] < b[1];
        });

        int length = 1, end = pairs[0][1];

        for (int i = 1; i < pairs.size(); i++) {
            if (end < pairs[i][0]) {
                length++;
                end = pairs[i][1];
            }
        }

        return length;
    }
};
```

**Complexity**

- Time complexity: $O(n\log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.
