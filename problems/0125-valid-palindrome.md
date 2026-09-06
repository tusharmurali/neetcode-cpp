# 125. Valid Palindrome

- **Difficulty:** Easy  
- **Pattern:** Two Pointers  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/valid-palindrome/>  
- **NeetCode:** <https://neetcode.io/problems/is-palindrome>  
- **Video:** <https://www.youtube.com/watch?v=jJXJ16kPFWg>  

[← Back to index](../INDEX.md)

## 1. Reverse String

To check if a string is a palindrome, we only care about letters and digits—everything else can be ignored.  
We can build a cleaned version of the string that contains only alphanumeric characters, all converted to lowercase for consistency.  
Once we have this cleaned string, the problem becomes very simple:  
a string is a palindrome if it is exactly the same as its reverse.

```cpp
class Solution {
public:
    bool isPalindrome(string s) {
        string newStr = "";
        for (char c : s) {
            if (isalnum(c)) {
                newStr += tolower(c);
            }
        }
        return newStr == string(newStr.rbegin(), newStr.rend());
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Two Pointers

Instead of building a new string, we can check the palindrome directly in-place using two pointers.  
One pointer starts at the beginning (`l`) and the other at the end (`r`).  
We move both pointers inward, skipping any characters that are not letters or digits.  
Whenever both pointers point to valid characters, we compare them in lowercase form.  
If at any point they differ, the string is not a palindrome.  
This method avoids extra space and keeps the logic simple and efficient.

```cpp
class Solution {
public:
    bool isPalindrome(string s) {
        int l = 0, r = s.length() - 1;

        while (l < r) {
            while (l < r && !alphaNum(s[l])) {
                l++;
            }
            while (r > l && !alphaNum(s[r])) {
                r--;
            }
            if (tolower(s[l]) != tolower(s[r])) {
                return false;
            }
            l++; r--;
        }
        return true;
    }

    bool alphaNum(char c) {
        return (c >= 'A' && c <= 'Z' ||
                c >= 'a' && c <= 'z' ||
                c >= '0' && c <= '9');
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0125-valid-palindrome.cpp` in the NeetCode repo)

```cpp
/*
    Given a string s, return true if it's a palindrome
    Ex. s = "A man, a plan, a canal: Panama" -> true

    2 pointers, outside in, skip non-letters & compare

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    bool isPalindrome(string s) {
        int i = 0;
        int j = s.size() - 1;
        
        while (i < j) {
            while (!isalnum(s[i]) && i < j) {
                i++;
            }
            while (!isalnum(s[j]) && i < j) {
                j--;
            }
            if (tolower(s[i]) != tolower(s[j])) {
                return false;
            }
            i++;
            j--;
        }
        
        return true;
    }
};
```
