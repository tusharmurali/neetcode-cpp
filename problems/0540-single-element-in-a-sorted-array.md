# 540. Single Element in a Sorted Array

- **Difficulty:** Medium  
- **Pattern:** Binary Search  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/single-element-in-a-sorted-array/>  
- **NeetCode:** <https://neetcode.io/problems/single-element-in-a-sorted-array>  
- **Video:** <https://www.youtube.com/watch?v=HGtqdzyUJ3k>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach is to scan the array and check each element against its neighbors. If an element is different from both its left and right neighbors, it must be the single element. This works because every other element appears exactly twice and must be adjacent to its duplicate in a sorted array.

```cpp
class Solution {
public:
    int singleNonDuplicate(vector<int>& nums) {
        int n = nums.size();
        for (int i = 0; i < n; i++) {
            if ((i > 0 && nums[i] == nums[i - 1]) ||
                (i < n - 1 && nums[i] == nums[i + 1])) {
                continue;
            }
            return nums[i];
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Brute Force (Bitwise Xor)

XOR has a useful property: a number XORed with itself gives `0`, and a number XORed with `0` gives the number itself. Since every element except one appears twice, XORing all elements together will cancel out all pairs, leaving only the single element.

```cpp
class Solution {
public:
    int singleNonDuplicate(vector<int>& nums) {
        int xorr = 0;
        for (int num : nums) {
            xorr ^= num;
        }
        return xorr;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 3. Binary Search

Since the array is sorted and every element except one appears twice, we can use binary search. Before the single element, pairs start at even indices (`0`, `2`, `4`...). After the single element, this pattern shifts. By checking whether the middle element pairs correctly with its neighbor, we can determine which half contains the single element.

```cpp
class Solution {
public:
    int singleNonDuplicate(vector<int>& nums) {
        int l = 0, r = nums.size() - 1;

        while (l <= r) {
            int m = l + (r - l) / 2;
            if ((m - 1 < 0 || nums[m - 1] != nums[m]) &&
                (m + 1 == nums.size() || nums[m] != nums[m + 1])) {
                return nums[m];
            }

            int leftSize = (m - 1 >= 0 && nums[m - 1] == nums[m]) ? m - 1 : m;
            if (leftSize % 2 == 1) {
                r = m - 1;
            } else {
                l = m + 1;
            }
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 4. Binary Search On Even Indexes

We can simplify binary search by only considering even indices. In a valid array without the single element disruption, every pair starts at an even index, so `nums[even] == nums[even + 1]`. If this condition holds at the middle even index, the single element must be to the right. Otherwise, it is on the left or at the current position.

```cpp
class Solution {
public:
    int singleNonDuplicate(vector<int>& nums) {
        int l = 0, r = nums.size() - 1;

        while (l < r) {
            int m = l + (r - l) / 2;
            if (m & 1) {
                m--;
            }
            if (nums[m] != nums[m + 1]) {
                r = m;
            } else {
                l = m + 2;
            }
        }

        return nums[l];
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 5. Binary Search + Bit Manipulation

We can use XOR with `1` to elegantly find the pair index. For even indices, `m ^ 1` gives `m + 1`; for odd indices, it gives `m - 1`. This means `nums[m]` should equal `nums[m ^ 1]` if we are in the portion before the single element. If they differ, the single element is at or before index `m`.

```cpp
class Solution {
public:
    int singleNonDuplicate(vector<int>& nums) {
        int l = 0, r = nums.size() - 1;

        while (l < r) {
            int m = (l + r) >> 1;
            if (nums[m] != nums[m ^ 1]) {
                r = m;
            } else {
                l = m + 1;
            }
        }

        return nums[l];
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0540-single-element-in-a-sorted-array.cpp` in the NeetCode repo)

```cpp
// Time complexity: O(log n)
// Space complexity: O(1)

class Solution
{
public:
    int singleNonDuplicate(vector<int> &nums)
    {
        int left = 0, right = nums.size() - 2;

        while (left <= right)
        {
            int mid1 = (left + right) >> 1;
            int mid2 = mid1 ^ 1;
            if (nums[mid1] == nums[mid2])
            {
                left = mid1 + 1;
            }
            else
            {
                right = mid1 - 1;
            }
        }

        return nums[left];
    }
};
```
