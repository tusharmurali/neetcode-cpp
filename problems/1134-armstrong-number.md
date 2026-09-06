# 1134. Armstrong Number

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/armstrong-number/>  
- **NeetCode:** <https://neetcode.io/problems/armstrong-number>  

[← Back to index](../INDEX.md)

## 1. Calculate k by Converting to String

An Armstrong number equals the sum of its digits each raised to the power of the total digit count. For example, 153 has 3 digits, and 1^3 + 5^3 + 3^3 = 153.

The straightforward approach is to convert the number to a string to count digits, then extract each digit and compute the sum of powers. We compare this sum to the original number.

```cpp
class Solution {
public:
    int getSumOfKthPowerOfDigits(int n, int k) {
        int result = 0;

        while (n != 0) {
            result += pow(n % 10, k);
            n /= 10;
        }

        return result;
    }

    bool isArmstrong(int n) {
        int length = to_string(n).length();

        return getSumOfKthPowerOfDigits(n, length) == n;
    }
};
```

**Complexity**

- Time complexity: $O(M)$

- Space complexity: $O(1)$ constant space

> Where $M$ is the number of digits in the input integer `n`.

## 2. Calculate k by Using Log

Instead of converting to a string, we can use logarithms to count digits. The number of digits in a positive integer `n` is `floor(log10(n)) + 1`. This avoids string allocation and can be slightly more efficient.

The rest of the logic remains the same: extract digits, raise each to the power of `k`, sum them up, and compare.

```cpp
class Solution {
public:
    int getSumOfKthPowerOfDigits(int n, int k) {
        int result = 0;

        while (n != 0) {
            result += pow(n % 10, k);
            n /= 10;
        }

        return result;
    }

    bool isArmstrong(int n) {
        int length = log10(n) + 1;

        return getSumOfKthPowerOfDigits(n, length) == n;
    }
};
```

**Complexity**

- Time complexity: $O(M)$

- Space complexity: $O(1)$ constant space

> Where $M$ is the number of digits in the input integer `n`.

## 3. Calculate k Without Built-in Methods

We can count digits without any built-in functions by simply dividing the number by 10 until it becomes 0, counting iterations. This approach uses only basic arithmetic and works in any language without library dependencies.

```cpp
class Solution {
public:
    int getSumOfKthPowerOfDigits(int n, int k) {
       int result = 0;

        while(n != 0) {
            result += pow(n % 10, k);
            n /= 10;
        }

       return result;
    }

    bool isArmstrong(int n) {
        int length = 0;
        int tempN = n;

        while (tempN) {
            length++;
            tempN /= 10;
        }

        return getSumOfKthPowerOfDigits(n, length) == n;
    }
};
```

**Complexity**

- Time complexity: $O(M)$

- Space complexity: $O(1)$ constant space

> Where $M$ is the number of digits in the input integer `n`.
