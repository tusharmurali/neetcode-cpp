# 371. Sum of Two Integers

- **Difficulty:** Medium  
- **Pattern:** Bit Manipulation  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/sum-of-two-integers/>  
- **NeetCode:** <https://neetcode.io/problems/sum-of-two-integers>  
- **Video:** <https://www.youtube.com/watch?v=gVUrDV4tZfY>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The goal is to compute the **sum of two integers**.

In the brute force approach, we rely directly on the language’s built-in arithmetic addition operator. This is the most straightforward and intuitive solution because:

- Addition is a fundamental operation supported natively by all programming languages
- The language runtime already handles all edge cases such as:
    - negative numbers
    - carry propagation
    - integer representation

This approach focuses purely on **correctness and simplicity**, without worrying about implementation details.

```cpp
class Solution {
public:
    int getSum(int a, int b) {
        return a + b;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 2. Bit Manipulation

The problem asks us to compute the **sum of two integers without using the `+` or `-` operators**.

At the bit level, addition works using two simple ideas:

- **XOR (`^`)** gives the sum of two bits _without considering `carry`_
- **AND (`&`) + left shift** determines where a `carry` is generated

For example (single bit):

- `0 + 0 → sum = 0, carry = 0`
- `1 + 0 → sum = 1, carry = 0`
- `1 + 1 → sum = 0, carry = 1`

By repeating this logic for all bit positions, we can simulate normal addition exactly as it happens in hardware.

Because integers are stored in **fixed-width (32-bit) two's complement form**, we also need to:

- limit results to 32 bits
- correctly convert the result back if it represents a negative number

```cpp
class Solution {
public:
    int getSum(int a, int b) {
        int carry = 0, res = 0, mask = 0xFFFFFFFF;

        for (int i = 0; i < 32; i++) {
            int a_bit = (a >> i) & 1;
            int b_bit = (b >> i) & 1;
            int cur_bit = a_bit ^ b_bit ^ carry;
            carry = (a_bit + b_bit + carry) >= 2 ? 1 : 0;
            if (cur_bit) {
                res |= (1 << i);
            }
        }

        if (res > 0x7FFFFFFF) {
            res = ~(res ^ mask);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 3. Bit Manipulation (Optimal)

We need to add two integers **without using `+` or `-`**.
Binary addition can be built from two operations:

1. **Sum without `carry`**
    - `a XOR b` gives the bit-by-bit sum ignoring `carry`
      (because `1 XOR 1 = 0`, which matches sum without `carry`)

2. **`Carry` information**
    - `a AND b` tells us where both bits are `1`, which creates a `carry`
    - shifting left by 1 (`<< 1`) moves that `carry` to the next higher bit

So we can repeatedly:

- compute the `carry`
- update the partial sum using XOR
- add the `carry` again (by setting `b = carry`)

We keep doing this until there is **no `carry` left** (`b == 0`).

Because many languages use **fixed-width integers** (like 32-bit signed integers), we use a `mask` to keep only the lower 32 bits at each step. Finally, if the result represents a negative number in 32-bit two's complement form, we convert it back to a signed integer.

```cpp
class Solution {
public:
    int getSum(int a, int b) {
        while (b != 0) {
            int carry = (a & b) << 1;
            a ^= b;
            b = carry;
        }
        return a;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0371-sum-of-two-integers.cpp` in the NeetCode repo)

```cpp
/*
    Given 2 ints, return sum w/o using +/-
    Ex. a = 1 b = 2 -> 3, a = 2 b = 3 -> 5

    XOR for addition, AND for carry bit

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int getSum(int a, int b) {
        while (b != 0) {
            int carry = a & b;
            a = a ^ b;
            b = (unsigned)carry << 1;
        }
        return a;
    }
};
```
