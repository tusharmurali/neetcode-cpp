# 1160. Find Words That Can Be Formed by Characters

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-words-that-can-be-formed-by-characters/>  
- **NeetCode:** <https://neetcode.io/problems/find-words-that-can-be-formed-by-characters>  
- **Video:** <https://www.youtube.com/watch?v=EQ5jTZdEn8Y>  

[← Back to index](../INDEX.md)

## 1. Hash Map (Two Pass)

A word can be formed from `chars` if every character in the word appears in `chars` with at least the same frequency. We first count character frequencies in `chars`, then for each word, count its character frequencies and verify that `chars` has enough of each character.

```cpp
class Solution {
public:
    int countCharacters(vector<string>& words, string chars) {
        unordered_map<char, int> count;
        for (char c : chars) {
            count[c]++;
        }
        int res = 0;
        for (const string& w : words) {
            unordered_map<char, int> curWord;
            for (char c : w) {
                curWord[c]++;
            }
            bool good = true;
            for (const auto& p : curWord) {
                if (p.second > count[p.first]) {
                    good = false;
                    break;
                }
            }
            if (good) {
                res += w.size();
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + (m * k))$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

> Where $n$ is the length of $chars$, $m$ is the number of words and $k$ is the average length of each word.

## 2. Hash Map (One Pass)

Instead of building the complete frequency map for each word first, we can check character availability on the fly. As we iterate through each character of a word, we increment its count in a temporary map and immediately check if it exceeds the available count in `chars`. This allows early termination if a word is invalid.

```cpp
class Solution {
public:
    int countCharacters(vector<string>& words, string chars) {
        unordered_map<char, int> count;
        for (char c : chars) {
            count[c]++;
        }
        int res = 0;
        for (const string& w : words) {
            unordered_map<char, int> curWord;
            bool good = true;
            for (char c : w) {
                curWord[c]++;
                if (curWord[c] > count[c]) {
                    good = false;
                    break;
                }
            }
            if (good) {
                res += w.size();
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + (m * k))$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

> Where $n$ is the length of $chars$, $m$ is the number of words and $k$ is the average length of each word.

## 3. Hash Table

Since we only have lowercase letters, we can use a fixed-size array of 26 elements instead of a hash map. This is more cache-friendly and avoids hash function overhead. We decrement counts as we use characters and reset the array for each new word using a stored original copy.

```cpp
class Solution {
public:
    int countCharacters(vector<string>& words, string chars) {
        vector<int> count(26, 0);
        for (char c : chars) {
            count[c - 'a']++;
        }

        vector<int> org = count;
        int res = 0;

        for (string& w : words) {
            bool good = true;
            for (char& c : w) {
                int i = c - 'a';
                count[i]--;
                if (count[i] < 0) {
                    good = false;
                    break;
                }
            }
            if (good) {
                res += w.length();
            }
            for (int i = 0; i < 26; i++) {
                count[i] = org[i];
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + (m * k))$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

> Where $n$ is the length of $chars$, $m$ is the number of words and $k$ is the average length of each word.
