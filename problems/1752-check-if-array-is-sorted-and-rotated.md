# 1752. Check if Array Is Sorted and Rotated

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/check-if-array-is-sorted-and-rotated/>  
- **NeetCode:** <https://neetcode.io/problems/check-if-array-is-sorted-and-rotated>  
- **Video:** <https://www.youtube.com/watch?v=Vzs_vlCIFEw>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A sorted and rotated array can be thought of as taking a sorted array and moving some elements from the end to the beginning. For example, `[3,4,5,1,2]` is `[1,2,3,4,5]` rotated. We can verify this by sorting the array and checking if our original array matches some rotation of the sorted version.

```cpp
class Solution {
public:
    bool check(vector<int>& nums) {
        int n = nums.size();
        vector<int> sortedNums = nums;
        sort(sortedNums.begin(), sortedNums.end());

        for (int i = 0; i < n; i++) {
            bool match = true;
            int idx = 0;
            for (int j = n - i; j < n && match; j++) {
                if (nums[idx] != sortedNums[j]) {
                    match = false;
                }
                idx++;
            }

            for (int j = 0; j < n - i && match; j++) {
                if (nums[idx] != sortedNums[j]) {
                    match = false;
                }
                idx++;
            }

            if (match) return true;
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Sliding Window

If we imagine the array as circular (the last element connects back to the first), a valid sorted-and-rotated array should have a contiguous segment of length `n` where elements are in non-decreasing order. We can simulate this circular behavior by conceptually doubling the array and looking for `n` consecutive non-decreasing elements.

```cpp
class Solution {
public:
    bool check(vector<int>& nums) {
        int N = nums.size();
        int count = 1;

        for (int i = 1; i < 2 * N; i++) {
            if (nums[(i - 1) % N] <= nums[i % N]) {
                count++;
            } else {
                count = 1;
            }
            if (count == N) {
                return true;
            }
        }

        return N == 1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 3. Iteration

In a sorted-and-rotated array, there can be at most one "break point" where a larger element is followed by a smaller element. This break point is where the rotation occurred. If we find more than one such break, the array cannot be a valid rotation of a sorted array.

```cpp
class Solution {
public:
    bool check(vector<int>& nums) {
        int count = 0, N = nums.size();

        for (int i = 0; i < N; i++) {
            if (nums[i] > nums[(i + 1) % N] && ++count > 1) {
                return false;
            }
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
