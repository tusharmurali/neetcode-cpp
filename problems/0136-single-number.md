# 136. Single Number

- **Difficulty:** Easy  
- **Pattern:** Bit Manipulation  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/single-number/>  
- **NeetCode:** <https://neetcode.io/problems/single-number>  
- **Video:** <https://www.youtube.com/watch?v=qMPX1AOa83k>  
- **Video approach:** 4. Bit Manipulation  

[← Back to index](../INDEX.md)

## 1. Brute Force

We are given an array where **every element appears twice except one**, and we need to find that unique element.

The brute force idea is straightforward:

- for each element in the array
- check whether it appears **anywhere else**
- if it does not match with any other element, then it must be the single number

This approach is simple and easy to understand, especially for beginners, because it directly follows the problem statement without using extra data structures or clever tricks.

```cpp
class Solution {
public:
    int singleNumber(vector<int>& nums) {
        for (int i = 0; i < nums.size(); i++) {
            bool flag = true;
            for (int j = 0; j < nums.size(); j++) {
                if (i != j && nums[i] == nums[j]) {
                    flag = false;
                    break;
                }
            }
            if (flag) {
                return nums[i];
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$

## 2. Hash Set

We are given an array where **every number appears exactly twice except one**, and we need to find that single number.

A convenient way to solve this is by using a **hash set** to track numbers as we iterate:

- when we see a number **for the first time**, we add it to the set
- when we see the **same number again**, we remove it from the set

Because:

- duplicates are added once and removed once
- only the number that appears **exactly once** will remain in the set

At the end, the set will contain **only one element**, which is the answer.

```cpp
class Solution {
public:
    int singleNumber(vector<int>& nums) {
        unordered_set<int> seen;
        for (int num : nums) {
            if (seen.count(num)) {
                seen.erase(num);
            } else {
                seen.insert(num);
            }
        }
        return *seen.begin();
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Sorting

We are given an array where **every element appears exactly twice except one**, and we need to find that unique element.

Sorting helps simplify the problem:

- after sorting, **duplicate numbers appear next to each other**
- the single number will be the **only element that does not have an identical neighbor**

So we can scan the array in steps of two:

- if `nums[i] == nums[i + 1]`, they form a valid pair → skip both
- if they are not equal, then `nums[i]` must be the unique element

This approach avoids extra space and relies on the structure created by sorting.

```cpp
class Solution {
public:
    int singleNumber(vector<int>& nums) {
        sort(begin(nums), end(nums));
        int i = 0;
        while (i < nums.size() - 1) {
            if (nums[i] == nums[i + 1]) {
                i += 2;
            } else {
                return nums[i];
            }
        }
        return nums[i];
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 4. Bit Manipulation ▶ video

We are given an array where **every number appears exactly twice except one**, and we need to find that unique number.

This problem is a perfect fit for **bit manipulation**, specifically the XOR (`^`) operation.

Key properties of XOR:

- `a ^ a = 0` (a number XORed with itself cancels out)
- `a ^ 0 = a` (XOR with `0` keeps the number unchanged)
- XOR is **commutative and associative**, so order does not matter

Because of these properties:

- all numbers that appear twice will cancel each other out
- the number that appears once will remain

```cpp
class Solution {
public:
    int singleNumber(vector<int>& nums) {
        int res = 0;
        for (int num : nums) {
            res ^= num;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0136-single-number.cpp` in the NeetCode repo)

```cpp
/*
    Given int array, every element appears twice except 1, find it
    Ex. nums = [2,2,1] -> 1, nums = [4,1,2,1,2] -> 4

    a XOR a returns 0, so returns 0 for all except the unique one

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int singleNumber(vector<int>& nums) {
        int result = 0;
        
        for (int i = 0; i < nums.size(); i++) {
            result = result ^ nums[i];
        }
        
        return result;
    }
};
```
