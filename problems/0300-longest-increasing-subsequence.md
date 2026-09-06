# 300. Longest Increasing Subsequence

- **Difficulty:** Medium  
- **Pattern:** 1-D Dynamic Programming  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/longest-increasing-subsequence/>  
- **NeetCode:** <https://neetcode.io/problems/longest-increasing-subsequence>  
- **Video:** <https://www.youtube.com/watch?v=cjWnW0hdF1Y>  
- **Video approach:** 5. Dynamic Programming (Bottom-Up) - II  

[← Back to index](../INDEX.md)

## 1. Recursion

To find the longest increasing subsequence, we consider each element and decide whether to include it. We can only include an element if it's larger than the previous one in our subsequence. This gives us two choices at each step: skip the current element or include it (if valid). We explore all possibilities recursively and return the maximum length found.

```cpp
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        return dfs(nums, 0, -1);
    }

private:
    int dfs(vector<int>& nums, int i, int j) {
        if (i == nums.size()) {
            return 0;
        }

        int LIS = dfs(nums, i + 1, j); // not include

        if (j == -1 || nums[j] < nums[i]) {
            LIS = max(LIS, 1 + dfs(nums, i + 1, i)); // include
        }

        return LIS;
    }
};
```

**Complexity**

- Time complexity: $O(2 ^ n)$
- Space complexity: $O(n)$

## 2. Dynamic Programming (Top-Down) - I

The recursive solution revisits the same `(i, j)` pairs multiple times. We can memoize results using a 2D table indexed by current position and the last included index. Since `j` can range from `-1` to `n-1`, we offset by 1 when indexing the memo table.

```cpp
class Solution {
public:
    vector<vector<int>> memo;

    int dfs(int i, int j, vector<int>& nums) {
        if (i == nums.size()) {
            return 0;
        }
        if (memo[i][j + 1] != -1) {
            return memo[i][j + 1];
        }

        int LIS = dfs(i + 1, j, nums);

        if (j == -1 || nums[j] < nums[i]) {
            LIS = max(LIS, 1 + dfs(i + 1, i, nums));
        }

        memo[i][j + 1] = LIS;
        return LIS;
    }

    int lengthOfLIS(vector<int>& nums) {
        int n = nums.size();
        memo = vector<vector<int>>(n, vector<int>(n + 1, -1));
        return dfs(0, -1, nums);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Dynamic Programming (Top-Down) - II

Instead of tracking both current index and last included index, we can define `dfs(i)` as the length of the longest increasing subsequence starting at index `i`. For each starting position, we look at all positions `j > i` where `nums[j] > nums[i]` and take the maximum. This reduces the state to just one dimension.

```cpp
class Solution {
private:
    vector<int> memo;

    int dfs(vector<int>& nums, int i) {
        if (memo[i] != -1) {
            return memo[i];
        }

        int LIS = 1;
        for (int j = i + 1; j < nums.size(); j++) {
            if (nums[i] < nums[j]) {
                LIS = max(LIS, 1 + dfs(nums, j));
            }
        }

        return memo[i] = LIS;
    }

public:
    int lengthOfLIS(vector<int>& nums) {
        int n = nums.size();
        memo.assign(n, -1);

        int maxLIS = 1;
        for (int i = 0; i < n; i++) {
            maxLIS = max(maxLIS, dfs(nums, i));
        }
        return maxLIS;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 4. Dynamic Programming (Bottom-Up) - I

This is the iterative version of the two-dimensional memoization approach. We fill a 2D table `dp[i][j]` from right to left. The value represents the longest increasing subsequence considering elements from index `i` onward, given that the last included element was at index `j` (or no element if `j == -1`).

```cpp
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        int n = nums.size();
        vector<vector<int>> dp(n + 1, vector<int>(n + 1, 0));

        for (int i = n - 1; i >= 0; --i) {
            for (int j = i - 1; j >= -1; --j) {
                int LIS = dp[i + 1][j + 1]; // Not including nums[i]

                if (j == -1 || nums[j] < nums[i]) {
                    LIS = max(LIS, 1 + dp[i + 1][i + 1]); // Including nums[i]
                }

                dp[i][j + 1] = LIS;
            }
        }

        return dp[0][0];
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 5. Dynamic Programming (Bottom-Up) - II ▶ video

A simpler 1D approach: let `LIS[i]` be the length of the longest increasing subsequence starting at index `i`. Working from right to left, for each `i`, we check all `j > i`. If `nums[i] < nums[j]`, we can extend the subsequence starting at `j`. We take the maximum extension and add 1 for the current element.

```cpp
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        vector<int> LIS(nums.size(), 1);

        for (int i = nums.size() - 1; i >= 0; i--) {
            for (int j = i + 1; j < nums.size(); j++) {
                if (nums[i] < nums[j]) {
                    LIS[i] = max(LIS[i], 1 + LIS[j]);
                }
            }
        }
        return *max_element(LIS.begin(), LIS.end());
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 6. Segment Tree

We can use a segment tree to efficiently query the maximum LIS length among all elements smaller than the current one. First, we compress the values to indices. Then, for each element, we query the segment tree for the maximum LIS among all values less than the current value, add 1, and update the segment tree at the current value's position.

```cpp
class SegmentTree {
public:
    int n;
    vector<int> tree;

    SegmentTree(int N) {
        n = N;
        while (n & (n - 1)) {
            n++;
        }
        tree.resize(2 * n);
    }

    void update(int i, int val) {
        tree[n + i] = val;
        int j = (n + i) >> 1;
        while (j >= 1) {
            tree[j] = max(tree[j << 1], tree[j << 1 | 1]);
            j >>= 1;
        }
    }

    int query(int l, int r) {
        if (l > r) {
            return 0;
        }
        int res = INT_MIN;
        l += n;
        r += n + 1;
        while (l < r) {
            if (l & 1) {
                res = max(res, tree[l]);
                l++;
            }
            if (r & 1) {
                r--;
                res = max(res, tree[r]);
            }
            l >>= 1;
            r >>= 1;
        }
        return res;
    }
};

class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        vector<int> sortedArr = nums;
        sort(sortedArr.begin(), sortedArr.end());
        sortedArr.erase(unique(sortedArr.begin(),
                        sortedArr.end()), sortedArr.end());

        vector<int> order(nums.size());
        for (int i = 0; i < nums.size(); i++) {
            order[i] = lower_bound(sortedArr.begin(), sortedArr.end(),
                                   nums[i]) - sortedArr.begin();
        }

        int n = sortedArr.size();
        SegmentTree segTree(n);

        int LIS = 0;
        for (int num : order) {
            int curLIS = segTree.query(0, num - 1) + 1;
            segTree.update(num, curLIS);
            LIS = max(LIS, curLIS);
        }
        return LIS;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 7. Dynamic Programming + Binary Search

We maintain an array `dp` where `dp[i]` is the smallest ending element of all increasing subsequences of length `i + 1`. This array stays sorted. For each new element, if it's larger than the last element in `dp`, it extends the longest subsequence. Otherwise, we use binary search to find the position where it can replace an element, keeping the array optimal for future extensions.

```cpp
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        vector<int> dp;
        dp.push_back(nums[0]);

        int LIS = 1;
        for (int i = 1; i < nums.size(); i++) {
            if (dp.back() < nums[i]) {
                dp.push_back(nums[i]);
                LIS++;
                continue;
            }

            int idx = lower_bound(dp.begin(),
                                  dp.end(), nums[i]) - dp.begin();
            dp[idx] = nums[i];
        }

        return LIS;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0300-longest-increasing-subsequence.cpp` in the NeetCode repo)

```cpp
/*
    Given int array, return length of longest increasing subsequence
    Ex. nums = [10,9,2,5,3,7,101,18] -> 4, [2,3,7,101]

    Why DP? 1) Max/min of smth, 2) make decisions based on prev decisions
    "Decision": is it worth it to consider this number?
    If use may contribute to better LIS, but may also eliminate an even better LIS

    Framework to solve DP:
    1) Need some function or array that represents ans to the problem (dp array)
    2) Way to transition b/w states (recurrence relation), depends on question
    3) Need a base case (initial solution for every subproblem)

    Recurrence relation: dp[i] = max(dp[j] + 1)
    Base case: dp[i] = 1, since every element on its own has an LIS of 1

    Time: O(n^2)
    Space: O(n)
*/

class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        int n = nums.size();
        vector<int> dp(n, 1);
        
        int result = 1;
        
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (nums[j] < nums[i]) {
                    dp[i] = max(dp[i], dp[j] + 1);
                }
            }
            result = max(result, dp[i]);
        }
        
        return result;
    }
};
```
