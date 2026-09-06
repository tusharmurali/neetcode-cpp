# 1544. Make The String Great

- **Difficulty:** Easy  
- **Pattern:** Stack  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/make-the-string-great/>  
- **NeetCode:** <https://neetcode.io/problems/make-the-string-great>  
- **Video:** <https://www.youtube.com/watch?v=10tBWNjzvtw>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A "bad" pair consists of the same letter in different cases adjacent to each other (like "aA" or "Aa"). We repeatedly scan the string looking for such pairs. When we find one, we remove both characters and restart the scan since removing a pair might create a new bad pair from previously non-adjacent characters.

```cpp
class Solution {
public:
    string makeGood(string s) {
        int n = s.length();
        int i = 0;
        while (i < n) {
            if (i > 0 && s[i] != s[i - 1] && tolower(s[i]) == tolower(s[i - 1])) {
                s = s.substr(0, i - 1) + s.substr(i + 1);
                n -= 2;
                i -= 2;
            }
            i++;
        }
        return s;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Stack - I

A stack naturally handles the "undo" pattern we need. As we process each character, we compare it with the top of the stack. If they form a bad pair (same letter, different cases), we pop the stack, effectively removing both characters. Otherwise, we push the current character. This handles cascading removals automatically.

```cpp
class Solution {
public:
    string makeGood(string s) {
        string stack;
        for (char c : s) {
            if (!stack.empty() && stack.back() != c &&
                tolower(stack.back()) == tolower(c)) {
                stack.pop_back();
            } else {
                stack.push_back(c);
            }
        }
        return stack;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Stack - II

We can simplify the bad pair check using ASCII values. In ASCII, the difference between a lowercase letter and its uppercase counterpart is exactly `32` (e.g., 'a' is 97 and 'A' is 65). So if the absolute difference between two characters is `32`, they are the same letter in different cases.

```cpp
class Solution {
public:
    string makeGood(string s) {
        string stack;
        for (char& c : s) {
            if (!stack.empty() && abs(stack.back() - c) == 32) {
                stack.pop_back();
            } else {
                stack.push_back(c);
            }
        }
        return stack;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Two Pointers

Instead of using extra space for a stack, we can simulate it in-place using two pointers. The left pointer `l` represents the "top" of our virtual stack, while the right pointer `r` scans through the input. Characters before position `l` form our result. When we find a bad pair, we "pop" by decrementing `l`.

```cpp
class Solution {
public:
    string makeGood(string s) {
        int l = 0;
        for (int r = 0; r < s.length(); r++) {
            if (l > 0 && abs(s[r] - s[l - 1]) == 32) {
                l--;
            } else {
                s[l++] = s[r];
            }
        }
        return s.substr(0, l);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the language.
