# 446. Arithmetic Slices II

- **Difficulty:** Hard  
- **Pattern:** 2-D Dynamic Programming  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/arithmetic-slices-ii-subsequence/>  
- **NeetCode:** <https://neetcode.io/problems/arithmetic-slices-ii-subsequence>  
- **Video:** <https://www.youtube.com/watch?v=YIMwwT9JdIE>  

[← Back to index](../INDEX.md)

## 1. Brute Force

An arithmetic subsequence has at least 3 elements with a constant difference between consecutive terms. We can try all possible subsequences using recursion, tracking the last two elements to determine the required difference. Once we pick two elements, any future element must continue the same difference.

We use memoization to avoid recomputing the same states. The state includes the current index, the previous index, the difference, and whether we have at least 3 elements.

```cpp
class Solution {
    static const long long INF = 1e15;
    unordered_map<string, int> dp;

    int dfs(vector<int>& nums, int i, int j, long long diff, int flag) {
        if (i == nums.size()) {
            return flag;
        }

        string key = to_string(i) + "," + to_string(j) + "," + to_string(diff) + "," + to_string(flag);
        if (dp.count(key)) {
            return dp[key];
        }

        int res = dfs(nums, i + 1, j, diff, flag);
        if (j == -1) {
            res += dfs(nums, i + 1, i, INF, flag);
        } else {
            if (diff == INF) {
                res += dfs(nums, i + 1, i, nums[i] - 0LL - nums[j], flag);
            } else if (diff == nums[i] - 0LL - nums[j]) {
                res += dfs(nums, i + 1, i, diff, 1);
            }
        }

        dp[key] = res;
        return res;
    }

public:
    int numberOfArithmeticSlices(vector<int>& nums) {
        if (nums.size() < 3) return 0;
        return dfs(nums, 0, -1, INF, 0);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 3)$
- Space complexity: $O(n ^ 3)$

## 2. Dynamic Programming (Bottom-Up)

Instead of recursion, we can build the solution iteratively. For each pair of indices `(i, j)` where `j < i`, we compute the difference and count how many arithmetic subsequences end at index `i` with that difference.

The key insight is that `dp[i][diff]` stores the count of subsequences (of length 2 or more) ending at index `i` with the given difference. When we extend a subsequence from `j` to `i`, we add `dp[j][diff]` to the result because those represent valid 3+ element subsequences.

```cpp
class Solution {
public:
    int numberOfArithmeticSlices(vector<int>& nums) {
        int n = nums.size();
        int res = 0;
        vector<unordered_map<long long, int>> dp(n);

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < i; j++) {
                long long diff = (long long) nums[i] - nums[j];
                int count = dp[j][diff];
                dp[i][diff] += count + 1;
                res += count;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 3. Dynamic Programming (Optimization) - I

The standard DP approach stores counts for all differences at each index. However, we only need to track a difference if it could potentially extend further. If `nums[i] + diff` does not exist in the array, there is no point storing that state since no future element can continue the sequence.

By checking if the next element in the sequence exists before storing, we reduce unnecessary hash map entries and improve practical performance.

```cpp
class Solution {
public:
    int numberOfArithmeticSlices(vector<int>& nums) {
        int res = 0, n = nums.size();
        unordered_set<int> s(nums.begin(), nums.end());
        vector<unordered_map<long long, int>> dp(n);

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < i; j++) {
                long long diff = (long long)nums[i] - nums[j];
                int cnt = dp[j].count(diff) ? dp[j][diff] : 0;
                if (s.count(nums[i] + diff)) {
                    dp[i][diff] += cnt + 1;
                }
                res += cnt;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## 4. Dynamic Programming (Optimization) - II

Instead of using a hash map keyed by difference, we can use a 2D DP array where `dp[i][j]` represents the count of arithmetic subsequences ending at indices `i` and `j`. To extend a subsequence ending at `j`, we need to find an earlier index `k` such that `nums[j] - nums[k] = nums[i] - nums[j]`.

We precompute the indices of each value in a map. For a pair `(j, i)`, we calculate the required previous value as `2 * nums[j] - nums[i]` and look up all indices where this value appears.

```cpp
class Solution {
public:
    int numberOfArithmeticSlices(vector<int>& nums) {
        int res = 0;
        unordered_map<int, vector<int>> mpIdx;
        int n = nums.size();
        vector<vector<int>> dp(n, vector<int>(n, 0));

        for (int i = 0; i < n; i++) {
            mpIdx[nums[i]].push_back(i);
        }

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < i; j++) {
                long prev = 2L * nums[j] - nums[i];
                if (prev < INT_MIN || prev > INT_MAX) continue;

                if (mpIdx.count(prev)) {
                    for (int k : mpIdx[prev]) {
                        if (k >= j) break;
                        dp[i][j] += dp[j][k] + 1;
                    }
                }
                res += dp[i][j];
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$
