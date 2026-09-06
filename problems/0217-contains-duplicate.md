# 217. Contains Duplicate

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/contains-duplicate/>  
- **NeetCode:** <https://neetcode.io/problems/duplicate-integer>  
- **Video:** <https://www.youtube.com/watch?v=3OamzN90kPg>  
- **Video approach:** 3. Hash Set  

[← Back to index](../INDEX.md)

## 1. Brute Force

We can check every pair of different elements in the array and return `true` if any pair has equal values.  
This is the most intuitive approach because it directly compares all possible pairs, but it is also the least efficient since it examines every combination.

```cpp
class Solution {
public:
    bool hasDuplicate(vector<int>& nums) {
        for (int i = 0; i < nums.size(); i++) {
            for (int j = i + 1; j < nums.size(); j++) {
                if (nums[i] == nums[j]) {
                    return true;
                }
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Sorting

If we sort the array, then any duplicate values will appear next to each other.  
Sorting groups identical elements together, so we can simply check adjacent positions to detect duplicates.  
This reduces the problem to a single linear scan after sorting, making it easy to identify if any value repeats.

```cpp
class Solution {
public:
    bool hasDuplicate(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        for (int i = 1; i < nums.size(); i++) {
            if (nums[i] == nums[i - 1]) {
                return true;
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 3. Hash Set ▶ video

We can use a hash set to efficiently keep track of the values we have already encountered.  
As we iterate through the array, we check whether the current value is already present in the set.  
If it is, that means we've seen this value before, so a duplicate exists.  
Using a hash set allows constant-time lookups, making this approach much more efficient than comparing every pair.

```cpp
class Solution {
public:
    bool hasDuplicate(vector<int>& nums) {
        unordered_set<int> seen;
        for (int num : nums) {
            if (seen.count(num)) {
                return true;
            }
            seen.insert(num);
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Hash Set Length

This approach uses the same idea as the previous hash set method: a set only stores unique values, so duplicates are automatically removed.  
Instead of checking each element manually, we simply compare the length of the set to the length of the original array.  
If duplicates exist, the set will contain fewer elements.  
The logic is identical to the earlier approach — this version is just a shorter and more concise implementation of it.

```cpp
class Solution {
public:
    bool hasDuplicate(vector<int>& nums) {
        return unordered_set<int>(nums.begin(), nums.end()).size() < nums.size();
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0217-contains-duplicate.cpp` in the NeetCode repo)

```cpp
/*
    Given int array, return true if any value appears at least twice
    Ex. nums = [1,2,3,1] -> true, nums = [1,2,3,4] -> false

    If the number has been seen previously, then it has a duplicate. Otherwise, insert it into the hash set.

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    bool containsDuplicate(vector<int>& nums) {
        unordered_set<int> s;
        
        for (int i = 0; i < nums.size(); i++) {
            if (s.find(nums[i]) != s.end()) {
                return true;
            }
            s.insert(nums[i]);
        }
        
        return false;
    }
};
```
