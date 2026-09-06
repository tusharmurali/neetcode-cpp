# 190. Reverse Bits

- **Difficulty:** Easy  
- **Pattern:** Bit Manipulation  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/reverse-bits/>  
- **NeetCode:** <https://neetcode.io/problems/reverse-bits>  
- **Video:** <https://www.youtube.com/watch?v=UcoN6UjAI64>  
- **Video approach:** 2. Bit Manipulation  

[← Back to index](../INDEX.md)

## 1. Brute Force

We are given a **32-bit unsigned integer**, and we need to **reverse its bits**.

The most straightforward way to think about this problem is:

- Read the bits of the number from **right to left**
- Build a new number by placing those bits from **left to right**

In simpler terms:

- Extract each bit one by one
- Reverse their order
- Reconstruct the number from the reversed bits

This brute force approach closely follows how humans would solve the problem manually, making it **easy to understand**, though not the most optimal.

```cpp
class Solution {
public:
    uint32_t reverseBits(uint32_t n) {
        string binary = "";
        for (int i = 0; i < 32; i++) {
            if (n & (1 << i)) {
                binary += '1';
            } else {
                binary += '0';
            }
        }

        uint32_t res = 0;
        for (int i = 0; i < 32; i++) {
            if (binary[31 - i] == '1') {
                res |= (1 << i);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 2. Bit Manipulation ▶ video

We are given a **32-bit unsigned integer** and need to **reverse all its bits**.

Instead of storing bits in a string or array, we can do this directly using **bit manipulation**:

- Extract each bit from the original number starting from the least significant bit
- Place that bit into the correct reversed position in the result
- Repeat this for all 32 bits

This approach avoids extra memory and works directly at the **bit level**, making it both clean and efficient.

```cpp
class Solution {
public:
    uint32_t reverseBits(uint32_t n) {
        uint32_t res = 0;
        for (int i = 0; i < 32; i++) {
            uint32_t bit = (n >> i) & 1;
            res += (bit << (31 - i));
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 3. Bit Manipulation (Optimal)

We are given a **32-bit unsigned integer** and need to **reverse its bits**.

Instead of reversing bits one-by-one, we can do this **much faster** by using a classic bit-manipulation trick called **bitwise divide and conquer**.

The key idea is:

- Reverse bits in **large blocks first**
- Then gradually reverse **smaller and smaller blocks**
- Until all individual bits are reversed

This works because reversing bits is equivalent to:

- swapping the left half with the right half
- then swapping bytes
- then nibbles (4 bits)
- then pairs
- finally single bits

Each step rearranges bits closer to their final reversed positions.

```cpp
class Solution {
public:
    uint32_t reverseBits(uint32_t n) {
        uint32_t ret = n;
        ret = (ret >> 16) | (ret << 16);
        ret = ((ret & 0xff00ff00) >> 8) | ((ret & 0x00ff00ff) << 8);
        ret = ((ret & 0xf0f0f0f0) >> 4) | ((ret & 0x0f0f0f0f) << 4);
        ret = ((ret & 0xcccccccc) >> 2) | ((ret & 0x33333333) << 2);
        ret = ((ret & 0xaaaaaaaa) >> 1) | ((ret & 0x55555555) << 1);
        return ret;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0190-reverse-bits.cpp` in the NeetCode repo)

```cpp
/*
    Reverse bits of a given integer
    Ex. n = 10011100 -> 00111001 = 57

    Shift into result & shift out of n

    Time: O(1)
    Space: O(1)
*/

class Solution {
public:
    uint32_t reverseBits(uint32_t n) {
        uint32_t result = 0;
        
        for (int i = 0; i < 32; i++) {
            result <<= 1;
            result |= n & 1;
            n >>= 1;
        }
        
        return result;
    }
};
```
