# 760. Find Anagram Mappings

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-anagram-mappings/>  
- **NeetCode:** <https://neetcode.io/problems/find-anagram-mappings>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The problem asks us to find, for each element in `nums1`, an index in `nums2` where that same value appears. The simplest approach is to check every position in `nums2` for each element in `nums1`. When we find a match, we record that index and move on. This guarantees correctness since we examine all possibilities.

```cpp
class Solution {
public:
    vector<int> anagramMappings(vector<int>& nums1, vector<int>& nums2) {
        // List to store the anagram mappings.
        vector<int> mappings;
        
        for (int num : nums1) {
            for (int i = 0; i < nums2.size(); i++) {
                // Store the corresponding index of number in the second list.
                if (num == nums2[i]) {
                    mappings.push_back(i);
                    break;
                }
            }
        }
        return mappings;
    }
};
```

**Complexity**

- Time complexity: $O(N^2)$
- Space complexity: $O(1)$ constant space

>  Where $N$ is the number of integers in the list `nums1` and `nums2`.

## 2. HashMap

Instead of scanning `nums2` repeatedly, we can preprocess it into a hash map that stores each value's index. This allows us to look up the corresponding index for any element in constant time. Since both arrays are anagrams, every element in `nums1` is guaranteed to exist in `nums2`.

```cpp
class Solution {
public:
    vector<int> anagramMappings(vector<int>& nums1, vector<int>& nums2) {
        // Store the index corresponding to the value in the second list.
        unordered_map<int, int> valueToPos;
        for (int i = 0; i < nums2.size(); i++) {
            valueToPos[nums2[i]] = i;
        }
        
        // List to store the anagram mappings.
        vector<int> mappings;
        for (int num : nums1) {
            mappings.push_back(valueToPos[num]);
        }
        
        return mappings;
    }
};
```

**Complexity**

- Time complexity: $O(N)$
- Space complexity: $O(N)$

>  Where $N$ is the number of integers in the list `nums1` and `nums2`.

## 3. Bit Manipulation + Sorting

We can avoid using extra hash map space by encoding each element's original index directly into the element itself using bit manipulation. By left-shifting each value and adding its index, we preserve both pieces of information in a single integer. After sorting both arrays, elements with the same original value will align at the same positions, letting us extract and pair up their indices.

```cpp
class Solution {
public:
    const int bitsToShift = 7;
    const int numToGetLastBits = (1 << bitsToShift) - 1;
    
    vector<int> anagramMappings(vector<int>& nums1, vector<int>& nums2) {
        // Store the index within the integer itself.
        for (int i = 0; i < nums1.size(); i++) {
            nums1[i] = (nums1[i] << bitsToShift) + i;
            nums2[i] = (nums2[i] << bitsToShift) + i;
        }
        
        // Sort both lists so that the original integers end up at the same index.
        sort(nums1.begin(), nums1.end());
        sort(nums2.begin(), nums2.end());
        
        // List to store the anagram mappings.
        vector<int> mappings(nums1.size());
        for (int i = 0; i < nums1.size(); i++) {
            // Store the index in the second list corresponding to the integer index in the first list.
            mappings[nums1[i] & numToGetLastBits] = (nums2[i] & numToGetLastBits);
        }

        return mappings;
    }
};
```

**Complexity**

- Time complexity: $O(N \log N)$
- Space complexity: $O(\log N)$

>  Where $N$ is the number of integers in the list `nums1` and `nums2`.
