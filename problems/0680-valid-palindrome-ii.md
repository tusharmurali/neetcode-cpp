# 680. Valid Palindrome II

- **Difficulty:** Easy  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/valid-palindrome-ii/>  
- **NeetCode:** <https://neetcode.io/problems/valid-palindrome-ii>  
- **Video:** <https://www.youtube.com/watch?v=JrxRYBwG6EI>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest approach is to check every possibility. First, check if the string is already a palindrome. If not, try removing each character one at a time and check if the resulting string becomes a palindrome. If any removal produces a palindrome, return `true`. This guarantees we find a solution if one exists, but it requires checking up to `n` different strings.

```cpp
class Solution {
public:
    bool validPalindrome(string s) {
        if (isPalindrome(s)) {
            return true;
        }

        for (int i = 0; i < s.size(); i++) {
            string newS = s.substr(0, i) + s.substr(i + 1);
            if (isPalindrome(newS)) {
                return true;
            }
        }

        return false;
    }

private:
    bool isPalindrome(const string& s) {
        int left = 0, right = s.size() - 1;
        while (left < right) {
            if (s[left] != s[right]) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Two Pointers

Instead of blindly trying every removal, we can be smarter. Use two pointers starting from both ends of the string and move them inward. As long as characters match, keep going. When we find a mismatch, we know exactly where the problem is. At this point, we have only two choices: remove the left character or remove the right character. We check if either choice results in a palindrome for the remaining substring.

```cpp
class Solution {
public:
    bool validPalindrome(string s) {
        int l = 0, r = s.size() - 1;

        while (l < r) {
            if (s[l] != s[r]) {
                return isPalindrome(s.substr(0, l) + s.substr(l + 1)) ||
                       isPalindrome(s.substr(0, r) + s.substr(r + 1));
            }
            l++;
            r--;
        }

        return true;
    }

private:
    bool isPalindrome(string s) {
        int l = 0, r = s.length() - 1;
        while (l < r) {
            if (s[l] != s[r]) {
                return false;
            }
            l++;
            r--;
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Two Pointers (Optimal)

The previous two-pointer solution creates new substrings, which costs `O(n)` space. We can optimize this by passing index bounds to our palindrome check function instead of creating new strings. This way, we check the same characters without allocating extra memory. The logic remains identical: find the first mismatch, then verify if skipping either character leads to a valid palindrome.

```cpp
class Solution {
public:
    bool validPalindrome(string s) {
        int l = 0, r = s.size() - 1;

        while (l < r) {
            if (s[l] != s[r]) {
                return isPalindrome(s, l + 1, r) ||
                       isPalindrome(s, l, r - 1);
            }
            l++;
            r--;
        }

        return true;
    }

private:
    bool isPalindrome(const string& s, int l, int r) {
        while (l < r) {
            if (s[l] != s[r]) {
                return false;
            }
            l++;
            r--;
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0680-valid-palindrome-ii.cpp` in the NeetCode repo)

```cpp
class Solution {
private:
    bool validPalindromeUtil(string s, int i, int j) {
        while(i < j)
            if(s[i] == s[j]) {
                i += 1;
                j -= 1;
            } else
                return false;
        return true;
    }
public:
    bool validPalindrome(string s) {
        int i = 0, j = s.length() - 1;
        
        while(i < j)
            if(s[i] == s[j]) {
                i += 1;
                j -= 1;
            } else
                return validPalindromeUtil(s, i + 1, j) || validPalindromeUtil(s, i, j - 1);
        return true;
    }
};
```
