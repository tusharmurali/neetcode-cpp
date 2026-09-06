# 342. Power of Four

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/power-of-four/>  
- **NeetCode:** <https://neetcode.io/problems/power-of-four>  
- **Video:** <https://www.youtube.com/watch?v=qEYZPwnlM0U>  

[← Back to index](../INDEX.md)

## 1. Recursion

A number is a power of four if we can repeatedly divide it by 4 until we reach 1. If at any point the number is not divisible by 4 (or becomes zero or negative), it cannot be a power of four.

This naturally leads to a recursive solution where we reduce the problem size by dividing by 4 at each step.

```cpp
class Solution {
public:
    bool isPowerOfFour(int n) {
        if (n == 1) {
            return true;
        }
        if (n <= 0 || n % 4 != 0) {
            return false;
        }
        return isPowerOfFour(n / 4);
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 2. Iteration

The same logic as recursion applies here, but we use a loop instead. We keep dividing `n` by 4 as long as it remains divisible. If we end up with `1`, the original number was a power of four.

```cpp
class Solution {
public:
    bool isPowerOfFour(int n) {
        if (n < 0) return false;

        while (n > 1) {
            if (n % 4 != 0) return false;
            n /= 4;
        }

        return n == 1;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 3. Math

If `n` is a power of 4, then `n = 4^k` for some integer `k`. Taking the logarithm base 4 of both sides gives `k = log4(n)`. If this result is an integer, then `n` is a power of four.

We check if the logarithm yields a whole number by verifying the remainder when divided by 1 is zero.

```cpp
class Solution {
public:
    bool isPowerOfFour(int n) {
        return n > 0 && fmod(log(n) / log(4), 1) == 0;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 4. Bit Manipulation

Powers of four in binary are `1`, `100`, `10000`, `1000000`, etc. They have exactly one set bit, and that bit is always at an even position (`0`, `2`, `4`, ...).

We can check all even bit positions (`0`, `2`, `4`, ..., `30`) and see if `n` equals exactly one of these values: `1`, `4`, `16`, `64`, and so on.

```cpp
class Solution {
public:
    bool isPowerOfFour(int n) {
        if (n < 0) return false;

        for (int i = 0; i < 32; i += 2) {
            if (n == (1 << i)) {
                return true;
            }
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 5. Bit Mask - I

A power of four must first be a power of two (exactly one bit set). We verify this using `n & (n - 1) == 0`. But not all powers of two are powers of four (e.g., `2` and `8` are not).

Powers of four have their single set bit at even positions. The mask `0x55555555` (binary: `01010101...`) has `1`s at all even positions. ANDing with this mask confirms the bit is at a valid position.

```cpp
class Solution {
public:
    bool isPowerOfFour(int n) {
        return n > 0 && (n & (n - 1)) == 0 && (n & 0x55555555) == n;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 6. Bit Mask - II

Powers of four follow a pattern when divided by 3: `4^k mod 3 = 1` for all non-negative `k`. This is because `4 = 3 + 1`, so `4^k = (3+1)^k`, which when expanded always leaves remainder `1`.

Powers of two that are not powers of four (like `2`, `8`, `32`) give remainder `2` when divided by `3`. This gives us a simple way to distinguish between them.

```cpp
class Solution {
public:
    bool isPowerOfFour(int n) {
        return n > 0 && (n & (n - 1)) == 0 && (n % 3 == 1);
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0342-power-of-four.cpp` in the NeetCode repo)

```cpp
class Solution{    
    public:    
        bool isPowerOfFour(int n){            
            if(n <= 0){                
                return false;                
            }            
            bool pow = true;            
            while((n > 1) && (pow == true)){                
                n % 4 == 0 ? n = n / 4 : pow = false;                
            }            
            return pow;
        }    
};
```
