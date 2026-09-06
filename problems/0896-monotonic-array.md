# 896. Monotonic Array

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/monotonic-array/>  
- **NeetCode:** <https://neetcode.io/problems/monotonic-array>  
- **Video:** <https://www.youtube.com/watch?v=sqWOFIZ9Z0U>  

[← Back to index](../INDEX.md)

## 1. Two Pass

An array is monotonic if it is entirely non-decreasing or entirely non-increasing. We can check each condition separately. First, scan to see if every element is greater than or equal to the previous one. If this holds, the array is monotonically increasing. If not, scan again to check if every element is less than or equal to the previous one. If either condition is satisfied, the array is monotonic.

```cpp
class Solution {
public:
    bool isMonotonic(vector<int>& nums) {
        int n = nums.size();
        bool increase = true;
        for (int i = 1; i < n; ++i) {
            if (nums[i] < nums[i - 1]) {
                increase = false;
                break;
            }
        }
        if (increase) {
            return true;
        }

        bool decrease = true;
        for (int i = 1; i < n; ++i) {
            if (nums[i] > nums[i - 1]) {
                decrease = false;
                break;
            }
        }
        return decrease;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. One Pass - I

We can determine the expected direction by comparing the first and last elements. If the first element is less than or equal to the last, the array should be non-decreasing. Otherwise, it should be non-increasing. With the direction determined upfront, a single pass can verify whether all consecutive pairs follow the expected pattern.

```cpp
class Solution {
public:
    bool isMonotonic(vector<int>& nums) {
        int n = nums.size();
        if (nums[0] <= nums[n - 1]) {
            for (int i = 1; i < n; ++i) {
                if (nums[i] < nums[i - 1]) {
                    return false;
                }
            }
            return true;
        } else {
            for (int i = 1; i < n; ++i) {
                if (nums[i] > nums[i - 1]) {
                    return false;
                }
            }
            return true;
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 3. One Pass - II

Rather than deciding the direction upfront, we can track both possibilities simultaneously. We maintain two flags: one for whether the array could still be non-decreasing, and one for whether it could still be non-increasing. As we scan, any violation disqualifies that direction. At the end, if at least one flag remains `true`, the array is monotonic.

```cpp
class Solution {
public:
    bool isMonotonic(vector<int>& nums) {
        bool increase = true, decrease = true;

        for (int i = 0; i < nums.size() - 1; ++i) {
            if (!(nums[i] <= nums[i + 1])) {
                increase = false;
            }
            if (!(nums[i] >= nums[i + 1])) {
                decrease = false;
            }
        }
        return increase || decrease;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
