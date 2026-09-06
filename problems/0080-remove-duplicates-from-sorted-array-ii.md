# 80. Remove Duplicates From Sorted Array II

- **Difficulty:** Medium  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/>  
- **NeetCode:** <https://neetcode.io/problems/remove-duplicates-from-sorted-array-ii>  
- **Video:** <https://www.youtube.com/watch?v=ycAq8iqh0TI>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We allow each element to appear at most twice. When we find more than two consecutive duplicates, we shift all subsequent elements left to overwrite the extras. This in-place modification is straightforward but inefficient due to repeated shifting operations.

```cpp
class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        int n = nums.size();
        if (n <= 2) return n;
        int i = 0;
        while (i < n - 1) {
            if (nums[i] == nums[i + 1]) {
                int j = i + 2, cnt = 0;
                while (j < n && nums[i] == nums[j]) {
                    j++;
                    cnt++;
                }
                for (int k = i + 2; k < n; k++) {
                    if (j >= n) break;
                    nums[k] = nums[j++];
                }
                n -= cnt;
                i += 2;
            } else {
                i++;
            }
        }
        return n;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 2. Hash Map

We count occurrences of each element using a hash map while preserving order. Then we reconstruct the array, writing each element at most twice. This uses extra space but separates the counting logic from the placement logic.

```cpp
class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        unordered_map<int, int> count;
        vector<int> arr;
        for (int& num : nums) {
            count[num]++;
            if (count[num] == 1) {
                arr.push_back(num);
            }
        }

        int i = 0;
        for (auto& num : arr) {
            int& cnt = count[num];
            nums[i++] = num;
            cnt--;
            if (cnt >= 1) {
                nums[i++] = num;
                cnt--;
            }
        }
        return i;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Two Pointers

We process groups of consecutive duplicates together. For each group, we write at most two copies to the result portion of the array. The left pointer tracks where to write, and the right pointer scans through the array finding groups.

```cpp
class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        int l = 0, r = 0;

        while (r < nums.size()) {
            int count = 1;
            while (r + 1 < nums.size() && nums[r] == nums[r + 1]) {
                r++;
                count++;
            }

            for (int i = 0; i < min(2, count); i++) {
                nums[l] = nums[r];
                l++;
            }
            r++;
        }

        return l;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 4. Two Pointers (Optimal)

The cleanest approach uses a single condition: we only write an element if the write position is less than 2 (first two elements always go through) OR the current element differs from the element two positions back in the result. This automatically limits each value to at most two occurrences.

```cpp
class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        int l = 0;
        for (int num : nums) {
            if (l < 2 || num != nums[l - 2]) {
                nums[l] = num;
                l++;
            }
        }
        return l;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/0080-remove-duplicates-from-sorted-array-ii.cpp` in the NeetCode repo)

```cpp
/*
    Given a sorted array nums, remove some duplicates in-place such that each unique element appears at most twice.
    Ex:- nums = [1,1,1,2,2,3] -> [1,1,2,2,3,_]

    Input  -> nums = [1,1,1,2,2,3]
    Output -> 5

    Use two pointers to find at most 2 duplicates.

    Time - O(n)
    Space - O(1)
*/

class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        int k = 2; // define at most k times of duplicate numbers
        
        int l = 1, count = 1;

        for(int r = 1; r < nums.size(); r++){
            if(nums[r] == nums[r-1]){
                if(count < k)
                    nums[l++] = nums[r];
                count++;
            }
            else {
                count = 1;
                nums[l++] = nums[r];
            }
        }

        return l;
    }
};
```
