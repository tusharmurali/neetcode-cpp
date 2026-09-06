# 410. Split Array Largest Sum

- **Difficulty:** Hard  
- **Pattern:** Binary Search  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/split-array-largest-sum/>  
- **NeetCode:** <https://neetcode.io/problems/split-array-largest-sum>  
- **Video:** <https://www.youtube.com/watch?v=YUF3_eBdzsk>  
- **Video approach:** 5. Binary Search  

[← Back to index](../INDEX.md)

## 1. Recursion

We want to split the array into k subarrays and minimize the maximum sum among them. Using recursion, we try every possible way to form the first subarray, then recursively solve for the remaining elements with k-1 subarrays. For each split point, we track the maximum sum between the current subarray and the best result from the recursive call, then take the minimum across all choices.

```cpp
class Solution {
public:
    int splitArray(vector<int>& nums, int k) {
        int n = nums.size();
        return dfs(nums, 0, k, n);
    }

private:
    int dfs(vector<int>& nums, int i, int m, int n) {
        if (i == n) {
            return m == 0 ? 0 : INT_MAX;
        }
        if (m == 0) {
            return INT_MAX;
        }

        int res = INT_MAX, curSum = 0;
        for (int j = i; j <= n - m; j++) {
            curSum += nums[j];
            res = min(res, max(curSum, dfs(nums, j + 1, m - 1, n)));
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems since we may compute `dfs(i, m)` multiple times with the same parameters. By caching results in a memoization table, we avoid redundant computation. The state is defined by the current index and remaining subarrays to form.

```cpp
class Solution {
    vector<vector<int>> dp;

public:
    int splitArray(vector<int>& nums, int k) {
        int n = nums.size();
        dp.assign(n, vector<int>(k + 1, -1));
        return dfs(nums, 0, k, n);
    }

private:
    int dfs(vector<int>& nums, int i, int m, int n) {
        if (i == n) {
            return m == 0 ? 0 : INT_MAX;
        }
        if (m == 0) {
            return INT_MAX;
        }
        if (dp[i][m] != -1) {
            return dp[i][m];
        }

        int res = INT_MAX, curSum = 0;
        for (int j = i; j <= n - m; j++) {
            curSum += nums[j];
            res = min(res, max(curSum, dfs(nums, j + 1, m - 1, n)));
        }

        return dp[i][m] = res;
    }
};
```

**Complexity**

- Time complexity: $O(k * n ^ 2)$
- Space complexity: $O(k * n)$

> Where $n$ is the size of the array $nums$ and $k$ is the number of sub-arrays to form.

## 3. Dynamic Programming (Bottom-Up)

We can convert the top-down approach to bottom-up by filling the DP table iteratively. We build solutions for smaller subproblems first (fewer subarrays, starting from the end of the array) and use them to solve larger problems. The table `dp[i][m]` represents the minimum largest sum when splitting elements from index `i` to the end into `m` subarrays.

```cpp
class Solution {
public:
    int splitArray(vector<int>& nums, int k) {
        int n = nums.size();
        vector<vector<int>> dp(n + 1, vector<int>(k + 1, INT_MAX));
        dp[n][0] = 0;

        for (int m = 1; m <= k; m++) {
            for (int i = n - 1; i >= 0; i--) {
                int curSum = 0;
                for (int j = i; j < n - m + 1; j++) {
                    curSum += nums[j];
                    dp[i][m] = min(dp[i][m], max(curSum, dp[j + 1][m - 1]));
                }
            }
        }

        return dp[0][k];
    }
};
```

**Complexity**

- Time complexity: $O(k * n ^ 2)$
- Space complexity: $O(k * n)$

> Where $n$ is the size of the array $nums$ and $k$ is the number of sub-arrays to form.

## 4. Dynamic Programming (Space Optimized)

In the bottom-up approach, computing `dp[i][m]` only depends on values from `dp[...][m-1]`. We can reduce space from O(k \* n) to O(n) by using two 1D arrays: one for the previous layer and one for the current layer, swapping them after each iteration.

```cpp
class Solution {
public:
    int splitArray(vector<int>& nums, int k) {
        int n = nums.size();
        vector<int> dp(n + 1, INT_MAX), nextDp(n + 1, INT_MAX);
        dp[n] = 0;

        for (int m = 1; m <= k; m++) {
            fill(nextDp.begin(), nextDp.end(), INT_MAX);
            for (int i = n - 1; i >= 0; i--) {
                int curSum = 0;
                for (int j = i; j < n - m + 1; j++) {
                    curSum += nums[j];
                    nextDp[i] = min(nextDp[i], max(curSum, dp[j + 1]));
                }
            }
            dp.swap(nextDp);
        }

        return dp[0];
    }
};
```

**Complexity**

- Time complexity: $O(k * n ^ 2)$
- Space complexity: $O(n)$

> Where $n$ is the size of the array $nums$ and $k$ is the number of sub-arrays to form.

## 5. Binary Search ▶ video

Instead of trying all possible splits, we binary search on the answer itself. The minimum possible largest sum is the maximum element (when k equals n), and the maximum is the total sum (when k equals 1). For a given target sum, we greedily check if we can split the array into at most k subarrays where no subarray exceeds the target. If possible, we try a smaller target; otherwise, we need a larger one.

```cpp
class Solution {
public:
    int splitArray(vector<int>& nums, int k) {
        int l = *max_element(nums.begin(), nums.end());
        int r = accumulate(nums.begin(), nums.end(), 0);
        int res = r;

        while (l <= r) {
            int mid = l + (r - l) / 2;
            if (canSplit(nums, k, mid)) {
                res = mid;
                r = mid - 1;
            } else {
                l = mid + 1;
            }
        }
        return res;
    }

private:
    bool canSplit(vector<int>& nums, int k, int largest) {
        int subarray = 1, curSum = 0;
        for (int num : nums) {
            curSum += num;
            if (curSum > largest) {
                subarray++;
                if (subarray > k) return 0;
                curSum = num;
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n \log s)$
- Space complexity: $O(1)$

> Where $n$ is the size of the array $nums$ and $s$ is the sum of all the elements in the array.

## 6. Binary Search + Prefix Sum

We can optimize the feasibility check using prefix sums and binary search. Instead of linearly scanning to find where each subarray should end, we use binary search on the prefix sum array to find the farthest index where the subarray sum stays within the target. This speeds up the check from O(n) to O(k log n) for each candidate.

```cpp
class Solution {
private:
    vector<int> prefix;
    int n;

public:
    int splitArray(vector<int>& nums, int k) {
        n = nums.size();
        prefix.resize(n + 1, 0);
        for (int i = 0; i < n; ++i) {
            prefix[i + 1] = prefix[i] + nums[i];
        }

        int l = *max_element(nums.begin(), nums.end());
        int r = accumulate(nums.begin(), nums.end(), 0);
        int res = r;

        while (l <= r) {
            int mid = l + (r - l) / 2;
            if (canSplit(mid, k)) {
                res = mid;
                r = mid - 1;
            } else {
                l = mid + 1;
            }
        }

        return res;
    }

private:
    bool canSplit(int largest, int k) {
        int subarrays = 0, i = 0;
        while (i < n) {
            int l = i + 1, r = n;
            while (l <= r) {
                int mid = l + (r - l) / 2;
                if (prefix[mid] - prefix[i] <= largest) {
                    l = mid + 1;
                } else {
                    r = mid - 1;
                }
            }
            subarrays++;
            i = r;
            if (subarrays > k) {
                return false;
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n + (k * \log n * \log s))$
- Space complexity: $O(n)$

> Where $n$ is the size of the array $nums$, $s$ is the sum of all the elements in the array, and $k$ is the number of sub-arrays to form.
