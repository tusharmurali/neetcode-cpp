# 1968. Array With Elements Not Equal to Average of Neighbors

- **Difficulty:** Medium  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/array-with-elements-not-equal-to-average-of-neighbors/>  
- **NeetCode:** <https://neetcode.io/problems/array-with-elements-not-equal-to-average-of-neighbors>  
- **Video:** <https://www.youtube.com/watch?v=Wmb3YdVYfqM>  

[← Back to index](../INDEX.md)

## 1. Greedy

If we sort the array, adjacent elements become close in value, which makes it more likely for an element to be the average of its neighbors. To avoid this, we can interleave elements from the small and large ends of the sorted array. By alternating between picking from the front (small) and back (large), we create a pattern where neighbors differ significantly, preventing any element from being the exact average of its neighbors.

```cpp
class Solution {
public:
    vector<int> rearrangeArray(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<int> res;
        int l = 0, r = nums.size() - 1;

        while (res.size() != nums.size()) {
            res.push_back(nums[l++]);
            if (l <= r) {
                res.push_back(nums[r--]);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n\log n)$
- Space complexity: $O(n)$

## 2. Greedy (Space Optimized)

Instead of building a new array, we can rearrange in place. After sorting, if we swap every pair of adjacent elements at odd indices with their preceding element, we create a zigzag pattern. This ensures that each element at an odd index is a local maximum or minimum relative to its neighbors, which prevents any element from being the average of its neighbors.

```cpp
class Solution {
public:
    vector<int> rearrangeArray(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        for (int i = 1; i < nums.size(); i += 2) {
            swap(nums[i], nums[i - 1]);
        }
        return nums;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 3. Greedy (Optimal) - I

We can fix violations as we find them without sorting first. If an element equals the average of its neighbors, swapping it with an adjacent element will break that relationship. By making one forward pass and one backward pass, we can fix all violations. The forward pass handles cases where swapping with the next element helps, and the backward pass catches any remaining issues.

```cpp
class Solution {
public:
    vector<int> rearrangeArray(vector<int>& nums) {
        int n = nums.size();

        for (int i = 1; i < n - 1; i++) {
            if (2 * nums[i] == (nums[i - 1] + nums[i + 1])) {
                swap(nums[i], nums[i + 1]);
            }
        }

        for (int i = n - 2; i > 0; i--) {
            if (2 * nums[i] == (nums[i - 1] + nums[i + 1])) {
                swap(nums[i], nums[i - 1]);
            }
        }

        return nums;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 4. Greedy Optimal - II

A valid arrangement alternates between increasing and decreasing. We can enforce this pattern in a single pass by tracking whether the next step should increase or decrease. Starting from the relationship between the first two elements, we alternate the expected direction. If the actual relationship violates the expected direction, we swap to fix it.

```cpp
class Solution {
public:
    vector<int> rearrangeArray(vector<int>& nums) {
        bool increase = nums[0] < nums[1];
        for (int i = 1; i < nums.size() - 1; i++) {
            if ((increase && nums[i] < nums[i + 1]) ||
                (!increase && nums[i] > nums[i + 1])) {
                swap(nums[i], nums[i + 1]);
            }
            increase = !increase;
        }
        return nums;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/1968-array-with-elements-not-equal-to-average-of-neighbors.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    vector<int> rearrangeArray(vector<int>& nums) {
         vector<int> ans;
        for(int i=1;i<nums.size()-1;i++){
            int a=nums[i-1];
            int b=nums[i];
            int c=nums[i+1];
            if(a>b && b>c || a<b && b<c)
            {
                swap(nums[i],nums[i+1]);
            }
        }
        return nums;
    }
};
```
