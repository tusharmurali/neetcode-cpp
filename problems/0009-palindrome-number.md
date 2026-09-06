# 9. Palindrome Number

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/palindrome-number/>  
- **NeetCode:** <https://neetcode.io/problems/palindrome-number>  
- **Video:** <https://www.youtube.com/watch?v=yubRKwixN-U>  

[← Back to index](../INDEX.md)

## 1. Convert to String

The most straightforward approach is to convert the integer to a string and check if the string is a palindrome by reversing it.

If the original string equals its reversed version, the number is a palindrome.

```cpp
class Solution {
public:
    bool isPalindrome(int x) {
        string s = to_string(x);
        string rev = s;
        reverse(rev.begin(), rev.end());
        return s == rev;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the number of digits in the given integer.

## 2. Convert to String (Optimal)

Instead of creating a reversed copy of the entire string, we can compare characters from both ends moving toward the center. This avoids the extra space needed for the reversed string.

We only need to check half the string since we compare characters in pairs.

```cpp
class Solution {
public:
    bool isPalindrome(int x) {
        string s = to_string(x);
        int n = s.length();
        for (int i = 0; i < n / 2; i++) {
            if (s[i] != s[n - i - 1]) {
                return false;
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

> Where $n$ is the number of digits in the given integer.

## 3. Reverse the Integer

Without using string conversion, we can reverse the entire integer mathematically and compare it to the original. If they are equal, the number is a palindrome.

Negative numbers cannot be palindromes because of the negative sign. We build the reversed number digit by digit using modulo and division operations.

```cpp
class Solution {
public:
    bool isPalindrome(int x) {
        if (x < 0) {
            return false;
        }

        long long rev = 0, num = x;
        while (num != 0) {
            rev = (rev * 10) + (num % 10);
            num /= 10;
        }

        return rev == x;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

> Where $n$ is the number of digits in the given integer.

## 4. Two Pointers

We can compare digits from both ends without converting to a string or reversing the entire number. The idea is to extract the leftmost and rightmost digits and compare them.

We use a divisor to extract the leftmost digit and modulo to extract the rightmost digit, then shrink the number from both ends.

```cpp
class Solution {
public:
    bool isPalindrome(int x) {
        if (x < 0) {
            return false;
        }

        long long div = 1;
        while (x >= 10 * div) {
            div *= 10;
        }

        while (x != 0) {
            if (x / div != x % 10) {
                return false;
            }
            x = (x % div) / 10;
            div /= 100;
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

> Where $n$ is the number of digits in the given integer.

## 5. Reverse Half of the Number

Reversing the entire number risks integer overflow. A clever optimization is to reverse only the second half of the number and compare it to the first half.

We keep extracting digits from the end and building the reversed half until the reversed half is greater than or equal to the remaining number. At that point, we have processed half (or just past half) of the digits.

```cpp
class Solution {
public:
    bool isPalindrome(int x) {
        if (x < 0 || (x != 0 && x % 10 == 0)) {
            return false;
        }

        int rev = 0;
        while (x > rev) {
            rev = rev * 10 + x % 10;
            x /= 10;
        }

        return x == rev || x == rev / 10;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

> Where $n$ is the number of digits in the given integer.

## Standalone solution file (`cpp/0009-palindrome-number.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    bool isPalindrome(int x) {
        if(x < 0) return false;
        
        long div = 1;
        while(x >= 10 * div)
            div *= 10;
        
        while(x) {
            int right = x % 10;
            int left = x / div;
            
            if(left != right) return false;
            
            x = (x % div) / 10;
            div = div / 100;
        }
        return true;
    }
};
```
