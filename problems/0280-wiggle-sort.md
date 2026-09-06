# 280. Wiggle Sort

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/wiggle-sort/>  
- **NeetCode:** <https://neetcode.io/problems/wiggle-sort>  
- **Video:** <https://www.youtube.com/watch?v=vGsyTE4s34w>  

[← Back to index](../INDEX.md)

## 1. Max-Heap

For a wiggle sorted array, odd indices should hold larger values and even indices should hold smaller values relative to their neighbors. Using a max-heap, we can extract elements in descending order and strategically place the largest values at odd indices first, then fill even indices with the remaining values. This ensures the wiggle property is maintained.

```cpp
class Solution {
public:
    void wiggleSort(vector<int>& nums) {
        priority_queue<int> maxHeap;
        for (int& num : nums) {
            maxHeap.push(num);
        }

        for (int i = 1; i < nums.size(); i += 2) {
            nums[i] = maxHeap.top();
            maxHeap.pop();
        }
        for (int i = 0; i < nums.size(); i += 2) {
            nums[i] = maxHeap.top();
            maxHeap.pop();
        }
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Sorting

After sorting the array, we can create the wiggle pattern by swapping adjacent pairs starting from index 1. When we swap elements at positions 1 and 2, then 3 and 4, and so on, we create local peaks at odd indices. This works because after sorting, swapping pushes the slightly larger element to the odd index position.

```cpp
class Solution {
public:
    void wiggleSort(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        for (int i = 1; i < nums.size() - 1; i += 2) {
            swap(nums[i], nums[i + 1]);
        }
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 3. Greedy - I

We can achieve wiggle sort in a single pass by observing the required relationship at each index. At odd indices, the element should be greater than or equal to its predecessor. At even indices, the element should be less than or equal to its predecessor. If these conditions are violated, we simply swap with the previous element to fix the relationship locally without affecting previously processed elements.

```cpp
class Solution {
public:
    void wiggleSort(vector<int>& nums) {
        for (int i = 1; i <nums.size(); i++) {
            if ((i % 2 == 1 && nums[i] < nums[i - 1]) ||
                (i % 2 == 0 && nums[i] > nums[i - 1])) {
                swap(nums[i], nums[i - 1]);
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 4. Greedy - II

This is an optimized version of the greedy approach using XOR for condition checking. The key observation is that we need to swap when the parity of the index does not match whether the current element is greater than the previous. Using XOR on these two boolean conditions elegantly captures when a swap is needed.

```cpp
class Solution {
public:
    void wiggleSort(vector<int>& nums) {
        for (int i = 1; i <nums.size(); i++) {
            if ((i % 2) ^ (nums[i] > nums[i - 1])) {
                swap(nums[i], nums[i - 1]);
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0280-wiggle-sort.cpp` in the NeetCode repo)

```cpp
/*
    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    void wiggleSort(vector<int> &nums) {
        for(int i=1; i<nums.size(); i++) {
            if((i%2==1 && (nums[i] < nums[i-1])) || (i%2==0 && (nums[i] > nums[i-1])))
                swap(nums[i], nums[i-1]);
        }
    }
};
```
