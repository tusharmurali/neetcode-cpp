# 448. Find All Numbers Disappeared in An Array

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/>  
- **NeetCode:** <https://neetcode.io/problems/find-all-numbers-disappeared-in-an-array>  
- **Video:** <https://www.youtube.com/watch?v=8i-f24YFWC4>  
- **Video approach:** 4. Negative Marking (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Hash Set

We need to find numbers in the range `[1, n]` that are missing from the array. A simple approach is to create a set containing all numbers from `1` to `n`, then remove each number we find in the array. Whatever remains in the set are the missing numbers.

```cpp
class Solution {
public:
    vector<int> findDisappearedNumbers(vector<int>& nums) {
        int n = nums.size();
        unordered_set<int> store;
        for (int i = 1; i <= n; i++) store.insert(i);

        for (int num : nums) {
            store.erase(num);
        }

        vector<int> result(store.begin(), store.end());
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Boolean Array

Instead of using a set, we can use a boolean array where `mark[i]` indicates whether the number `i+1` is present in the input. We first mark all numbers that appear, then collect all indices where the mark is still `false`.

```cpp
class Solution {
public:
    vector<int> findDisappearedNumbers(vector<int>& nums) {
        int n = nums.size();
        vector<bool> mark(n, false);

        for (int num : nums) {
            mark[num - 1] = true;
        }

        vector<int> res;
        for (int i = 1; i <= n; i++) {
            if (!mark[i - 1]) {
                res.push_back(i);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Sorting

After sorting, we can use a two-pointer technique to find missing numbers. We iterate through numbers `1` to `n` and use a pointer to track our position in the sorted array. If the current number is not found at the pointer position, it must be missing.

```cpp
class Solution {
public:
    vector<int> findDisappearedNumbers(vector<int>& nums) {
        int n = nums.size();
        sort(nums.begin(), nums.end());

        vector<int> res;
        int idx = 0;
        for (int num = 1; num <= n; num++) {
            while (idx < n && nums[idx] < num) {
                idx++;
            }
            if (idx == n || nums[idx] > num) {
                res.push_back(num);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 4. Negative Marking ▶ video

Since values are in range `[1, n]`, we can use the input array itself as a marker. For each value `v`, we mark the position `v-1` as visited by making it negative. After processing all values, any position that remains positive corresponds to a missing number.

```cpp
class Solution {
public:
    vector<int> findDisappearedNumbers(vector<int>& nums) {
        for (int num : nums) {
            int i = abs(num) - 1;
            nums[i] = -abs(nums[i]);
        }

        vector<int> res;
        for (int i = 0; i < nums.size(); i++) {
            if (nums[i] > 0) {
                res.push_back(i + 1);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we modified the input array without using extra space.

## Standalone solution file (`cpp/0448-find-all-numbers-disappeared-in-an-array.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    /*
    Approach: 
    Traverse the entire array from start to end. Since the numbers are in a range [1, n] we can use this simple trick.
    At every index mark the position arr[arr[i]] as negative.
    Repeat this for every index in the array.
    At the end, which ever places are positive, add them to our answer.
    
    Time complexity: O(n)
    Space complexity: O(n)
    */
    vector<int> findDisappearedNumbers(vector<int>& nums) {
        vector<int> ans;
        
        for(int x : nums){                 /* Mark values as negative */
            int currentVal = abs(x);
            nums[currentVal-1] = 0 - abs(nums[currentVal-1]);
        }
        
        for(int i = 1; i <= nums.size(); i++)
            if(nums[i-1] > 0) ans.push_back(i);    /* Find unmarked values */
        
        return ans;
    }
};
```
