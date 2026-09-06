# 930. Binary Subarrays with Sum

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/binary-subarrays-with-sum/>  
- **NeetCode:** <https://neetcode.io/problems/binary-subarrays-with-sum>  
- **Video:** <https://www.youtube.com/watch?v=j4JDr4-jvo4>  
- **Video approach:** 4. Sliding Window (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach is to check every possible subarray. For each starting index, we extend the subarray one element at a time, keeping track of the running sum. Whenever the sum equals the goal, we count it. Since the array contains only 0s and 1s, the sum can only increase as we extend the subarray.

```cpp
class Solution {
public:
    int numSubarraysWithSum(vector<int>& nums, int goal) {
        int n = nums.size(), res = 0;

        for (int i = 0; i < n; i++) {
            int curSum = 0;
            for (int j = i; j < n; j++) {
                curSum += nums[j];
                if (curSum == goal) {
                    res++;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Prefix Sum + Hash Map

For a subarray from index `i+1` to `j` to have sum equal to `goal`, we need `prefixSum[j] - prefixSum[i] = goal`, which means `prefixSum[i] = prefixSum[j] - goal`. As we iterate through the array computing prefix sums, we can use a hash map to count how many times each prefix sum has occurred. For each position, we check how many previous positions had a prefix sum that would give us our target subarray sum.

```cpp
class Solution {
public:
    int numSubarraysWithSum(vector<int>& nums, int goal) {
        int prefixSum = 0, res = 0;
        unordered_map<int, int> count;
        count[0] = 1;

        for (int& num : nums) {
            prefixSum += num;
            res += count[prefixSum - goal];
            count[prefixSum]++;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Prefix Sum + Array

Since the array contains only `0`s and `1`s, the prefix sum at any position is at most `n` (the array length). This allows us to use an array instead of a hash map for counting prefix sums. Array access is faster than hash map operations, making this approach more efficient in practice. The logic remains the same as the hash map approach.

```cpp
class Solution {
public:
    int numSubarraysWithSum(vector<int>& nums, int goal) {
        int n = nums.size(), prefixSum = 0, res = 0;
        vector<int> count(n + 1, 0);
        count[0] = 1;

        for (int num : nums) {
            prefixSum += num;
            if (prefixSum >= goal) {
                res += count[prefixSum - goal];
            }
            count[prefixSum]++;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Sliding Window ▶ video

Counting subarrays with exactly `goal` sum is tricky with a sliding window because shrinking the window might skip valid subarrays. However, counting subarrays with sum at most `goal` is straightforward. We can use the identity: `count(exactly goal) = count(at most goal) - count(at most goal-1)`. For each right endpoint, we shrink the left side until the sum is at most the target, and all subarrays ending at `right` with starting points from `left` to `right` are valid.

```cpp
class Solution {
public:
    int numSubarraysWithSum(vector<int>& nums, int goal) {
        return helper(nums, goal) - helper(nums, goal - 1);
    }

private:
    int helper(vector<int>& nums, int x) {
        if (x < 0) return 0;
        int res = 0, l = 0, cur = 0;
        for (int r = 0; r < nums.size(); r++) {
            cur += nums[r];
            while (cur > x) {
                cur -= nums[l];
                l++;
            }
            res += (r - l + 1);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
