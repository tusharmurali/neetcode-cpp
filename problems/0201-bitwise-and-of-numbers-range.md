# 201. Bitwise AND of Numbers Range

- **Difficulty:** Medium  
- **Pattern:** Bit Manipulation  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/bitwise-and-of-numbers-range/>  
- **NeetCode:** <https://neetcode.io/problems/bitwise-and-of-numbers-range>  
- **Video:** <https://www.youtube.com/watch?v=R3T0olAhUq0>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach is to AND all numbers in the range together. Starting with the left boundary, we iterate through each number up to the right boundary, accumulating the AND result. While simple, this is inefficient for large ranges.

```cpp
class Solution {
public:
    int rangeBitwiseAnd(int left, int right) {
        int res = left;
        for (int i = left + 1; i <= right; i++) {
            res &= i;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Bit Manipulation - I

For any bit position in the result to be `1`, that bit must be `1` in all numbers from `left` to `right`. If a bit is `1` in `left`, we need to check if it will flip to `0` at some point in the range. A bit at position `i` flips when we reach the next multiple of `2^(i+1)`. So we calculate how far `left` is from that flip point and check if `right` is still before it.

```cpp
class Solution {
public:
    int rangeBitwiseAnd(int left, int right) {
        int res = 0;
        for (int i = 0; i < 32; i++) {
            int bit = (left >> i) & 1;
            if (!bit) {
                continue;
            }

            int remain = left % (1 << (i + 1));
            uint diff = (1ul << (i + 1)) - remain;
            if (right - left < diff) {
                res |= (1 << i);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(1)$ since we iterate $32$ times.
- Space complexity: $O(1)$

## 3. Bit Manipulation - II

The result is the common prefix of the binary representations of `left` and `right`. When `left` and `right` differ, the differing bits and all bits to the right will become `0` in the AND result (since there will be at least one `0` in each of those positions across the range). We find this common prefix by right-shifting both numbers until they are equal.

```cpp
class Solution {
public:
    int rangeBitwiseAnd(int left, int right) {
        int i = 0;
        while (left != right) {
            left >>= 1;
            right >>= 1;
            i++;
        }
        return left << i;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 4. Bit Manipulation - III

Instead of shifting both numbers, we can repeatedly clear the rightmost set bit of `right` until `right` becomes less than or equal to `left`. The operation `(n & (n-1))` clears the lowest set bit of `n`. This works because any bit position where `right` has a `1` but needs to flip within the range will be cleared, leaving only the common prefix.

```cpp
class Solution {
public:
    int rangeBitwiseAnd(int left, int right) {
        while (left < right) {
            right &= (right - 1);
        }
        return right;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$
