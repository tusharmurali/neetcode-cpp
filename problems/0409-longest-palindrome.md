# 409. Longest Palindrome

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/longest-palindrome/>  
- **NeetCode:** <https://neetcode.io/problems/longest-palindrome>  
- **Video:** <https://www.youtube.com/watch?v=_g9jrLuAphs>  

[← Back to index](../INDEX.md)

## 1. Hash Map

A palindrome reads the same forwards and backwards. For most characters, we need pairs: one for each side. Characters with even counts can be fully used. Characters with odd counts contribute their largest even portion, and at most one odd character can sit in the middle. We count character frequencies and sum up pairs as we find them.

```cpp
class Solution {
public:
    int longestPalindrome(string s) {
        unordered_map<char, int> count;
        int res = 0;

        for (char c : s) {
            count[c]++;
            if (count[c] % 2 == 0) {
                res += 2;
            }
        }

        for (auto& [ch, cnt] : count) {
            if (cnt % 2 == 1) {
                res += 1;
                break;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(m)$

> Where $n$ is the length of the given string, and $m$ is the number of distinct characters in the string.

## 2. Hash Map (Optimal)

We can simplify the check for the middle character. If the total count of paired characters is less than the string length, it means at least one character has an odd count, so we can place one in the middle. This eliminates the need for a separate loop to check for odd counts.

```cpp
class Solution {
public:
    int longestPalindrome(string s) {
        unordered_map<char, int> count;
        int res = 0;

        for (char c : s) {
            count[c]++;
            if (count[c] % 2 == 0) {
                res += 2;
            }
        }

        return res + (res < s.size());
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(m)$

> Where $n$ is the length of the given string, and $m$ is the number of distinct characters in the string.

## 3. Hash Set

Instead of counting exact frequencies, we only need to know if a character has been seen an odd number of times. A set works perfectly: add a character when first seen, remove it when seen again (forming a pair). Each removal represents a pair. At the end, if the set is non-empty, we can use one character as the center.

```cpp
class Solution {
public:
    int longestPalindrome(string s) {
        unordered_set<char> seen;
        int res = 0;

        for (char c : s) {
            if (seen.count(c)) {
                seen.erase(c);
                res += 2;
            } else {
                seen.insert(c);
            }
        }

        return seen.empty() ? res : res + 1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(m)$

> Where $n$ is the length of the given string, and $m$ is the number of distinct characters in the string.

## 4. Bitmask

Since we're only dealing with lowercase and uppercase English letters (52 total), we can use two 32-bit integers as bitmasks instead of a set. Each bit represents whether that character has been seen an odd number of times. Toggling a bit (XOR) when we see a character tracks odd/even status. When a bit flips from 1 to 0, we found a pair.

```cpp
class Solution {
public:
    int longestPalindrome(string s) {
        int mask1 = 0; // [a - z]
        int mask2 = 0; // [A - Z]
        int res = 0;

        for (char c : s) {
            if ('a' <= c && c <= 'z') {
                int bit = 1 << (c - 'a');
                if (mask1 & bit) {
                    res += 2;
                }
                mask1 ^= bit;
            } else {
                int bit = 1 << (c - 'A');
                if (mask2 & bit) {
                    res += 2;
                }
                mask2 ^= bit;
            }
        }

        return (mask1 || mask2) ? res + 1 : res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
