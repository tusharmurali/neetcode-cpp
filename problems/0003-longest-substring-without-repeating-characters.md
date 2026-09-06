# 3. Longest Substring Without Repeating Characters

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/longest-substring-without-repeating-characters/>  
- **NeetCode:** <https://neetcode.io/problems/longest-substring-without-duplicates>  
- **Video:** <https://www.youtube.com/watch?v=wiGpQwVHdE0>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The brute-force idea is to try starting a substring at every index and keep extending it until we see a repeated character.  
For each starting point, we use a set to track the characters we’ve seen so far.  
As soon as a duplicate appears, that substring can’t grow anymore, so we stop and record its length.  
By doing this for every index, we are guaranteed to find the longest valid substring, though the approach is slow.

```cpp
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        int res = 0;
        for (int i = 0; i < s.size(); i++) {
            unordered_set<char> charSet;
            for (int j = i; j < s.size(); j++) {
                if (charSet.find(s[j]) != charSet.end()) {
                    break;
                }
                charSet.insert(s[j]);
            }
            res = max(res, (int)charSet.size());
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(m)$

> Where $n$ is the length of the string and $m$ is the total number of unique characters in the string.

## 2. Sliding Window

Instead of restarting at every index like brute force, we can keep one **window** that always has _unique_ characters.
We expand the window by moving the `right` pointer.
If we ever see a repeated character, we shrink the window from the `left` until the duplicate is removed.
This way, the window always represents a valid substring, and we track its maximum size.
It's efficient because each character is added and removed at most once.

```cpp
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        unordered_set<char> charSet;
        int l = 0;
        int res = 0;

        for (int r = 0; r < s.size(); r++) {
            while (charSet.find(s[r]) != charSet.end()) {
                charSet.erase(s[l]);
                l++;
            }
            charSet.insert(s[r]);
            res = max(res, r - l + 1);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(m)$

> Where $n$ is the length of the string and $m$ is the total number of unique characters in the string.

## 3. Sliding Window (Optimal)

Instead of removing characters one by one when we see a repeat, we can **jump the `left` pointer** directly to the correct position.
We keep a map that stores the last index where each character appeared.
When a character repeats, the earliest valid starting point moves to **one position after** its previous occurrence.
This lets us adjust the window in one step and always keep it valid, making the approach fast and clean.

```cpp
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        unordered_map<char, int> mp;
        int l = 0, res = 0;

        for (int r = 0; r < s.size(); r++) {
            if (mp.find(s[r]) != mp.end()) {
                l = max(mp[s[r]] + 1, l);
            }
            mp[s[r]] = r;
            res = max(res, r - l + 1);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(m)$

> Where $n$ is the length of the string and $m$ is the total number of unique characters in the string.

## Standalone solution file (`cpp/0003-longest-substring-without-repeating-characters.cpp` in the NeetCode repo)

```cpp
/*
    Given string, find longest substring w/o repeating chars
    Ex. s = "abcabcbb" -> 3 "abc", s = "bbbbb" -> 1 "b"

    Sliding window, expand if unique, contract if duplicate

    Time: O(n)
    Space: O(n)
*/
/*
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        unordered_set<char> letters;
        
        int i = 0;
        int j = 0;
        
        int result = 0;
        
        while (j < s.size()) {
            if (letters.find(s[j]) == letters.end()) {
                letters.insert(s[j]);
                result = max(result, j - i + 1);
                j++;
            } else {
                letters.erase(s[i]);
                i++;
            }
        }
        
        return result;
    }
};
*/
// Same solution as above with the same amount of total iterations.
// Above solution: no inner loop, but the "j" variable is not increased at each iteration
// Below: inner loop increasing "i", outer loop increasing "j".
class Solution {
public:
    int lengthOfLongestSubstring(string& s) {
        unordered_set<char> chars;
        int maxSize = 0;
        int i = 0, j = 0;
        while (j < s.size()){
            while (chars.find(s[j]) != chars.end()){
                chars.erase(s[i]);
                ++i;
            }
            maxSize = max(maxSize, j - i + 1);
            chars.insert(s[j]);
            ++j;
        }
        return maxSize;
    }
};
```
