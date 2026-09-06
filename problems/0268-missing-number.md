# 268. Missing Number

- **Difficulty:** Easy  
- **Pattern:** Bit Manipulation  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/missing-number/>  
- **NeetCode:** <https://neetcode.io/problems/missing-number>  
- **Video:** <https://www.youtube.com/watch?v=WnPLSRLSANE>  
- **Video approach:** 4. Math  

[← Back to index](../INDEX.md)

## 1. Sorting

We are given an array containing `n` **distinct numbers** taken from the range `[0, n]`.  
Exactly **one number is missing**, and we need to find it.

A simple way to reason about this is:

- If the array were complete and sorted, the number at index `i` should be exactly `i`
- As soon as this condition breaks, that index represents the missing number

Sorting the array puts the numbers in order, making this comparison straightforward and beginner-friendly.

```cpp
class Solution {
public:
    int missingNumber(vector<int>& nums) {
        int n = nums.size();
        sort(nums.begin(), nums.end());
        for (int i = 0; i < n; i++) {
            if (nums[i] != i) {
                return i;
            }
        }
        return n;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the sorting algorithm.

## 2. Hash Set

We are given `n` distinct numbers taken from the range `[0, n]`, with **exactly one number missing**.

A natural way to approach this is to ask:

> “Can we quickly check whether a number exists in the array?”

Using a **hash-based data structure** (like a hash set) allows us to:

- Store all given numbers
- Check the presence of any number in **constant time**

Once all numbers are stored, we simply look for the number in the range `[0, n]` that does **not** appear in the set.

This approach trades a little extra space for very clear and simple logic.

```cpp
class Solution {
public:
    int missingNumber(vector<int>& nums) {
        unordered_set<int> num_set(nums.begin(), nums.end());
        int n = nums.size();
        for (int i = 0; i <= n; i++) {
            if (num_set.find(i) == num_set.end()) {
                return i;
            }
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Bitwise XOR

We are given `n` distinct numbers from the range `[0, n]`, with **exactly one number missing**.

A very powerful observation comes from the properties of **XOR (⊕)**:

- `a ⊕ a = 0` (a number cancels itself)
- `a ⊕ 0 = a`
- XOR is **commutative and associative** (order does not matter)

If we XOR:

- all numbers from `0` to `n`
- and all numbers present in the array

Every number that appears in both places will cancel out, leaving **only the missing number**.

This allows us to find the answer in **linear time** and **constant space**, without sorting or extra data structures.

```cpp
class Solution {
public:
    int missingNumber(vector<int>& nums) {
        int n = nums.size();
        int xorr = n;
        for (int i = 0; i < n; i++) {
            xorr ^= i ^ nums[i];
        }
        return xorr;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 4. Math ▶ video

We are given `n` distinct numbers from the range `[0, n]`, with **exactly one number missing**.

A simple mathematical observation helps here:

- The sum of numbers from `0` to `n` is known
- If we subtract the sum of the given array from this expected sum, the result must be the missing number

Instead of computing two separate sums, we can combine both ideas into a **single running calculation**, which keeps the logic clean and avoids overflow issues in some languages.

This approach uses **basic arithmetic**, making it easy to understand and language-independent.

```cpp
class Solution {
public:
    int missingNumber(vector<int>& nums) {
        int res = nums.size();

        for (int i = 0; i < nums.size(); i++) {
            res += i - nums[i];
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0268-missing-number.cpp` in the NeetCode repo)

```cpp
/*
    Given array in range [0, n], return missing
    Ex. nums = [3,0,1] -> 2, nums = [0,1] -> 2

    Use the fact that XOR is its own inverse
    Ex. [0,1,3,4]
    Missing = 4^(0^0)^(1^1)^(2^3)^(3^4)
            = (4^4)^(0^0)^(1^1)^(3^3)^2
            = 0^0^0^0^2 = 2

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int missingNumber(vector<int>& nums) {
        int n = nums.size();
        int result = n;
        for (int i = 0; i < n; i++) {
            result ^= i ^ nums[i];
        }
        return result;
    }
};
```
