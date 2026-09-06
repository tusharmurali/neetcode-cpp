# 698. Partition to K Equal Sum Subsets

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/partition-to-k-equal-sum-subsets/>  
- **NeetCode:** <https://neetcode.io/problems/partition-to-k-equal-sum-subsets>  
- **Video:** <https://www.youtube.com/watch?v=mBk4I0X46oI>  
- **Video approach:** 1. Backtracking  

[← Back to index](../INDEX.md)

## 1. Backtracking ▶ video

The problem asks whether we can divide the array into exactly `k` subsets, each with the same sum. First, we check if the total sum is divisible by `k`. If not, it's impossible. Otherwise, each subset must sum to `target = total / k`.

We use backtracking to try placing each number into one of the `k` subsets. Sorting the array in descending order helps us fail faster when a large number cannot fit. Once a subset reaches the target sum, we start building the next one. If we successfully build all `k` subsets, we return `true`.

```cpp
class Solution {
    vector<bool> used;
    int target;

public:
    bool canPartitionKSubsets(vector<int>& nums, int k) {
        int sum = accumulate(nums.begin(), nums.end(), 0);
        if (sum % k != 0) return false;

        target = sum / k;
        sort(nums.rbegin(), nums.rend());
        used.assign(nums.size(), false);
        return backtrack(nums, k, 0, 0);
    }

private:
    bool backtrack(vector<int>& nums, int k, int currentSum, int start) {
        if (k == 0) return true;
        if (currentSum == target) return backtrack(nums, k - 1, 0, 0);

        for (int i = start; i < nums.size(); i++) {
            if (used[i] || currentSum + nums[i] > target) continue;
            used[i] = true;
            if (backtrack(nums, k, currentSum + nums[i], i + 1)) return true;
            used[i] = false;
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(k * 2 ^ n)$
- Space complexity: $O(n)$

> Where $n$ is the size of the array $nums$ and $k$ is the number of subsets.

## 2. Backtracking (Pruning)

This approach extends the basic backtracking by adding a key pruning optimization. If we fail to place any element into an empty subset (when `subsetSum == 0`), we know that element cannot be placed anywhere, so the entire configuration is invalid. This avoids redundant exploration of branches that will never succeed.

```cpp
class Solution {
    vector<bool> used;
    int target;

public:
    bool canPartitionKSubsets(vector<int>& nums, int k) {
        int sum = accumulate(nums.begin(), nums.end(), 0);
        if (sum % k != 0) return false;

        target = sum / k;
        sort(nums.rbegin(), nums.rend());
        used.assign(nums.size(), false);
        return backtrack(nums, k, 0, 0);
    }

private:
    bool backtrack(vector<int>& nums, int k, int currentSum, int start) {
        if (k == 0) return true;
        if (currentSum == target) return backtrack(nums, k - 1, 0, 0);

        for (int i = start; i < nums.size(); i++) {
            if (used[i] || currentSum + nums[i] > target) continue;
            used[i] = true;
            if (backtrack(nums, k, currentSum + nums[i], i + 1)) return true;
            used[i] = false;
            if (currentSum == 0) {  // Pruning
                return false;
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(k * 2 ^ n)$
- Space complexity: $O(n)$

> Where $n$ is the size of the array $nums$ and $k$ is the number of subsets.

## 3. Backtracking (Bit Mask + Pruning)

Instead of using a boolean array to track used elements, we can represent the state as a bitmask. Each bit indicates whether the corresponding element has been used. This representation is more compact and prepares us for memoization in later approaches.

```cpp
class Solution {
    int target, n;

public:
    bool canPartitionKSubsets(vector<int>& nums, int k) {
        int total = accumulate(nums.begin(), nums.end(), 0);
        if (total % k != 0) return false;

        target = total / k;
        n = nums.size();
        sort(nums.rbegin(), nums.rend());
        return backtrack(nums, 0, k, 0, (1 << n) - 1);
    }

private:
    bool backtrack(vector<int>& nums, int i, int k, int subsetSum, int mask) {
        if (k == 0) return true;
        if (subsetSum == target) return backtrack(nums, 0, k - 1, 0, mask);
        for (int j = i; j < nums.size(); j++) {
            if ((mask & (1 << j)) == 0 || subsetSum + nums[j] > target) continue;
            if (backtrack(nums, j + 1, k, subsetSum + nums[j], mask ^ (1 << j))) {
                return true;
            }
            if (subsetSum == 0) return false;
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(k * 2 ^ n)$
- Space complexity:
    - $O(1)$ or $O(n)$ space depending on the sorting algorithm.
    - $O(n)$ for the recursion stack.

> Where $n$ is the size of the array $nums$ and $k$ is the number of subsets.

## 4. Dynamic Programming (Top-Down) + Bit Mask

The bitmask from the previous approach naturally lends itself to memoization. Different orderings of element selection can lead to the same `mask`, so we cache results for each `mask` to avoid recomputation. This transforms the exponential backtracking into a more efficient dynamic programming solution.

```cpp
class Solution {
    int target, n;
    vector<int> dp;

public:
    bool canPartitionKSubsets(vector<int>& nums, int k) {
        int total = accumulate(nums.begin(), nums.end(), 0);
        if (total % k != 0) return false;

        target = total / k;
        n = nums.size();
        dp.assign(1 << n, -1);
        sort(nums.rbegin(), nums.rend());
        return backtrack(nums, 0, k, 0, (1 << n) - 1);
    }

private:
    int backtrack(vector<int>& nums, int i, int k, int subsetSum, int mask) {
        if (dp[mask] != -1) return dp[mask];
        if (k == 0) {
            dp[mask] = 1;
            return 1;
        }
        if (subsetSum == target) {
            dp[mask] = backtrack(nums, 0, k - 1, 0, mask);
            return dp[mask];
        }
        for (int j = i; j < nums.size(); j++) {
            if ((mask & (1 << j)) == 0 || subsetSum + nums[j] > target) continue;
            if (backtrack(nums, j + 1, k, subsetSum + nums[j], mask ^ (1 << j))) {
                dp[mask] = 1;
                return 1;
            }
            if (subsetSum == 0) {
                break;
            }
        }
        dp[mask] = 0;
        return 0;
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity: $O(2 ^ n)$

## 5. Dynamic Programming (Bottom-Up) + Bit Mask

Instead of recursion, we iterate through all possible `mask` values from `0` to `2^n - 1`. For each valid state (reachable configuration), we try adding each unused element. The key insight is that `dp[mask]` stores the current sum modulo `target`. If we can reach the full `mask` with sum `0` (meaning all subsets are complete), we have a valid partition.

```cpp
class Solution {
public:
    bool canPartitionKSubsets(vector<int>& nums, int k) {
        int total = accumulate(nums.begin(), nums.end(), 0);
        if (total % k != 0) return false;

        int target = total / k;
        int n = nums.size();
        int N = 1 << n;
        vector<int> dp(N, -1);
        dp[0] = 0;

        for (int mask = 0; mask < N; mask++) {
            if (dp[mask] == -1) continue;
            for (int i = 0; i < n; i++) {
                if ((mask & (1 << i)) == 0 && dp[mask] + nums[i] <= target) {
                    dp[mask | (1 << i)] = (dp[mask] + nums[i]) % target;
                }
            }
        }

        return dp[N - 1] == 0;
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity: $O(2 ^ n)$
