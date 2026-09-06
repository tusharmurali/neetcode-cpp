# 1523. Count Odd Numbers in an Interval Range

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/count-odd-numbers-in-an-interval-range/>  
- **NeetCode:** <https://neetcode.io/problems/count-odd-numbers-in-an-interval-range>  
- **Video:** <https://www.youtube.com/watch?v=wrIWye928JQ>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach is to iterate through every number in the range and check if it is odd. We count all numbers where the least significant bit is 1.

```cpp
class Solution {
public:
    int countOdds(int low, int high) {
        int odd = 0;
        for (int num = low; num <= high; num++) {
            if (num & 1) {
                odd++;
            }
        }
        return odd;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

> Where $n$ is the number of integers in the given range.

## 2. Math

In any range of consecutive integers, odd and even numbers alternate. In a range of length `n`, there are `n/2` odd numbers if `n` is even. If `n` is odd, the count depends on whether the range starts with an odd number. Starting with odd gives one extra odd number.

```cpp
class Solution {
public:
    int countOdds(int low, int high) {
        int length = high - low + 1;
        int count = length / 2;
        if (length % 2 == 1 && low % 2 == 1) {
            count++;
        }
        return count;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 3. Math (One Liner)

The count of odd numbers from `1` to `n` is `(n + 1) / 2` (or equivalently `(n + 1) >> 1`). To find odd numbers in range `[low, high]`, we take the count up to `high` and subtract the count below `low`. The count below `low` equals the count up to `(low - 1)`, which is `low / 2` or `low >> 1`.

```cpp
class Solution {
public:
    int countOdds(int low, int high) {
        return ((high + 1) >> 1) - (low >> 1);
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$
