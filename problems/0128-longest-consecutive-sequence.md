# 128. Longest Consecutive Sequence

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/longest-consecutive-sequence/>  
- **NeetCode:** <https://neetcode.io/problems/longest-consecutive-sequence>  
- **Video:** <https://www.youtube.com/watch?v=P6RZZMu_maU>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A consecutive sequence grows by checking whether the next number (`num + 1`, `num + 2`, …) exists in the set.
The brute-force approach simply starts from every number in the list and tries to extend a consecutive streak as far as possible.
For each number, we repeatedly check if the next number exists, increasing the streak length until the sequence breaks.
Even though this method works, it does unnecessary repeated work because many sequences get recomputed multiple times.

```cpp
class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        int res = 0;
        unordered_set<int> store(nums.begin(), nums.end());

        for (int num : nums) {
            int streak = 0, curr = num;
            while (store.find(curr) != store.end()) {
                streak++;
                curr++;
            }
            res = max(res, streak);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Sorting

If we sort the numbers first, then all consecutive values will appear next to each other.  
This makes it easy to walk through the sorted list and count how long each consecutive sequence is.  
We simply move forward while the current number matches the expected next value in the sequence.  
Duplicates don’t affect the result—they are just skipped—while gaps reset the streak count.  
This approach is simpler and more organized than the brute force method because sorting places all potential sequences in order.

```cpp
class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        if (nums.empty()) return 0;
        sort(nums.begin(), nums.end());

        int res = 0, curr = nums[0], streak = 0, i = 0;

        while (i < nums.size()) {
            if (curr != nums[i]) {
                curr = nums[i];
                streak = 0;
            }
            while (i < nums.size() && nums[i] == curr) {
                i++;
            }
            streak++;
            curr++;
            res = max(res, streak);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 3. Hash Set

To avoid repeatedly recounting the same sequences, we only want to start counting when we find the **beginning** of a consecutive sequence.
A number is the start of a sequence if `num - 1` is **not** in the set.
This guarantees that each consecutive sequence is counted exactly once.

Once we identify such a starting number, we simply keep checking if `num + 1`, `num + 2`, … exist in the set and extend the streak as far as possible.
This makes the solution efficient and clean because each number contributes to the sequence only one time.

```cpp
class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        unordered_set<int> numSet(nums.begin(), nums.end());
        int longest = 0;

        for (int num : numSet) {
            if (numSet.find(num - 1) == numSet.end()) {
                int length = 1;
                while (numSet.find(num + length) != numSet.end()) {
                    length++;
                }
                longest = max(longest, length);
            }
        }
        return longest;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Hash Map

When we place a new number into the map, it may connect two existing sequences or extend one of them.
Instead of scanning forward or backward, we only look at the lengths stored at the **neighbors**:

- `mp[num - 1]` gives the length of the sequence ending right before `num`
- `mp[num + 1]` gives the length of the sequence starting right after `num`

By adding these together and including the current number, we know the total length of the new merged sequence.
We then update the **left boundary** and **right boundary** of this sequence so the correct length can be retrieved later.
This keeps the whole operation very efficient and avoids repeated work.

```cpp
class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        unordered_map<int, int> mp;
        int res = 0;

        for (int num : nums) {
            if (!mp[num]) {
                mp[num] = mp[num - 1] + mp[num + 1] + 1;
                mp[num - mp[num - 1]] = mp[num];
                mp[num + mp[num + 1]] = mp[num];
                res = max(res, mp[num]);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0128-longest-consecutive-sequence.cpp` in the NeetCode repo)

```cpp
/*
    Given unsorted array, return length of longest consecutive sequence
    Ex. nums = [100,4,200,1,3,2] -> 4, longest is [1,2,3,4]

    Store in hash set, only check for longer seq if it's the beginning

    Time: O(n)
    Space: O(n)
*/


class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        unordered_set<int>s(nums.begin(), nums.end());
        int longest = 0;
        for(auto &n: s){
            //if this is the start of the sequence
            if(!s.count(n - 1)){
                int length = 1; 
                while(s.count(n + length))
                    ++length;
                longest = max(longest, length);
            } 

        }
        return longest;
    }
};
```
