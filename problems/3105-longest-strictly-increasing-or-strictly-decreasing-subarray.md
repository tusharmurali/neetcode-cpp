# 3105. Longest Strictly Increasing or Strictly Decreasing Subarray

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/longest-strictly-increasing-or-strictly-decreasing-subarray/>  
- **NeetCode:** <https://neetcode.io/problems/longest-strictly-increasing-or-strictly-decreasing-subarray>  
- **Video:** <https://www.youtube.com/watch?v=zDbApBI7UpE>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The straightforward approach is to check every possible starting position and see how far we can extend a monotonic subarray from there. For each starting index, we determine if the subarray is increasing or decreasing based on the first two elements, then continue as long as the pattern holds.

```cpp
class Solution {
public:
    int longestMonotonicSubarray(vector<int>& nums) {
        int n = nums.size();
        int res = 1;

        for (int i = 0; i < n - 1; i++) {
            int curLen = 1;
            for (int j = i + 1; j < n; j++) {
                if (nums[j] == nums[j - 1] || ((nums[i] < nums[i + 1]) != (nums[j - 1] < nums[j]))) {
                    break;
                }
                curLen++;
            }
            res = max(res, curLen);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Iteration - I

We can solve this in a single pass by tracking the current monotonic subarray's length and direction. As we scan through the array, we check if the current element continues the same pattern (increasing or decreasing). If it does, we extend the current subarray. If not, we start a new subarray with the current pair of elements.

```cpp
class Solution {
public:
    int longestMonotonicSubarray(vector<int>& nums) {
        int cur = 1;
        int res = 1;
        int increasing = 0;

        for (int i = 1; i < nums.size(); i++) {
            if (nums[i - 1] < nums[i]) {
                if (increasing > 0) {
                    cur++;
                } else {
                    cur = 2;
                    increasing = 1;
                }
            } else if (nums[i - 1] > nums[i]) {
                if (increasing < 0) {
                    cur++;
                } else {
                    cur = 2;
                    increasing = -1;
                }
            } else {
                cur = 1;
                increasing = 0;
            }
            res = max(res, cur);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 3. Iteration - II

A cleaner approach is to maintain two separate counters: one for the current strictly increasing subarray length and one for the current strictly decreasing subarray length. At each step, we update both counters based on the relationship between consecutive elements.

```cpp
class Solution {
public:
    int longestMonotonicSubarray(vector<int>& nums) {
        int inc = 1, dec = 1, res = 1;

        for (int i = 1; i < nums.size(); i++) {
            if (nums[i] == nums[i - 1]) {
                inc = dec = 1;
            } else if (nums[i] > nums[i - 1]) {
                inc = inc + 1;
                dec = 1;
            } else {
                inc = 1;
                dec = dec + 1;
            }
            res = max(res, max(inc, dec));
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 4. Iteration - III

Another variation uses a single counter and checks if the current direction matches the direction at the start of the current subarray. By comparing the relationship between elements at the subarray's start with the relationship at the current position, we can determine if we're still following the same monotonic pattern.

```cpp
class Solution {
public:
    int longestMonotonicSubarray(vector<int>& nums) {
        int curLen = 1, res = 1;

        for (int i = 1; i < nums.size(); i++) {
            if (nums[i] == nums[i - 1] ||
                ((nums[i - curLen] < nums[i - curLen + 1]) != (nums[i - 1] < nums[i]))) {
                curLen = (nums[i] == nums[i - 1]) ? 1 : 2;
                continue;
            }

            curLen++;
            res = max(res, curLen);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
