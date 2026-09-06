# 167. Two Sum II Input Array Is Sorted

- **Difficulty:** Medium  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/>  
- **NeetCode:** <https://neetcode.io/problems/two-integer-sum-ii>  
- **Video:** <https://www.youtube.com/watch?v=cQ1Oz4ckceM>  

[← Back to index](../INDEX.md)

## 1. Brute Force

Brute force ignores the ordering and simply checks every possible pair.
For each index `i`, we look at every index `j > i` and check whether their sum equals the target.  
This approach is easy to understand but inefficient because it tries all combinations without using the sorted property.

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        for (int i = 0; i < numbers.size(); i++) {
            for (int j = i + 1; j < numbers.size(); j++) {
                if (numbers[i] + numbers[j] == target) {
                    return { i + 1, j + 1 };
                }
            }
        }
        return {};
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Binary Search

Because the array is already sorted, we don’t need to check every pair.  
For each number at index `i`, we know exactly what value we need to find:  
`target - numbers[i]`.  
Since the array is sorted, we can efficiently search for this value using **binary search** instead of scanning linearly.  
This reduces the inner search from **O(n)** to **O(log n)**, making the solution much faster.

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        for (int i = 0; i < numbers.size(); i++) {
            int l = i + 1, r = numbers.size() - 1;
            int tmp = target - numbers[i];
            while (l <= r) {
                int mid = l + (r - l) / 2;
                if (numbers[mid] == tmp) {
                    return { i + 1, mid + 1 };
                } else if (numbers[mid] < tmp) {
                    l = mid + 1;
                } else {
                    r = mid - 1;
                }
            }
        }
        return {};
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$

## 3. Hash Map

Even though the array is sorted, we can still use a hash map to solve the problem efficiently.  
As we scan through the list, we compute the needed complement for each number.  
If that complement has already been seen earlier (stored in the hash map), then we have found the required pair.  
Otherwise, we store the current number with its **(1-indexed)** position.

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        unordered_map<int, int> mp;
        for (int i = 0; i < numbers.size(); i++) {
            int tmp = target - numbers[i];
            if (mp.count(tmp)) {
                return { mp[tmp], i + 1 };
            }
            mp[numbers[i]] = i + 1;
        }
        return {};
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Two Pointers

Because the array is sorted, we can use two pointers to adjust the sum efficiently.  
If the current sum is too big, moving the right pointer left makes the sum smaller.  
If the sum is too small, moving the left pointer right makes the sum larger.  
This lets us quickly close in on the target without checking every pair.

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        int l = 0, r = numbers.size() - 1;

        while (l < r) {
            int curSum = numbers[l] + numbers[r];

            if (curSum > target) {
                r--;
            } else if (curSum < target) {
                l++;
            } else {
                return { l + 1, r + 1 };
            }
        }
        return {};
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0167-two-sum-ii-input-array-is-sorted.cpp` in the NeetCode repo)

```cpp
/*
    Given a 1-indexed sorted int array & target:
    Return indices (added by 1) of 2 nums that add to target

    2 pointers, outside in, iterate i/j if sum is too low/high

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        int i = 0;
        int j = numbers.size() - 1;
        
        vector<int> result;
        
        while (i < j) {
            int sum = numbers[i] + numbers[j];
            if (sum < target) {
                i++;
            } else if (sum > target) {
                j--;
            } else {
                result.push_back(i + 1);
                result.push_back(j + 1);
                break;
            }
        }
        
        return result;
    }
};
```
