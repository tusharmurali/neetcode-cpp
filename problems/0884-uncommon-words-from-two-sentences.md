# 884. Uncommon Words from Two Sentences

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/uncommon-words-from-two-sentences/>  
- **NeetCode:** <https://neetcode.io/problems/uncommon-words-from-two-sentences>  
- **Video:** <https://www.youtube.com/watch?v=24IYW1kQdYU>  

[← Back to index](../INDEX.md)

## 1. Hash Map - I

A word is uncommon if it appears exactly once across both sentences. We can combine both sentences and count the frequency of each word. Any word with a count of 1 is uncommon.

```cpp
class Solution {
public:
    vector<string> uncommonFromSentences(string s1, string s2) {
        unordered_map<string, int> count;
        istringstream ss(s1 + " " + s2);
        string w;
        while (ss >> w) {
            count[w]++;
        }

        vector<string> res;
        for (auto& [word, freq] : count) {
            if (freq == 1) {
                res.push_back(word);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$

> Where $n$ and $m$ are the lengths of the strings $s1$ and $s2$, respectively.

## 2. Hash Map - II

This is a more concise version of the same approach. We use built-in functions like `Counter` (in Python) or stream operations (in Java) to reduce boilerplate while maintaining the same logic.

```cpp
class Solution {
public:
    vector<string> uncommonFromSentences(string s1, string s2) {
        unordered_map<string, int> count;
        istringstream ss(s1 + " " + s2);
        string w;
        while (ss >> w) {
            count[w]++;
        }

        vector<string> res;
        for (auto& [w, c] : count) {
            if (c == 1) {
                res.push_back(w);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$

> Where $n$ and $m$ are the lengths of the strings $s1$ and $s2$, respectively.
