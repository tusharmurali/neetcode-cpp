# 2439. Minimize Maximum of Array

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimize-maximum-of-array/>  
- **NeetCode:** <https://neetcode.io/problems/minimize-maximum-of-array>  
- **Video:** <https://www.youtube.com/watch?v=AeHMvcKuR0Y>  

[← Back to index](../INDEX.md)

## 1. Binary Search

The operation allows us to move value from a position to its left neighbor. This means we can redistribute values leftward but never rightward. The key observation is: for any target maximum value `m`, we can achieve it if and only if the prefix sum up to each index `i` does not exceed `m * (i + 1)`. This is because we can spread the total sum of the first `i+1` elements evenly among those positions.

Since the answer lies between 0 and the maximum element, we can binary search for the smallest valid maximum. For each candidate, we check if the prefix sum constraint holds for all positions.

```cpp
class Solution {
public:
    int minimizeArrayValue(vector<int>& nums) {
        int left = 0, right = *max_element(nums.begin(), nums.end());

        while (left < right) {
            int mid = left + (right - left) / 2;
            if (isValid(nums, mid)) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }

        return left;
    }

private:
    bool isValid(vector<int>& nums, int maxVal) {
        long long prefixSum = 0;
        for (int i = 0; i < nums.size(); i++) {
            prefixSum += nums[i];
            if (prefixSum > (long long)maxVal * (i + 1)) {
                return false;
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n \log m)$
- Space complexity: $O(1)$ extra space.

> Where $n$ is the size of the array $nums$ and $m$ is the maximum value in the array.

## 2. Prefix Sum + Greedy

Building on the prefix sum insight, we can solve this directly without binary search. At each position `i`, the minimum possible maximum considering elements `0` to `i` is the ceiling of `prefixSum / (i + 1)`. This represents the best we can do by spreading the total sum evenly across those positions.

The overall answer is the maximum of these values across all prefixes. We cannot do better than this because each prefix constrains how low the maximum can go, and the tightest constraint determines the answer.

```cpp
class Solution {
public:
    int minimizeArrayValue(vector<int>& nums) {
        int res = nums[0];
        long long total = nums[0];

        for (int i = 1; i < nums.size(); i++) {
            total += nums[i];
            res = max(res, (int)ceil((double)total / (i + 1)));
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
