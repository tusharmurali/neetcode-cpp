# 219. Contains Duplicate II

- **Difficulty:** Easy  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/contains-duplicate-ii/>  
- **NeetCode:** <https://neetcode.io/problems/contains-duplicate-ii>  
- **Video:** <https://www.youtube.com/watch?v=ypn0aZ0nrL4>  
- **Video approach:** 3. Hash Set  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach is to check every pair of elements. For each element, we look at all elements within distance `k` and check if any of them are equal. This guarantees finding a duplicate if one exists within the required distance.

```cpp
class Solution {
public:
    bool containsNearbyDuplicate(vector<int>& nums, int k) {
        for (int L = 0; L < nums.size(); L++) {
            for (int R = L + 1; R < min((int)nums.size(), L + k + 1); R++) {
                if (nums[L] == nums[R]) {
                    return true;
                }
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n * min(n, k))$
- Space complexity: $O(1)$

> Where $n$ is the size of the array $nums$ and $k$ is the maximum distance between two equal numbers.

## 2. Hash Map

Instead of checking all pairs, we can store the most recent index of each value in a hash map. When we encounter a value, we check if it appeared before and if the distance to its last occurrence is within `k`. This gives us O(1) lookup time for duplicates.

```cpp
class Solution {
public:
    bool containsNearbyDuplicate(vector<int>& nums, int k) {
        unordered_map<int, int> mp;

        for (int i = 0; i < nums.size(); i++) {
            if (mp.find(nums[i]) != mp.end() && i - mp[nums[i]] <= k) {
                return true;
            }
            mp[nums[i]] = i;
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the size of the array $nums$ and $k$ is the maximum distance between two equal numbers.

## 3. Hash Set ▶ video

We only need to check for duplicates within a sliding window of size `k`. Using a hash set, we maintain exactly the elements in the current window. If a new element already exists in the set, we found a duplicate within distance `k`. We slide the window by removing the leftmost element when the window exceeds size `k`.

```cpp
class Solution {
public:
    bool containsNearbyDuplicate(vector<int>& nums, int k) {
        unordered_set<int> window;
        int L = 0;

        for (int R = 0; R < nums.size(); R++) {
            if (R - L > k) {
                window.erase(nums[L]);
                L++;
            }
            if (window.find(nums[R]) != window.end()) {
                return true;
            }
            window.insert(nums[R]);
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(min(n, k))$

> Where $n$ is the size of the array $nums$ and $k$ is the maximum distance between two equal numbers.

## Standalone solution file (`cpp/0219-contains-duplicate-ii.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    bool containsNearbyDuplicate(vector<int>& nums, int k) {
        unordered_map<int,int> number_map;
        for (int i = 0; i < nums.size(); ++i) {
            int num = nums[i];
            if (number_map.find(num) != number_map.end() && i - number_map[num] <= k) {
                return true;
            }else {
                number_map[num] = i;
            }
        }
        return false;
    }
};
```
