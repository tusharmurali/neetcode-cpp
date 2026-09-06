# 242. Valid Anagram

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** Blind 75, NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/valid-anagram/>  
- **NeetCode:** <https://neetcode.io/problems/is-anagram>  
- **Video:** <https://www.youtube.com/watch?v=9UtInBqnCgA>  
- **Video approach:** 2. Hash Map  

[← Back to index](../INDEX.md)

## 1. Sorting

If two strings are anagrams, they must contain exactly the same characters with the same frequencies.  
By sorting both strings, all characters will be arranged in a consistent order.  
If the two sorted strings are identical, then every character and its count match, which means the strings are anagrams.

```cpp
class Solution {
public:
    bool isAnagram(string s, string t) {
        if (s.length() != t.length()) {
            return false;
        }

        sort(s.begin(), s.end());
        sort(t.begin(), t.end());
        return s == t;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n + m \log m)$
- Space complexity: $O(1)$ or $O(n + m)$ depending on the sorting algorithm.

> Where $n$ is the length of string $s$ and $m$ is the length of string $t$.

## 2. Hash Map ▶ video

If two strings are anagrams, they must use the same characters with the same frequencies.  
Instead of sorting, we can count how many times each character appears in both strings.  
By using two hash maps (or dictionaries), we track the frequency of every character in each string.  
If both frequency maps match exactly, then the strings contain the same characters with same frequencies, meaning they are anagrams.

```cpp
class Solution {
public:
    bool isAnagram(string s, string t) {
        if (s.length() != t.length()) {
            return false;
        }

        unordered_map<char, int> countS;
        unordered_map<char, int> countT;
        for (int i = 0; i < s.length(); i++) {
            countS[s[i]]++;
            countT[t[i]]++;
        }
        return countS == countT;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

> Where $n$ is the length of string $s$ and $m$ is the length of string $t$.

## 3. Hash Table (Using Array)

Since the problem guarantees lowercase English letters, we can use a fixed-size array of length `26` to count character frequencies instead of a hash map.
As we iterate through both strings simultaneously, we increment the count for each character in `s` and decrement the count for each character in `t`.
If the strings are anagrams, every increment will be matched by a corresponding decrement, and all values in the array will end at `0`.
This approach is efficient because it avoids hashing and uses constant space.

```cpp
class Solution {
public:
    bool isAnagram(string s, string t) {
        if (s.length() != t.length()) {
            return false;
        }

        vector<int> count(26, 0);
        for (int i = 0; i < s.length(); i++) {
            count[s[i] - 'a']++;
            count[t[i] - 'a']--;
        }

        for (int val : count) {
            if (val != 0) {
                return false;
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

> Where $n$ is the length of string $s$ and $m$ is the length of string $t$.

## Standalone solution file (`cpp/0242-valid-anagram.cpp` in the NeetCode repo)

```cpp
// hashmap solution, similar to neetcode python implementation

class Solution {
public:
    bool isAnagram(string s, string t) {
        if(s.size() != t.size()) return false;
        
        unordered_map<char, int> smap;
        unordered_map<char, int> tmap;
        
        for(int i = 0; i < s.size(); i++){
            smap[s[i]]++;
            tmap[t[i]]++;
        }

        for (auto const& [key, value] : smap) {
          if (value != tmap[key]) {
            return false;
          }
        }
        return true;
    }
};
```
