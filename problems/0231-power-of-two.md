# 231. Power of Two

- **Difficulty:** Easy  
- **Pattern:** Bit Manipulation  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/power-of-two/>  
- **NeetCode:** <https://neetcode.io/problems/power-of-two>  
- **Video:** <https://www.youtube.com/watch?v=H2bjttEV4Vc>  
- **Video approach:** 1. Brute Force (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Brute Force ▶ video

We can generate all powers of two by starting from `1` and repeatedly multiplying by `2`. If we reach exactly `n`, then `n` is a power of two. If we exceed `n` without matching it, then it's not.

```cpp
class Solution {
public:
    bool isPowerOfTwo(int n) {
        if (n <= 0) return false;

        long long x = 1;
        while (x < n) {
            x *= 2;
        }
        return x == n;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 2. Recursion

A number is a power of two if we can repeatedly divide it by `2` until we reach `1`. If at any point the number is odd (and not `1`), it cannot be a power of two.

This recursive approach reduces the problem by half at each step.

```cpp
class Solution {
public:
    bool isPowerOfTwo(int n) {
        if (n == 1) {
            return true;
        }
        if (n <= 0 || n % 2 == 1) {
            return false;
        }
        return isPowerOfTwo(n / 2);
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(\log n)$ for recursion stack.

## 3. Iteration

The same logic as recursion, but implemented with a loop. We keep dividing by `2` (or right-shifting by `1`) as long as the number is even. If we end up with `1`, the original number was a power of two.

```cpp
class Solution {
public:
    bool isPowerOfTwo(int n) {
        if (n <= 0) return false;

        while (n % 2 == 0) {
            n >>= 1;
        }
        return n == 1;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 4. Bit Manipulation - I

In two's complement representation, `-n` flips all bits of `n` and adds `1`. For a power of two (which has exactly one set bit), `n & (-n)` isolates the lowest set bit. If `n` is a power of two, this equals `n` itself since there's only one bit set.

```cpp
class Solution {
public:
    bool isPowerOfTwo(int n) {
        return n > 0 && (n & (-n)) == n;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 5. Bit Manipulation - II

Powers of two in binary have exactly one bit set (`1`, `10`, `100`, `1000`, ...). Subtracting `1` from such a number flips all bits from the rightmost set bit onward. For example, `8` (`1000`) minus `1` equals `7` (`0111`).

ANDing `n` with `n - 1` clears the lowest set bit. If `n` is a power of two, this results in `0` since there was only one bit to clear.

```cpp
class Solution {
public:
    bool isPowerOfTwo(int n) {
        return n > 0 && (n & (n - 1)) == 0;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 6. Math

The largest power of two that fits in a 32-bit signed integer is `2^30` (since `2^31` exceeds the positive range). Any smaller power of two must divide evenly into `2^30`.

If `n` is a power of two, then `2^30 mod n` equals `0`. If `n` is not a power of two, the division will have a remainder.

```cpp
class Solution {
public:
    bool isPowerOfTwo(int n) {
        return n > 0 && ((1 << 30) % n) == 0;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0231-power-of-two.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    bool isPowerOfTwo(int n) {
        return n > 0 && !(n & (n - 1));
    }
};
```
