# 205. Isomorphic Strings

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/isomorphic-strings/>  
- **NeetCode:** <https://neetcode.io/problems/isomorphic-strings>  
- **Video:** <https://www.youtube.com/watch?v=7yF-U1hLEqQ>  

[← Back to index](../INDEX.md)

## 1. Hash Map (Two Pass)

Two strings are isomorphic if there's a one-to-one mapping between their characters. We need to ensure that each character in `s` maps to exactly one character in `t`, and vice versa. A single pass checking only `s -> t` mapping isn't enough because two different characters in `s` could map to the same character in `t`. By running the check twice (once for `(s, t)` and once for `(t, s)`), we guarantee the mapping is bijective.

```cpp
class Solution {
private:
    bool helper(const string& s, const string& t) {
        unordered_map<char, char> map;
        for (int i = 0; i < s.length(); i++) {
            if (map.count(s[i]) && map[s[i]] != t[i]) {
                return false;
            }
            map[s[i]] = t[i];
        }
        return true;
    }

public:
    bool isIsomorphic(string s, string t) {
        return helper(s, t) && helper(t, s);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(m)$

> Where $n$ is the length of the input string and $m$ is the number of unique characters in the strings.

## 2. Hash Map (One Pass)

We can verify both mapping directions simultaneously in a single pass. By maintaining two hash maps, one for `s -> t` and one for `t -> s`, we check at each position that neither mapping is violated. If a character in `s` was previously mapped to a different character in `t`, or if a character in `t` was previously mapped to a different character in `s`, the strings aren't isomorphic.

```cpp
class Solution {
public:
    bool isIsomorphic(string s, string t) {
        unordered_map<char, char> mapST, mapTS;

        for (int i = 0; i < s.size(); i++) {
            char c1 = s[i], c2 = t[i];

            if ((mapST.count(c1) && mapST[c1] != c2) ||
                (mapTS.count(c2) && mapTS[c2] != c1)) {
                return false;
            }

            mapST[c1] = c2;
            mapTS[c2] = c1;
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(m)$

> Where $n$ is the length of the input string and $m$ is the number of unique characters in the strings.

## Standalone solution file (`cpp/0205-isomorphic-strings.cpp` in the NeetCode repo)

```cpp
/*Given two strings s and t, determine if they are isomorphic.

Two strings s and t are isomorphic if the characters in s can be replaced to get t.

All occurrences of a character must be replaced with another character while preserving the order of characters. No two characters may map to the same character, but a character may map to itself.

 */
class Solution {
public:
    bool isIsomorphic(string s, string t) {
       unordered_map<char,vector<int>>m1;
         unordered_map<char,vector<int>>m2;
        for(int i=0;i<s.length();i++){
            m1[s[i]].push_back(i);
             m2[t[i]].push_back(i);
            
            if(m1[s[i]]!=m2[t[i]])
                return false;
        }
        return true;
        
    }
};
```
