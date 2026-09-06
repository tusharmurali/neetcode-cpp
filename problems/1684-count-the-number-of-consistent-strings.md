# 1684. Count the Number of Consistent Strings

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/count-the-number-of-consistent-strings/>  
- **NeetCode:** <https://neetcode.io/problems/count-the-number-of-consistent-strings>  
- **Video:** <https://www.youtube.com/watch?v=CFa2TgIHMN0>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A string is consistent if every character in it appears in the `allowed` string. The straightforward approach is to check each word character by character. For each character, we scan through the `allowed` string to see if it exists. If any character is not found, the word is inconsistent.

```cpp
class Solution {
public:
    int countConsistentStrings(string allowed, vector<string>& words) {
        int res = 0;

        for (string& w : words) {
            bool flag = true;
            for (char c : w) {
                if (allowed.find(c) == string::npos) {
                    flag = false;
                    break;
                }
            }
            res += flag;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m * l)$
- Space complexity: $O(1)$

> Where $n$ is the number of words, $m$ is the length of the string $allowed$, and $l$ is the length of the longest word.

## 2. Hash Set

The brute force approach is slow because we scan through `allowed` for every character lookup. We can speed this up by storing all allowed characters in a hash set, which provides O(1) average lookup time. Instead of counting consistent words, we can start with the total count and subtract whenever we find an inconsistent word.

```cpp
class Solution {
public:
    int countConsistentStrings(string allowed, vector<string>& words) {
        unordered_set<char> allowedSet(allowed.begin(), allowed.end());

        int res = words.size();
        for (string& w : words) {
            for (char c : w) {
                if (allowedSet.find(c) == allowedSet.end()) {
                    res--;
                    break;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * l + m)$
- Space complexity: $O(m)$

> Where $n$ is the number of words, $m$ is the length of the string $allowed$, and $l$ is the length of the longest word.

## 3. Boolean Array

Since we are only dealing with lowercase English letters (26 characters), we can use a boolean array of size 26 instead of a hash set. Each index represents a letter (`'a' = 0`, `'b' = 1`, ..., `'z' = 25`). This provides the same O(1) lookup time as a hash set but with slightly better constant factors due to simpler memory access patterns.

```cpp
class Solution {
public:
    int countConsistentStrings(string allowed, vector<string>& words) {
        bool allowedArr[26] = {};
        for (char c : allowed) {
            allowedArr[c - 'a'] = true;
        }

        int res = words.size();
        for (const string& w : words) {
            for (char c : w) {
                if (!allowedArr[c - 'a']) {
                    res--;
                    break;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * l + m)$
- Space complexity: $O(m)$

> Where $n$ is the number of words, $m$ is the length of the string $allowed$, and $l$ is the length of the longest word.

## 4. Bitmask

We can compress the boolean array into a single 32-bit integer using bit manipulation. Each bit position represents whether a character is allowed (bit `i` represents the character `'a' + i`). This approach uses constant space (just one integer) and leverages fast bitwise operations for lookups.

```cpp
class Solution {
public:
    int countConsistentStrings(string allowed, vector<string>& words) {
        int bitMask = 0;
        for (char c : allowed) {
            bitMask |= (1 << (c - 'a'));
        }

        int res = words.size();
        for (const string& w : words) {
            for (char c : w) {
                int bit = 1 << (c - 'a');
                if ((bit & bitMask) == 0) {
                    res--;
                    break;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * l + m)$
- Space complexity: $O(1)$

> Where $n$ is the number of words, $m$ is the length of the string $allowed$, and $l$ is the length of the longest word.
