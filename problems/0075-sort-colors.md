# 75. Sort Colors

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/sort-colors/>  
- **NeetCode:** <https://neetcode.io/problems/sort-colors>  
- **Video:** <https://www.youtube.com/watch?v=4xbWSRZHqac>  
- **Video approach:** 3. Three Pointers - I  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach is to use a standard sorting algorithm. Since the array only contains values 0, 1, and 2, sorting will naturally arrange them in the required order. While this works, it does not take advantage of the limited value range.

```cpp
class Solution {
public:
    void sortColors(vector<int>& nums) {
        sort(nums.begin(), nums.end());
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 2. Counting Sort

Since there are only three possible values (0, 1, 2), we can count how many times each appears in a single pass. Then we overwrite the array in a second pass, placing the correct number of 0s, followed by 1s, followed by 2s. This is a classic application of counting sort.

```cpp
class Solution {
public:
    void sortColors(vector<int>& nums) {
        vector<int> count(3);
        for (int& num : nums) {
            count[num]++;
        }

        int index = 0;
        for (int i = 0; i < 3; i++) {
            while (count[i]-- > 0) {
                nums[index++] = i;
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 3. Three Pointers - I ▶ video

The Dutch National Flag algorithm partitions the array into three sections in a single pass. We maintain pointers for the boundary of 0s (left), the boundary of 2s (right), and the current element being examined. When we see a 0, we swap it to the left section. When we see a 2, we swap it to the right section. 1s naturally end up in the middle.

```cpp
class Solution {
public:
    void sortColors(vector<int>& nums) {
        int i = 0, l = 0, r = nums.size() - 1;
        while (i <= r) {
            if (nums[i] == 0) {
                swap(nums[l], nums[i]);
                l++;
            } else if (nums[i] == 2) {
                swap(nums[i], nums[r]);
                r--;
                i--;
            }
            i++;
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 4. Three Pointers - II

This approach uses insertion boundaries for each color. We track where the next 0, 1, and 2 should be placed. When we encounter a value, we shift the boundaries by overwriting in a cascading manner. For example, when we see a 0, we write 2 at position `two`, then 1 at position `one`, then 0 at position `zero`, and advance all three boundaries.

```cpp
class Solution {
public:
    void sortColors(vector<int>& nums) {
        int zero = 0, one = 0, two = 0;
        for (int i = 0; i < nums.size(); i++) {
            if (nums[i] == 0) {
                nums[two++] = 2;
                nums[one++] = 1;
                nums[zero++] = 0;
            } else if (nums[i] == 1) {
                nums[two++] = 2;
                nums[one++] = 1;
            } else {
                nums[two++] = 2;
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 5. Three Pointers - III

This is a streamlined version of the previous approach. We iterate with pointer `two` and always write 2 at the current position. If the original value was less than 2, we also write 1 at position `one`. If it was less than 1 (i.e., 0), we also write 0 at position `zero`. This cascading write pattern ensures correct placement.

```cpp
class Solution {
public:
    void sortColors(vector<int>& nums) {
        int zero = 0, one = 0;
        for (int two = 0; two < nums.size(); two++) {
            int tmp = nums[two];
            nums[two] = 2;
            if (tmp < 2) {
                nums[one++] = 1;
            }
            if (tmp < 1) {
                nums[zero++] = 0;
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0075-sort-colors.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    void sortColors(vector<int>& nums) {
        int p1=0,p2=nums.size()-1;
        for(int i=p1;i<=p2;i++)
        {
            if(nums[i]==0)
            {
                swap(nums[i],nums[p1]);
                p1++;
            }
            if(nums[i]==2)
            {
                swap(nums[i],nums[p2]);
                p2--;
                i--;
            }
        }
        
        
    }
};
```
