# 2616. Minimize the Maximum Difference of Pairs

- **Difficulty:** Medium  
- **Pattern:** Binary Search  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimize-the-maximum-difference-of-pairs/>  
- **NeetCode:** <https://neetcode.io/problems/minimize-the-maximum-difference-of-pairs>  
- **Video:** <https://www.youtube.com/watch?v=lf1Pxg7IrzQ>  

[← Back to index](../INDEX.md)

## 1. Greedy + Dynamic Programming (Top-Down)

To minimize the maximum difference among `p` pairs, we first sort the array. After sorting, optimal pairs are always adjacent elements because non-adjacent pairs would have larger differences. The problem becomes selecting `p` non-overlapping adjacent pairs to minimize the largest difference.

This is a classic DP problem: at each position, we decide whether to pair the current element with the next one (taking them both) or skip the current element. The goal is to minimize the maximum difference among all selected pairs.

```cpp
class Solution {
    unordered_map<long long, int> dp;

public:
    int minimizeMax(vector<int>& nums, int p) {
        int n = nums.size();
        sort(nums.begin(), nums.end());
        return dfs(0, 0, nums, p);
    }

private:
    int dfs(int i, int pairs, vector<int>& nums, int p) {
        if (pairs == p) return 0;
        if (i >= nums.size() - 1) return INT_MAX;
        long long key = i;
        key = (key << 31) | pairs;
        if (dp.count(key)) return dp[key];

        int take = max(nums[i + 1] - nums[i], dfs(i + 2, pairs + 1, nums, p));
        int skip = dfs(i + 1, pairs, nums, p);

        return dp[key] = min(take, skip);
    }
};
```

**Complexity**

- Time complexity: $O(n * p)$
- Space complexity: $O(n * p)$

> Where $n$ is the size of the input array and $p$ is the number of pairs to select.

## 2. Greedy + Dynamic Programming (Bottom-Up)

The same logic as the top-down approach, but we fill the DP table iteratively from the end of the array backward. At each position and pair count, we compute the minimum maximum difference achievable.

```cpp
class Solution {
public:
    int minimizeMax(vector<int>& nums, int p) {
        int n = nums.size();
        sort(nums.begin(), nums.end());

        vector<vector<int>> dp(n + 1, vector<int>(p + 1, INT_MAX));
        for (int i = 0; i <= n; i++) {
            dp[i][0] = 0;
        }

        for (int i = n - 2; i >= 0; i--) {
            for (int pairs = 1; pairs <= p; pairs++) {
                int take = INT_MAX;
                if (i + 1 < n) {
                    take = max(nums[i + 1] - nums[i], dp[i + 2][pairs - 1]);
                }
                int skip = dp[i + 1][pairs];
                dp[i][pairs] = min(take, skip);
            }
        }

        return dp[0][p];
    }
};
```

**Complexity**

- Time complexity: $O(n * p)$
- Space complexity: $O(n * p)$

> Where $n$ is the size of the input array and $p$ is the number of pairs to select.

## 3. Greedy + Dynamic Programming (Space Optimized)

Since each row of the DP table only depends on the next two rows, we can reduce space by keeping only three 1D arrays instead of the full 2D table. We rotate these arrays as we iterate backward through the array.

```cpp
class Solution {
public:
    int minimizeMax(vector<int>& nums, int p) {
        int n = nums.size();
        sort(nums.begin(), nums.end());

        vector<int> dp(p + 1, INT_MAX);
        vector<int> dp1(p + 1, INT_MAX);
        vector<int> dp2(p + 1, INT_MAX);

        dp[0] = dp1[0] = dp2[0] = 0;

        for (int i = n - 1; i >= 0; i--) {
            for (int pairs = 1; pairs <= p; pairs++) {
                int take = INT_MAX;
                if (i + 1 < n) {
                    take = max(nums[i + 1] - nums[i], dp2[pairs - 1]);
                }
                int skip = dp1[pairs];
                dp[pairs] = min(take, skip);
            }
            dp2 = dp1;
            dp1 = dp;
            fill(dp.begin(), dp.end(), INT_MAX);
            dp[0] = 0;
        }

        return dp1[p];
    }
};
```

**Complexity**

- Time complexity: $O(n * p)$
- Space complexity: $O(p)$

> Where $n$ is the size of the input array and $p$ is the number of pairs to select.

## 4. Greedy + Binary Search

Instead of DP, we can binary search on the answer. Given a threshold `t`, we greedily check if we can form `p` pairs where each pair has difference at most `t`. After sorting, we scan left to right: whenever two adjacent elements have difference at most `t`, we pair them and skip both. This greedy approach works because pairing earlier elements never blocks better options later.

The answer lies between 0 and `max - min` of the sorted array, so we binary search to find the smallest threshold that allows forming `p` pairs.

```cpp
class Solution {
public:
    int minimizeMax(vector<int>& nums, int p) {
        if (p == 0) return 0;

        sort(nums.begin(), nums.end());
        int left = 0, right = nums.back() - nums[0];
        int result = right;

        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (isValid(nums, mid, p)) {
                result = mid;
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        }

        return result;
    }

private:
    bool isValid(vector<int>& nums, int threshold, int p) {
        int i = 0, count = 0;
        while (i < nums.size() - 1) {
            if (abs(nums[i] - nums[i + 1]) <= threshold) {
                count++;
                i += 2;
            } else {
                i++;
            }
            if (count == p) return true;
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n\log n + n\log m)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

> Where $n$ is the size of the input array and $m$ is the maximum value in the array.
