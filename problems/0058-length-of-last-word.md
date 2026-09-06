# 58. Length of Last Word

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/length-of-last-word/>  
- **NeetCode:** <https://neetcode.io/problems/length-of-last-word>  
- **Video:** <https://www.youtube.com/watch?v=KT9rltZTybQ>  

[← Back to index](../INDEX.md)

## 1. Iteration - I

We need to find the length of the last word, where words are separated by spaces. Trailing spaces complicate matters since the last word might not be at the very end of the string. By scanning forward, we track the current word's length and reset it when we encounter a new word after spaces.

```cpp
class Solution {
public:
    int lengthOfLastWord(string s) {
        int length = 0, i = 0;
        while (i < s.length()) {
            if (s[i] == ' ') {
                while (i < s.length() && s[i] == ' ') {
                    i++;
                }
                if (i == s.length()) {
                    return length;
                }
                length = 0;
            } else {
                length++;
                i++;
            }
        }
        return length;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Iteration - II

Scanning from the end is more direct since we only care about the last word. First skip any trailing spaces, then count characters until we hit a space or the beginning of the string. This avoids processing earlier parts of the string entirely.

```cpp
class Solution {
public:
    int lengthOfLastWord(string s) {
        int n = s.length();
        int i = n - 1, length = 0;
        while (s[i] == ' ') i--;
        while (i >= 0 && s[i] != ' ') {
            i--;
            length++;
        }
        return length;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 3. Built-In Function

Most languages provide string manipulation functions that handle splitting and trimming. By splitting the string on spaces and taking the last non-empty segment, we get the last word directly. This trades some efficiency for code simplicity and readability.

```cpp
class Solution {
public:
    int lengthOfLastWord(string s) {
        s.erase(s.find_last_not_of(' ') + 1);
        return s.substr(s.find_last_of(' ') + 1).length();
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0058-length-of-last-word.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    /*
    Approach: 
    Traverse from end to the first whitespace character and count the number of letters.
    Return the count as our pointer hits the whitespace character.
    
    Time complexity: O(n)
    Space complexity: O(1)
    */    
    int lengthOfLastWord(string s) {
        int n = s.length();
        
        int ptr = n-1;
        while(ptr >= 0 && s[ptr] == ' ') ptr--; /* Skip the trailing whitespaces */
        
        int len = 0;
        while(ptr >= 0 && s[ptr--] != ' ') len++; /* Counting the letters in the last word */
        return len;
    }
};
```
