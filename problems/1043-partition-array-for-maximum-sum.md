# 1043. Partition Array for Maximum Sum

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/partition-array-for-maximum-sum/>  
- **NeetCode:** <https://neetcode.io/problems/partition-array-for-maximum-sum>  
- **Video:** <https://www.youtube.com/watch?v=kWhy4ZUBdOY>  

[← Back to index](../INDEX.md)

## 1. Recursion

We need to partition the array into subarrays of length at most k, where each element in a subarray becomes the maximum value of that subarray. The goal is to maximize the total sum after this transformation.

At each position, we have a choice: end the current subarray at any of the next k positions. For each choice, we calculate the contribution (maximum element times subarray length) and recursively solve the remaining array. We try all valid partition lengths and take the maximum result.

```cpp
class Solution {
public:
    int maxSumAfterPartitioning(vector<int>& arr, int k) {
        return dfs(0, arr, k);
    }

private:
    int dfs(int i, vector<int>& arr, int k) {
        if (i >= arr.size()) {
            return 0;
        }

        int cur_max = 0, res = 0;
        for (int j = i; j < min((int)arr.size(), i + k); j++) {
            cur_max = max(cur_max, arr[j]);
            int window_size = j - i + 1;
            res = max(res, dfs(j + 1, arr, k) + cur_max * window_size);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(k ^ n)$
- Space complexity: $O(n)$ for recursion stack.

> Where $k$ is the maximum length of the subarray and $n$ is the size of the array $arr$.

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems. When we compute the maximum sum starting from index `i`, we might need this value multiple times from different partition choices. By caching results, we avoid redundant calculations.

This is the memoized version of the recursive approach. We store computed results in a cache and return them directly when we encounter the same subproblem again.

```cpp
class Solution {
public:
    int maxSumAfterPartitioning(vector<int>& arr, int k) {
        vector<int> cache(arr.size() + 1, -1);
        cache[arr.size()] = 0;
        return dfs(0, arr, k, cache);
    }

private:
    int dfs(int i, vector<int>& arr, int k, vector<int>& cache) {
        if (cache[i] != -1) {
            return cache[i];
        }

        int cur_max = 0, res = 0;
        for (int j = i; j < min((int)arr.size(), i + k); j++) {
            cur_max = max(cur_max, arr[j]);
            int window_size = j - i + 1;
            res = max(res, dfs(j + 1, arr, k, cache) + cur_max * window_size);
        }

        return cache[i] = res;
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(n)$

> Where $k$ is the maximum length of the subarray and $n$ is the size of the array $arr$.

## 3. Dynamic Programming (Bottom-Up)

We can flip the top-down approach to bottom-up by filling the DP table from right to left. `dp[i]` represents the maximum sum achievable for the subarray starting at index `i`.

Starting from the last element and working backwards, we build up solutions to larger subproblems using already-computed smaller ones. This eliminates recursion overhead and makes the memory access pattern more predictable.

```cpp
class Solution {
public:
    int maxSumAfterPartitioning(vector<int>& arr, int k) {
        int n = arr.size();
        vector<int> dp(n + 1, 0);

        for (int i = n - 1; i >= 0; i--) {
            int cur_max = 0;
            for (int j = i; j < min(n, i + k); j++) {
                cur_max = max(cur_max, arr[j]);
                int window_size = j - i + 1;
                dp[i] = max(dp[i], dp[j + 1] + cur_max * window_size);
            }
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(n)$

> Where $k$ is the maximum length of the subarray and $n$ is the size of the array $arr$.

## 4. Dynamic Programming (Space Optimized)

Looking at the bottom-up solution, we notice that `dp[i]` only depends on `dp[i+1]` through `dp[i+k]`. We never need values more than k positions ahead. This means we can reduce our space from O(n) to O(k) using a circular buffer.

We use modulo arithmetic to wrap around and reuse array positions. This technique is common when the recurrence relation has a bounded look-ahead.

```cpp
class Solution {
public:
    int maxSumAfterPartitioning(vector<int>& arr, int k) {
        int n = arr.size();
        vector<int> dp(k);
        dp[0] = arr[0];

        for (int i = 1; i < n; i++) {
            int cur_max = 0, max_at_i = 0;
            for (int j = i; j > i - k; j--) {
                if (j < 0) break;
                cur_max = max(cur_max, arr[j]);
                int window_size = i - j + 1;
                int cur_sum = cur_max * window_size;
                int sub_sum = (j > 0) ? dp[(j - 1) % k] : 0;
                max_at_i = max(max_at_i, cur_sum + sub_sum);
            }
            dp[i % k] = max_at_i;
        }

        return dp[(n - 1) % k];
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(k)$

> Where $k$ is the maximum length of the subarray and $n$ is the size of the array $arr$.
