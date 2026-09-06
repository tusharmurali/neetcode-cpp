# 1611. Minimum Number of One Bit Operations to Make Integers Zero

- **Difficulty:** Hard  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-one-bit-operations-to-make-integers-zero/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-one-bit-operations-to-make-integers-zero>  
- **Video:** <https://www.youtube.com/watch?v=yRI18_MaG7k>  

[← Back to index](../INDEX.md)

## 1. Math (Recursion)

The key insight is understanding what it takes to flip the highest set bit to zero. To clear a bit at position `k`, we need to first set up a specific pattern where the bit at position `k-1` is `1` and all lower bits are `0`. This requires `2^k - 1` operations to go from `0` to that pattern. Once we have that setup, clearing the highest bit leaves us with a smaller number, and we recursively solve for that remainder. The operations alternate between adding and subtracting because each recursive step either builds toward or tears down from the target pattern.

```cpp
class Solution {
public:
    int minimumOneBitOperations(int n) {
        if (n == 0) {
            return 0;
        }

        int k = 1;
        while ((k << 1) <= n) {
            k <<= 1;
        }

        return (k << 1) - 1 - minimumOneBitOperations(k ^ n);
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(\log n)$ for recursion stack.

## 2. Math (Iteration) - I

This approach converts the recursive solution into an iterative one. We process each set bit from highest to lowest, alternating between adding and subtracting the cost. The first (highest) bit contributes positively, the next contributes negatively, and so on. This alternation happens because clearing one bit creates a pattern that partially overlaps with the work needed for the next bit.

```cpp
class Solution {
public:
    int minimumOneBitOperations(int n) {
        int res = 0, k = 1 << 30, sign = 1;

        while (n != 0) {
            while (k > n) {
                k >>= 1;
            }

            res += sign * ((k << 1) - 1);
            sign *= -1;
            n ^= k;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 3. Math (Iteration) - II

This variant uses a clever bit manipulation trick. The expression `n XOR (n-1)` isolates the rightmost set bit and all bits to its right (as a `mask` of `1`s). By processing bits from right to left and alternating `sign`s, we compute the same result as the previous approaches. The absolute value at the end handles the case where the `sign` ends up negative.

```cpp
class Solution {
public:
    int minimumOneBitOperations(int n) {
        int res = 0, sign = 1;
        while (n != 0) {
            res += sign * (n ^ (n - 1));
            n &= (n - 1);
            sign *= -1;
        }
        return abs(res);
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 4. Math (Grey Code)

This problem has a direct connection to Gray codes. A Gray code is a binary sequence where consecutive numbers differ by exactly one bit. The allowed operations in this problem exactly match how Gray codes transition between values. Converting a Gray code back to its binary `index` tells us how many steps away it is from zero. The conversion formula involves `XOR`ing `n` with all its right-shifted versions.

```cpp
class Solution {
public:
    int minimumOneBitOperations(int n) {
        int res = n;
        while (n != 0) {
            n >>= 1;
            res ^= n;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$
