# 1658. Minimum Operations to Reduce X to Zero

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-operations-to-reduce-x-to-zero/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-operations-to-reduce-x-to-zero>  
- **Video:** <https://www.youtube.com/watch?v=xumn16n7njs>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We can only remove elements from the left or right ends of the array. The total sum we remove must equal `x`. We try every possible combination: take some elements from the left (prefix) and some from the right (suffix), checking if their combined sum equals `x`. For each valid combination, we track the `min` number of elements removed.

```cpp
class Solution {
public:
    int minOperations(vector<int>& nums, int x) {
        int n = nums.size();
        int res = n + 1, suffixSum = 0, prefixSum = 0;

        for (int i = n - 1; i >= 0; i--) {
            suffixSum += nums[i];
            if (suffixSum == x) {
                res = min(res, n - i);
            }
        }

        for (int i = 0; i < n; i++) {
            prefixSum += nums[i];
            suffixSum = 0;
            if (prefixSum == x) {
                res = min(res, i + 1);
            }

            for (int j = n - 1; j > i; j--) {
                suffixSum += nums[j];
                if (prefixSum + suffixSum == x) {
                    res = min(res, i + 1 + n - j);
                }
            }
        }

        return res == n + 1 ? -1 : res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 2. Prefix Sum + Binary Search

Instead of recalculating prefix sums repeatedly, we precompute them. For each `suffixSum` we consider, we need to find a `prefixSum` that equals `x - suffixSum`. Since prefix sums are sorted in increasing order (all elements are positive), we can use binary search to quickly find if such a prefix exists. This eliminates the inner loop from the brute force approach.

```cpp
class Solution {
public:
    int minOperations(vector<int>& nums, int x) {
        int n = nums.size();
        vector<int> prefixSum(n + 1, 0);
        for (int i = 0; i < n; i++) {
            prefixSum[i + 1] = prefixSum[i] + nums[i];
        }

        if (x > prefixSum[n]) {
            return -1;
        }

        auto binarySearch = [&](int target, int m) {
            int l = 1, r = m, index = n + 1;
            while (l <= r) {
                int mid = (l + r) / 2;
                if (prefixSum[mid] >= target) {
                    if (prefixSum[mid] == target) {
                        index = mid;
                    }
                    r = mid - 1;
                } else {
                    l = mid + 1;
                }
            }
            return index;
        };

        int res = binarySearch(x, n);
        int suffixSum = 0;
        for (int i = n - 1; i > 0; i--) {
            suffixSum += nums[i];
            if (suffixSum == x) {
                res = min(res, n - i);
                break;
            }
            if (suffixSum > x) break;
            res = min(res, binarySearch(x - suffixSum, i) + n - i);
        }

        return res == n + 1 ? -1 : res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 3. Prefix Sum + Hash Map

Here is a clever reframing: removing elements from both ends that sum to `x` is the same as keeping a contiguous subarray in the middle that sums to `total - x`. The problem becomes finding the longest subarray with sum equal to `target = total - x`. A hash map storing prefix sums lets us check in `O(1)` whether the required complement exists.

```cpp
class Solution {
public:
    int minOperations(vector<int>& nums, int x) {
        int total = 0;
        for (int& num : nums) total += num;
        if (total == x) return nums.size();

        int target = total - x;
        if (target < 0) return -1;

        unordered_map<int, int> prefixMap;
        prefixMap[0] = -1;
        int prefixSum = 0, res = -1;

        for (int i = 0; i < nums.size(); i++) {
            prefixSum += nums[i];
            if (prefixMap.count(prefixSum - target)) {
                res = max(res, i - prefixMap[prefixSum - target]);
            }
            prefixMap[prefixSum] = i;
        }

        return res == -1 ? -1 : nums.size() - res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Sliding Window

Building on the same insight as the hash map approach, we want the longest subarray summing to `target = total - x`. Since all elements are positive, the subarray sum increases as we expand and decreases as we shrink. This monotonic property allows us to use a sliding window: expand the right boundary to include more elements, and shrink from the left when the sum exceeds the `target`.

```cpp
class Solution {
public:
    int minOperations(vector<int>& nums, int x) {
        int target = accumulate(nums.begin(), nums.end(), 0) - x;
        int curSum = 0, maxWindow = -1, l = 0;

        for (int r = 0; r < nums.size(); r++) {
            curSum += nums[r];

            while (l <= r && curSum > target) {
                curSum -= nums[l];
                l++;
            }

            if (curSum == target) {
                maxWindow = max(maxWindow, r - l + 1);
            }
        }

        return maxWindow == -1 ? -1 : nums.size() - maxWindow;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
