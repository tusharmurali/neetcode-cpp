# 368. Largest Divisible Subset

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/largest-divisible-subset/>  
- **NeetCode:** <https://neetcode.io/problems/largest-divisible-subset>  
- **Video:** <https://www.youtube.com/watch?v=LeRU6irRoW0>  

[← Back to index](../INDEX.md)

## 1. Dynamic Programming (Top-Down)

A divisible subset has a special property: if we sort the numbers, then for any pair in the subset, the larger number must be divisible by the smaller one. This means if we sort the array and pick elements in order, we only need to check divisibility with the most recently picked element. We can use recursion with memoization to try including or skipping each number.

```cpp
class Solution {
private:
    vector<vector<vector<int>>> cache;

public:
    vector<int> largestDivisibleSubset(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        cache = vector<vector<vector<int>>>(n, vector<vector<int>>(n + 1));
        return dfs(0, -1, nums);
    }

    vector<int> dfs(int i, int prevIndex, vector<int>& nums) {
        if (i == nums.size()) return {};
        if (!cache[i][prevIndex + 1].empty()) return cache[i][prevIndex + 1];

        vector<int> res = dfs(i + 1, prevIndex, nums);

        if (prevIndex == -1 || nums[i] % nums[prevIndex] == 0) {
            vector<int> tmp = {nums[i]};
            vector<int> next = dfs(i + 1, i, nums);
            tmp.insert(tmp.end(), next.begin(), next.end());
            if (tmp.size() > res.size()) res = tmp;
        }

        return cache[i][prevIndex + 1] = res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 2. Dynamic Programming (Top-Down) Space Optimized

We can simplify the state by observing that we only need to track the starting index, not the previous index. For each starting position, we find the longest divisible subset that begins there. When building the subset from index `i`, we look at all later indices `j` where `nums[j]` is divisible by `nums[i]` and take the best result.

```cpp
class Solution {
private:
    vector<vector<int>> cache;

public:
    vector<int> largestDivisibleSubset(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        cache.resize(n, vector<int>());

        vector<int> res;
        for (int i = 0; i < n; i++) {
            vector<int> tmp = dfs(i, nums);
            if (tmp.size() > res.size()) {
                res = tmp;
            }
        }
        return res;
    }

    vector<int> dfs(int i, vector<int>& nums) {
        if (!cache[i].empty()) return cache[i];

        vector<int> res = {nums[i]};
        for (int j = i + 1; j < nums.size(); j++) {
            if (nums[j] % nums[i] == 0) {
                vector<int> tmp = {nums[i]};
                vector<int> next = dfs(j, nums);
                tmp.insert(tmp.end(), next.begin(), next.end());

                if (tmp.size() > res.size()) {
                    res = tmp;
                }
            }
        }
        return cache[i] = res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

We can convert the top-down approach to bottom-up. Processing from right to left, for each index we compute the longest divisible subset starting from that position. At each step, we check all later indices for valid extensions and build upon the precomputed results.

```cpp
class Solution {
public:
    vector<int> largestDivisibleSubset(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        vector<vector<int>> dp(n);
        vector<int> res;

        for (int i = n - 1; i >= 0; i--) {
            dp[i].push_back(nums[i]);

            for (int j = i + 1; j < n; j++) {
                if (nums[j] % nums[i] == 0) {
                    vector<int> tmp = dp[j];
                    tmp.insert(tmp.begin(), nums[i]);

                    if (tmp.size() > dp[i].size()) {
                        dp[i] = tmp;
                    }
                }
            }
            if (dp[i].size() > res.size()) {
                res = dp[i];
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Top-Down) + Tracing

Instead of storing entire subsets in the DP table (which uses extra memory), we can store just two values per index: the length of the longest subset starting there, and the next index in that subset. After computing all lengths, we trace through the indices to reconstruct the actual subset.

```cpp
class Solution {
    vector<vector<int>> dp;

public:
    vector<int> largestDivisibleSubset(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        dp.assign(n, vector<int>(2, -1));

        int maxLen = 1, startIndex = 0;
        for (int i = 0; i < n; i++) {
            if (dfs(i, nums) > maxLen) {
                maxLen = dp[i][0];
                startIndex = i;
            }
        }

        vector<int> subset;
        while (startIndex != -1) {
            subset.push_back(nums[startIndex]);
            startIndex = dp[startIndex][1];
        }
        return subset;
    }

private:
    int dfs(int i, vector<int>& nums) {
        if (dp[i][0] != -1) return dp[i][0];

        dp[i][0] = 1;
        for (int j = i + 1; j < nums.size(); j++) {
            if (nums[j] % nums[i] == 0) {
                int length = dfs(j, nums) + 1;
                if (length > dp[i][0]) {
                    dp[i][0] = length;
                    dp[i][1] = j;
                }
            }
        }
        return dp[i][0];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 5. Dynamic Programming (Bottom-Up) + Tracing

This is the iterative version of the tracing approach. We process indices from left to right, looking backward for valid predecessors. For each position, we store the length of the longest subset ending there and a pointer to the previous index. This is similar to the classic Longest Increasing Subsequence pattern.

```cpp
class Solution {
public:
    vector<int> largestDivisibleSubset(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        vector<vector<int>> dp(n, vector<int>(2, -1)); // dp[i] = {maxLen, prevIdx}

        int maxLen = 1, startIndex = 0;
        for (int i = 0; i < n; i++) {
            dp[i][0] = 1;
            dp[i][1] = -1;
            for (int j = 0; j < i; j++) {
                if (nums[i] % nums[j] == 0 && dp[j][0] + 1 > dp[i][0]) {
                    dp[i][0] = dp[j][0] + 1;
                    dp[i][1] = j;
                }
            }

            if (dp[i][0] > maxLen) {
                maxLen = dp[i][0];
                startIndex = i;
            }
        }

        vector<int> subset;
        while (startIndex != -1) {
            subset.push_back(nums[startIndex]);
            startIndex = dp[startIndex][1];
        }
        return subset;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$
