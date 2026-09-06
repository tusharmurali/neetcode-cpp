# 67. Add Binary

- **Difficulty:** Easy  
- **Pattern:** Bit Manipulation  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/add-binary/>  
- **NeetCode:** <https://neetcode.io/problems/add-binary>  
- **Video:** <https://www.youtube.com/watch?v=keuWJ47xG8g>  

[← Back to index](../INDEX.md)

## 1. Iteration

Adding binary numbers works just like adding decimal numbers by hand, except we only have digits 0 and 1. We start from the rightmost digits (least significant bits) and add corresponding digits along with any carry from the previous position. If the sum is 2 or more, we carry 1 to the next position. We reverse both strings first to make indexing from the right easier, then build the result and reverse it at the end.

```cpp
class Solution {
public:
    string addBinary(string a, string b) {
        string res = "";
        int carry = 0;

        reverse(a.begin(), a.end());
        reverse(b.begin(), b.end());

        for (int i = 0; i < max(a.length(), b.length()); i++) {
            int digitA = i < a.length() ? a[i] - '0' : 0;
            int digitB = i < b.length() ? b[i] - '0' : 0;

            int total = digitA + digitB + carry;
            char c = (total % 2) + '0';
            res += c;
            carry = total / 2;
        }

        if (carry) {
            res += '1';
        }
        reverse(res.begin(), res.end());
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(max(m, n))$
- Space complexity: $O(m + n)$

> Where $m$ and $n$ are the lengths of the strings $a$ and $b$ respectively.

## 2. Iteration (Optimal)

Instead of reversing the strings upfront, we can use two pointers starting at the end of each string and work backward. This avoids the extra space and time needed to reverse the input strings. We continue until both pointers have moved past the beginning of their strings and no carry remains. The result is built in reverse order, so we reverse it once at the end.

```cpp
class Solution {
public:
    string addBinary(string a, string b) {
        string res = "";
        int carry = 0;

        int i = a.size() - 1, j = b.size() - 1;
        while (i >= 0 || j >= 0 || carry > 0) {
            int digitA = i >= 0 ? a[i] - '0' : 0;
            int digitB = j >= 0 ? b[j] - '0' : 0;

            int total = digitA + digitB + carry;
            res += (total % 2) + '0';
            carry = total / 2;

            i--;
            j--;
        }

        reverse(res.begin(), res.end());
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(max(m, n))$
- Space complexity: $O(max(m, n))$

> Where $m$ and $n$ are the lengths of the strings $a$ and $b$ respectively.

## Standalone solution file (`cpp/0067-add-binary.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    string addBinary(string a, string b) {
        string res;
        int maxLen = a.size() > b.size() ? a.size() : b.size();
        unsigned int carry = 0;

        for(int i = 0; i < maxLen; i++)
        {
            unsigned int bitA = i < a.size() ? a[a.size() - i - 1] - '0' : 0;
            unsigned int bitB = i < b.size() ? b[b.size() - i - 1] - '0' : 0;

            unsigned int total = bitA + bitB + carry;
            char sum = '0' + total % 2;
            carry = total / 2;

            // Add to the beginning of the string
            res.insert(0, 1, sum);
        }

        if(carry)
        {
            res.insert(0, 1, '1');
        }

        return res;
    }
};
```
