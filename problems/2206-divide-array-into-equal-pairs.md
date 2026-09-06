# 2206. Divide Array Into Equal Pairs

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/divide-array-into-equal-pairs/>  
- **NeetCode:** <https://neetcode.io/problems/divide-array-into-equal-pairs>  
- **Video:** <https://www.youtube.com/watch?v=vxcpdClAktE>  

[← Back to index](../INDEX.md)

## 1. Sorting

For an array to be divisible into pairs of equal elements, every distinct value must appear an even number of times. By sorting the array, identical elements become adjacent. We can then scan through and count consecutive runs of equal values. If any run has an odd length, we cannot form valid pairs.

```cpp
class Solution {
public:
    bool divideArray(vector<int>& nums) {
        int N = nums.size();
        sort(nums.begin(), nums.end());

        int i = 0;
        while (i < N) {
            int j = i;
            while (j < N && nums[i] == nums[j]) {
                j++;
            }

            if ((j - i) % 2 != 0) {
                return false;
            }

            i = j;
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 2. Hash Map

We can count the frequency of each element using a hash map. After counting, we check if every element appears an even number of times. If any element has an odd count, it cannot be fully paired, so we return `false`.

```cpp
class Solution {
public:
    bool divideArray(vector<int>& nums) {
        unordered_map<int, int> count;
        for (int num : nums) {
            count[num]++;
        }

        for (auto& [key, cnt] : count) {
            if (cnt % 2 == 1) {
                return false;
            }
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Hash Set

Instead of counting all frequencies, we can use a set to track elements with odd occurrences. When we see an element, if it is already in the set (meaning we have seen it an odd number of times), we remove it. If it is not in the set, we add it. At the end, if the set is empty, all elements appeared an even number of times.

```cpp
class Solution {
public:
    bool divideArray(vector<int>& nums) {
        unordered_set<int> oddSet;

        for (int num : nums) {
            if (oddSet.count(num)) {
                oddSet.erase(num);
            } else {
                oddSet.insert(num);
            }
        }

        return oddSet.empty();
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
