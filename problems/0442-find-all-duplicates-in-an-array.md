# 442. Find All Duplicates in an Array

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-all-duplicates-in-an-array/>  
- **NeetCode:** <https://neetcode.io/problems/find-all-duplicates-in-an-array>  
- **Video:** <https://www.youtube.com/watch?v=Y8x0iAVEITo>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most direct approach is to compare every element with every other element that comes after it. If we find two elements that are equal, we know that value appears twice (since the problem states each element appears at most twice).

```cpp
class Solution {
public:
    vector<int> findDuplicates(vector<int>& nums) {
        int n = nums.size();
        vector<int> res;

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (nums[i] == nums[j]) {
                    res.push_back(nums[i]);
                    break;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 2. Sorting

After sorting, duplicate values will be adjacent to each other. We can simply scan through the sorted array and check if any element equals its neighbor. This is more efficient than the brute force approach since we only need one pass after sorting.

```cpp
class Solution {
public:
    vector<int> findDuplicates(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<int> res;

        for (int i = 0; i < nums.size() - 1; i++) {
            if (nums[i] == nums[i + 1]) {
                res.push_back(nums[i]);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 3. Hash Set

We can use a hash set to track which numbers we have already seen. As we iterate through the array, if a number is already in the set, it must be a duplicate. Otherwise, we add it to the set. This gives us `O(1)` lookup time for each element.

```cpp
class Solution {
public:
    vector<int> findDuplicates(vector<int>& nums) {
        unordered_set<int> seen;
        vector<int> res;

        for (int num : nums) {
            if (seen.count(num)) {
                res.push_back(num);
            } else {
                seen.insert(num);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Hash Map

Instead of just tracking presence, we can count how many times each number appears using a hash map. After counting, we iterate through the map and collect all numbers that appear exactly `2`.

```cpp
class Solution {
public:
    vector<int> findDuplicates(vector<int>& nums) {
        unordered_map<int, int> count;
        vector<int> res;

        for (int num : nums) {
            count[num]++;
        }

        for (auto& [num, freq] : count) {
            if (freq == 2) {
                res.push_back(num);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 5. Negative Marking

Since all values are in the range `[1, n]` where `n` is the array length, we can use the array itself as a hash map. The key insight is that each value `v` can be mapped to index `v-1`. When we encounter a value, we mark the element at its corresponding index as negative. If we encounter a value whose corresponding index is already negative, that value must be a duplicate.

```cpp
class Solution {
public:
    vector<int> findDuplicates(vector<int>& nums) {
        vector<int> res;

        for (int num : nums) {
            int idx = abs(num) - 1;
            if (nums[idx] < 0) {
                res.push_back(abs(num));
            }
            nums[idx] = -nums[idx];
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
