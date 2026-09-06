# 1822. Sign of the Product of an Array

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/sign-of-the-product-of-an-array/>  
- **NeetCode:** <https://neetcode.io/problems/sign-of-the-product-of-an-array>  
- **Video:** <https://www.youtube.com/watch?v=ILDLM86jNow>  

[← Back to index](../INDEX.md)

## 1. Count Negative Numbers

The sign of a product depends on two things: whether any factor is zero, and whether the count of negative factors is odd or even. If any number is zero, the product is `0`. Otherwise, an even count of negatives gives a positive product (negatives cancel out), and an odd count gives a negative product. We do not need to compute the actual product; just counting negatives is enough.

```cpp
class Solution {
public:
    int arraySign(vector<int>& nums) {
        int neg = 0;
        for (int num : nums) {
            if (num == 0) {
                return 0;
            }
            if (num < 0) {
                neg++;
            }
        }
        return neg % 2 == 0 ? 1 : -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Track the Sign of the Product

Instead of counting negatives and checking parity at the end, we can track the running sign directly. Start with a sign of `1` (positive). Each time we encounter a negative number, we flip the sign by multiplying by `-1`. If we encounter zero, the product is immediately `0`. This approach mirrors the actual multiplication process but only tracks the sign.

```cpp
class Solution {
public:
    int arraySign(vector<int>& nums) {
        int sign = 1;
        for (int num : nums) {
            if (num == 0) {
                return 0;
            }
            if (num < 0) {
                sign *= -1;
            }
        }
        return sign;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/1822-sign-of-the-product-of-an-array.cpp` in the NeetCode repo)

```cpp
// Time:  O(n)
// Space: O(1)

class Solution {
public:
    int arraySign(vector<int>& nums) {
        int neg = 0;
        for (int i : nums) {
            if (i == 0) {
                return 0;
            } else {
                neg += (i < 0) ? 1 : 0;
            }
        }
        return (neg % 2 == 0) ? 1 : -1;
    }
};
```
