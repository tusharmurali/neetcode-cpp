# 673. Number of Longest Increasing Subsequence

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-longest-increasing-subsequence/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-longest-increasing-subsequence>  
- **Video:** <https://www.youtube.com/watch?v=Tuc-rjJbsXU>  

[← Back to index](../INDEX.md)

## 1. Recursion

The brute force approach explores every possible increasing subsequence by trying each element as a potential starting point. From each position, we recursively extend the subsequence by considering all future elements that are strictly greater than the current one. As we explore, we track the longest length found so far and count how many subsequences achieve that length. If we find a longer subsequence, we reset the count. If we find another subsequence of the same maximum length, we increment the count.

```cpp
class Solution {
    int LIS = 0;
    int res = 0;

    void dfs(vector<int>& nums, int i, int length) {
        if (LIS < length) {
            LIS = length;
            res = 1;
        } else if (LIS == length) {
            res++;
        }

        for (int j = i + 1; j < nums.size(); j++) {
            if (nums[j] <= nums[i]) {
                continue;
            }
            dfs(nums, j, length + 1);
        }
    }

public:
    int findNumberOfLIS(vector<int>& nums) {
        for (int i = 0; i < nums.size(); i++) {
            dfs(nums, i, 1);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down)

The recursive solution has overlapping subproblems since we repeatedly compute the longest increasing subsequence starting from the same index. By using memoization, we can store the result for each starting position after computing it once. For each index, we store both the length of the longest increasing subsequence starting there and the count of such subsequences. When we revisit an index, we simply return the cached result instead of recomputing.

```cpp
class Solution {
private:
    vector<vector<int>> dp;

    void dfs(vector<int>& nums, int i) {
        if (dp[i][0] != -1) return;

        int maxLen = 1, maxCnt = 1;
        for (int j = i + 1; j < nums.size(); j++) {
            if (nums[j] > nums[i]) {
                dfs(nums, j);
                int length = dp[j][0];
                int count = dp[j][1];
                if (1 + length > maxLen) {
                    maxLen = 1 + length;
                    maxCnt = count;
                } else if (1 + length == maxLen) {
                    maxCnt += count;
                }
            }
        }
        dp[i] = {maxLen, maxCnt};
    }

public:
    int findNumberOfLIS(vector<int>& nums) {
        int n = nums.size();
        dp.assign(n, vector<int>(2, -1));

        int lenLIS = 0, res = 0;
        for (int i = 0; i < n; i++) {
            dfs(nums, i);
            int maxLen = dp[i][0];
            int maxCnt = dp[i][1];
            if (maxLen > lenLIS) {
                lenLIS = maxLen;
                res = maxCnt;
            } else if (maxLen == lenLIS) {
                res += maxCnt;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 3. Dynamic Programming (Bottom-Up)

Instead of using recursion with memoization, we can iterate through the array in reverse order and build up the solution. For each position, we look at all positions to its right and determine the longest increasing subsequence that can be formed starting from the current position. This approach naturally ensures that when we process position `i`, all positions `j > i` have already been computed, giving us the information we need.

```cpp
class Solution {
public:
    int findNumberOfLIS(vector<int>& nums) {
        int n = nums.size();
        vector<vector<int>> dp(n, vector<int>(2, 0));
        int lenLIS = 0, res = 0;

        for (int i = n - 1; i >= 0; i--) {
            int maxLen = 1, maxCnt = 1;
            for (int j = i + 1; j < n; j++) {
                if (nums[j] > nums[i]) {
                    int length = dp[j][0];
                    int count = dp[j][1];
                    if (length + 1 > maxLen) {
                        maxLen = length + 1;
                        maxCnt = count;
                    } else if (length + 1 == maxLen) {
                        maxCnt += count;
                    }
                }
            }

            if (maxLen > lenLIS) {
                lenLIS = maxLen;
                res = maxCnt;
            } else if (maxLen == lenLIS) {
                res += maxCnt;
            }
            dp[i][0] = maxLen;
            dp[i][1] = maxCnt;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Binary Search + Prefix Sum)

The `O(n^2)` DP solution can be optimized by using binary search and prefix sums. The key insight is to organize elements by the length of the longest increasing subsequence ending at them. For each length, we maintain a list of elements sorted in decreasing order along with cumulative counts. When processing a new element, we use binary search to find where it fits and to count how many subsequences of the previous length can be extended by this element.

```cpp
class Solution {
public:
    int findNumberOfLIS(vector<int>& nums) {
        vector<vector<pair<int, int>>> dp = {{{0, 0}, {nums[0], 1}}};
        int LIS = 1;

        for (int i = 1; i < nums.size(); i++) {
            int num = nums[i];
            if (num > dp.back().back().first) {
                int count = bs2(dp, LIS - 1, num);
                dp.push_back({{0, 0}, {num, count}});
                LIS++;
            } else {
                int j = bs1(dp, num);
                int count = bs2(dp, j - 1, num);
                dp[j].push_back({num, dp[j].back().second + count});
            }
        }

        return dp.back().back().second;
    }

private:
    int bs1(vector<vector<pair<int, int>>>& dp, int num) {
        int l = 0, r = dp.size() - 1, j = dp.size() - 1;
        while (l <= r) {
            int mid = (l + r) / 2;
            if (dp[mid].back().first < num) {
                l = mid + 1;
            } else {
                j = mid;
                r = mid - 1;
            }
        }
        return j;
    }

    int bs2(vector<vector<pair<int, int>>>& dp, int i, int num) {
        if (i < 0) return 1;
        int l = 1, r = dp[i].size() - 1, j = 0;
        while (l <= r) {
            int mid = (l + r) / 2;
            if (dp[i][mid].first >= num) {
                j = mid;
                l = mid + 1;
            } else {
                r = mid - 1;
            }
        }
        return dp[i].back().second - dp[i][j].second;
    }
};
```

**Complexity**

- Time complexity: $O(n\log n)$
- Space complexity: $O(n)$
