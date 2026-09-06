# 1150. Check If a Number Is Majority Element in a Sorted Array

- **Difficulty:** Easy  
- **Pattern:** Binary Search  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/check-if-a-number-is-majority-element-in-a-sorted-array/>  
- **NeetCode:** <https://neetcode.io/problems/check-if-a-number-is-majority-element-in-a-sorted-array>  

[← Back to index](../INDEX.md)

## 1. Frequency Count

A majority element appears more than half the time. The simplest approach is to count how many times the target appears in the array by scanning through all elements. If the count exceeds `n`/2, the target is a majority element.

```cpp
class Solution {
public:
    bool isMajorityElement(vector<int>& nums, int target) {
        int count = 0;
        for (int num : nums) {
            count = num == target ? count + 1 : count;
        }

        return count > nums.size() / 2;
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(1)$ constant space

> Where $N$ is the size of `nums`.

## 2. Binary Search (Two Pass)

Since the array is sorted, all occurrences of the target are contiguous. We can use binary search to find the first and last occurrence of the target. The count is simply (`lastIndex` - `firstIndex` + 1), which we compare against `n`/2.

```cpp
class Solution {
public:
    // Returns the index of the first element equal to or greater than the target.
    // If there is no instance of the target in the list, it returns the length of the list.
    int lower_bound(vector<int>& nums, int target) {
        int start = 0;
        int end = nums.size() - 1;
        int index = nums.size();

        while (start <= end) {
            int mid = (start + end) / 2;

            if (nums[mid] >= target) {
                end = mid - 1;
                index = mid;
            } else {
                start = mid + 1;
            }
        }

        return index;
    }

    // Returns the index of the first element greater than the target.
    // If there is no instance of the target in the list, it returns the length of the list.
    int upper_bound(vector<int>& nums, int target) {
        int start = 0;
        int end = nums.size() - 1;
        int index = nums.size();

        while (start <= end) {
            int mid = (start + end) / 2;

            if (nums[mid] > target) {
                end = mid - 1;
                index = mid;
            } else {
                start = mid + 1;
            }
        }

        return index;
    }

    bool isMajorityElement(vector<int>& nums, int target) {
        int firstIndex = lower_bound(nums, target);
        int nextToLastIndex = upper_bound(nums, target);

        return nextToLastIndex - firstIndex > nums.size() / 2;
    }
};
```

**Complexity**

- Time complexity: $O(\log N)$
- Space complexity: $O(1)$ constant space

> Where $N$ is the size of `nums`.

## 3. Binary Search (One Pass)

If the target is a majority element, it must occupy more than half the array positions. This means if we find the first occurrence at index `i`, the element at index `i` + `n`/2 must also be the target. We only need one binary search to find the first occurrence, then check this specific position.

```cpp
class Solution {
public:
    // Returns the index of the first element equal to or greater than the target.
    // If there is no instance of the target in the list, it returns the length of the list.
    int lower_bound(vector<int>& nums, int target) {
        int start = 0;
        int end = nums.size() - 1;
        int index = nums.size();

        while (start <= end) {
            int mid = (start + end) / 2;

            if (nums[mid] >= target) {
                end = mid - 1;
                index = mid;
            } else {
                start = mid + 1;
            }
        }

        return index;
    }

    bool isMajorityElement(vector<int>& nums, int target) {
        int firstIndex = lower_bound(nums, target);

        return firstIndex + nums.size() / 2 < nums.size() && nums[firstIndex + nums.size() / 2] == target;
    }
};
```

**Complexity**

- Time complexity: $O(\log N)$
- Space complexity: $O(1)$ constant space

> Where $N$ is the size of `nums`.
