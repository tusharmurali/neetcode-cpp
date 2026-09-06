# 383. Ransom Note

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/ransom-note/>  
- **NeetCode:** <https://neetcode.io/problems/ransom-note>  
- **Video approach:** 2. Count Frequency (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each character in the ransom note, we search for a matching character in the magazine. When found, we remove that character from the magazine so it cannot be reused. If any character cannot be found, we know the ransom note cannot be constructed.

```cpp
class Solution {
public:
    bool canConstruct(string ransomNote, string magazine) {
        vector<char> mag(magazine.begin(), magazine.end());

        for (char c : ransomNote) {
            auto it = find(mag.begin(), mag.end(), c);
            if (it == mag.end()) return false;
            mag.erase(it);
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(n)$

> Where $m$ and $n$ are the lengths of the strings $ransomNote$ and $magazine$, respectively.

## 2. Count Frequency ▶ video

Instead of searching and removing characters one by one, we can count the frequency of each character in both strings. The ransom note can be constructed if and only if the magazine contains at least as many of each character as the ransom note requires.

```cpp
class Solution {
public:
    bool canConstruct(string ransomNote, string magazine) {
        int countR[26] = {};
        int countM[26] = {};

        for (char c : ransomNote) {
            countR[c - 'a']++;
        }

        for (char c : magazine) {
            countM[c - 'a']++;
        }

        for (int i = 0; i < 26; ++i) {
            if (countM[i] < countR[i]) return false;
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

> Where $m$ and $n$ are the lengths of the strings $ransomNote$ and $magazine$, respectively.

## 3. Count Frequency (Optimal)

We can optimize further by using a single count array. First, we count all characters in the magazine. Then, as we iterate through the ransom note, we decrement the count for each character. If any count goes negative, the magazine does not have enough of that character.

```cpp
class Solution {
public:
    bool canConstruct(string ransomNote, string magazine) {
        int count[26] = {};
        for (char c : magazine) {
            count[c - 'a']++;
        }
        for (char c : ransomNote) {
            if (--count[c - 'a'] < 0) return false;
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

> Where $m$ and $n$ are the lengths of the strings $ransomNote$ and $magazine$, respectively.
