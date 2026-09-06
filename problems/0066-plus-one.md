# 66. Plus One

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/plus-one/>  
- **NeetCode:** <https://neetcode.io/problems/plus-one>  
- **Video:** <https://www.youtube.com/watch?v=jIaA8boiG1s>  

[← Back to index](../INDEX.md)

## 1. Recursion

We are given a number represented as an array of digits, and we need to **add one** to this number.

The challenge comes from handling the **carry**:

- If the last digit is less than `9`, we can simply increment it.
- If the last digit is `9`, it becomes `0` and we need to carry `+1` to the remaining digits.

This recursive solution mirrors how addition works by hand:

- handle the **last digit**
- if there is a carry, recursively solve the smaller subproblem (all digits except the last)
- build the final result while returning from recursion

```cpp
class Solution {
public:
    vector<int> plusOne(vector<int>& digits) {
        if (digits.empty())
            return {1};

        if (digits.back() < 9) {
            digits.back() += 1;
            return digits;
        } else {
            digits.pop_back();
            vector<int> result = plusOne(digits);
            result.push_back(0);
            return result;
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Iteration - I

We are given a number as an array of digits and need to **add one** to it.

The main idea is to simulate manual addition starting from the **least significant digit** (the last digit).
Since addition naturally moves from right to left, this solution:

- reverses the array so we can process digits from left to right
- keeps a variable `one` to represent the **carry** (initially `1`)
- continues updating digits until the carry becomes `0`

This avoids recursion and handles all carry cases, including when the number consists entirely of `9`s (like `[9,9,9]`).

```cpp
class Solution {
public:
    vector<int> plusOne(vector<int>& digits) {
        int one = 1;
        int i = 0;
        reverse(digits.begin(), digits.end());

        while (one) {
            if (i < digits.size()) {
                if (digits[i] == 9) {
                    digits[i] = 0;
                } else {
                    digits[i] += 1;
                    one = 0;
                }
            } else {
                digits.push_back(one);
                one = 0;
            }
            i++;
        }
        reverse(digits.begin(), digits.end());
        return digits;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the language.

## 3. Iteration - II

We are given a number represented as an array of digits and need to **add one** to it.

The simplest way to do this is to simulate how addition works from **right to left**:

- start from the least significant digit
- if the digit is less than `9`, we can increment it and stop
- if the digit is `9`, it becomes `0` and we carry `+1` to the next digit on the left

If we finish processing all digits and still have a carry, it means the number was something like `[9, 9, 9]`, and we need to add a new leading `1`.

```cpp
class Solution {
public:
    vector<int> plusOne(vector<int>& digits) {
        int n = digits.size();
        for (int i = n - 1; i >= 0; i--) {
            if (digits[i] < 9) {
                digits[i]++;
                return digits;
            }
            digits[i] = 0;
        }
        vector<int> result(n + 1);
        result[0] = 1;
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0066-plus-one.cpp` in the NeetCode repo)

```cpp
/*
    Given large int as an array, add 1 (consider carry)
    Ex. digits = [1,2,3] -> [1,2,4]

    From right to left, keep carrying until digit < 9, add 1

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    vector<int> plusOne(vector<int>& digits) {
        for (int i = digits.size() - 1; i >= 0; i--) {
            if (digits[i] < 9) {
                digits[i]++;
                return digits;
            }
            digits[i] = 0;
        }
        
        digits[0] = 1;
        digits.push_back(0);
        return digits;
    }
};
```
