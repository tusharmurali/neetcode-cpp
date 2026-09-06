# 191. Number of 1 Bits

- **Difficulty:** Easy  
- **Pattern:** Bit Manipulation  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/number-of-1-bits/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-one-bits>  
- **Video:** <https://www.youtube.com/watch?v=5Km3utixwZs>  

[← Back to index](../INDEX.md)

## 1. Bit Mask - I

We are asked to count how many **`1` bits** are present in the binary representation of an integer `n`.  
This value is also known as the **Hamming Weight** or **population count**.

A straightforward way to do this is to:

- check each bit position one by one
- see whether that bit is set (`1`) or not (`0`)

Since integers are typically represented using **32 bits**, we can safely check all 32 bit positions.

At each position:

- create a mask with a single `1` at that position using `1 << i`
- use bitwise AND (`&`) to test whether that bit is set in `n`

```cpp
class Solution {
public:
    int hammingWeight(uint32_t n) {
        int res = 0;
        for (int i = 0; i < 32; i++) {
            if ((1 << i) & n) {
                res++;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 2. Bit Mask - II

We want to count the number of `1` bits in the binary representation of an integer `n`.

Instead of checking every bit position explicitly, we can:

- look at the **least significant bit** of `n`
- then **shift the number right** to bring the next bit into that position

At each step:

- `n & 1` tells us whether the current least significant bit is `1`
- shifting `n` right by one (`n >>= 1`) moves us to the next bit

We repeat this until `n` becomes `0`.

```cpp
class Solution {
public:
    int hammingWeight(uint32_t n) {
        int res = 0;
        while (n != 0) {
            res += (n & 1) ? 1 : 0;
            n >>= 1;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 3. Bit Mask (Optimal)

We want to count the number of `1` bits in the binary representation of an integer `n` (Hamming Weight).

A very efficient trick comes from this key observation:

- Subtracting `1` from a number **flips the rightmost `1` bit to `0`** and turns all bits to its right into `1`
- Performing `n & (n - 1)` **removes the rightmost `1` bit** from `n`

So every time we do:
`n = n & (n - 1)` we eliminate exactly **one `1` bit**.

This means:

- the number of iterations equals the number of `1` bits
- we don’t waste time checking bits that are `0`

That’s why this approach is considered optimal.

```cpp
class Solution {
public:
    int hammingWeight(uint32_t n) {
        int res = 0;
        while (n) {
            n &= n - 1;
            res++;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 4. Built-In Function

We want to find the **Hamming Weight** of a number, which means counting how many `1` bits are present in its binary representation.

Most programming languages provide:

- a way to convert a number into **binary form**, or
- a built-in utility to **count set bits**

Instead of manually checking each bit using bit manipulation, we can rely on these built-in features. This makes the solution **short, easy to understand, and less error-prone**, especially for beginners.

This approach focuses on **clarity and simplicity**, not on low-level optimizations.

```cpp
class Solution {
public:
    int hammingWeight(uint32_t n) {
        return __builtin_popcount(n);
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0191-number-of-1-bits.cpp` in the NeetCode repo)

```cpp
/*
    Return number of '1' bits in an int
    Ex. n = 00001011 -> 3

    Simply count bit-by-bit & shift it off

    Time: O(1)
    Space: O(1)
*/

class Solution {
public:
    int hammingWeight(uint32_t n) {
        int bit = 0;
        int result = 0;
        
        while (n != 0) {
            bit = n & 1;
            if (bit == 1) {
                result++;
            }
            n = n >> 1;
        }
        
        return result;
    }
};


/* use kernighan's algorithm to only iterate num(set bits) times */
class Solution {
public:
    int hammingWeight(uint32_t n) {
        unsigned int count = 0;

        while(n) {
            ++count;
            // unset rightmost set bit
            n = (n & (n - 1));
        }
        
        return count;
    }
};
```
