# 2108. Find First Palindromic String in the Array

- **Difficulty:** Easy  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-first-palindromic-string-in-the-array/>  
- **NeetCode:** <https://neetcode.io/problems/find-first-palindromic-string-in-the-array>  
- **Video:** <https://www.youtube.com/watch?v=4JA5MW772N0>  

[← Back to index](../INDEX.md)

## 1. Reverse String

A palindrome reads the same forwards and backwards. The simplest way to check this is to reverse the string and compare it to the original. If they match, it's a palindrome. We iterate through the array and return the first string that passes this check.

```cpp
class Solution {
public:
    string firstPalindrome(vector<string>& words) {
        for (const string& w : words) {
            string rev = w;
            reverse(rev.begin(), rev.end());
            if (w == rev) {
                return w;
            }
        }
        return "";
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(m)$

> Where $n$ is the size of the string array $words$ and $m$ is the average length of a word in the array.

## 2. Two Pointers

Instead of creating a reversed copy (which uses extra space), we can check if a string is a palindrome in place using two pointers. One pointer starts at the beginning, the other at the end. If all corresponding characters match as the pointers move toward each other, the string is a palindrome. This avoids the extra memory needed to store the reversed string.

```cpp
class Solution {
public:
    string firstPalindrome(vector<string>& words) {
        for (const string& w : words) {
            int l = 0, r = w.length() - 1;
            while (w[l] == w[r]) {
                if (l >= r) return w;
                l++;
                r--;
            }
        }
        return "";
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(1)$ extra space.

> Where $n$ is the size of the string array $words$ and $m$ is the average length of a word in the array.
