# 3151. Special Array I

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/special-array-i/>  
- **NeetCode:** <https://neetcode.io/problems/special-array-i>  
- **Video:** <https://www.youtube.com/watch?v=RY6P9V878-0>  

[← Back to index](../INDEX.md)

## 1. Modulo Comparison

An array is special if every pair of adjacent elements has different parity (one is even, one is odd). To check this, we compare the parity of each element with its neighbor. Using the modulo operator, we can determine if a number is even (remainder 0 when divided by 2) or odd (remainder 1). If any two adjacent elements have the same parity, the array is not special.

```cpp
class Solution {
public:
    bool isArraySpecial(vector<int>& nums) {
        for (int i = 1; i < nums.size(); i++) {
            if (nums[i - 1] % 2 == nums[i] % 2) {
                return false;
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Bitwise Comparison

Instead of using the modulo operator to check parity, we can use bitwise AND with 1. The least significant bit of a number determines its parity: if the bit is 1, the number is odd; if the bit is 0, the number is even. Bitwise operations are typically faster than modulo operations, making this approach slightly more efficient.

```cpp
class Solution {
public:
    bool isArraySpecial(vector<int>& nums) {
        for (int i = 1; i < nums.size(); i++) {
            if ((nums[i - 1] & 1) == (nums[i] & 1)) {
                return false;
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
