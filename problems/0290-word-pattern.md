# 290. Word Pattern

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/word-pattern/>  
- **NeetCode:** <https://neetcode.io/problems/word-pattern>  
- **Video:** <https://www.youtube.com/watch?v=W_akoecmCbM>  

[← Back to index](../INDEX.md)

## 1. Two Hash Maps

A valid pattern match requires a bijection (one-to-one correspondence) between pattern characters and words. Each character must map to exactly one word, and each word must map to exactly one character. Using two hash maps allows us to verify both directions of this mapping simultaneously as we iterate through the `pattern` and `words`.

```cpp
class Solution {
public:
    bool wordPattern(string pattern, string s) {
        vector<string> words;
        string word;
        stringstream ss(s);
        while (ss >> word) {
            words.push_back(word);
        }

        if (pattern.length() != words.size()) {
            return false;
        }

        unordered_map<char, string> charToWord;
        unordered_map<string, char> wordToChar;

        for (int i = 0; i < pattern.length(); i++) {
            char c = pattern[i];
            string& w = words[i];

            if (charToWord.count(c) && charToWord[c] != w) {
                return false;
            }
            if (wordToChar.count(w) && wordToChar[w] != c) {
                return false;
            }

            charToWord[c] = w;
            wordToChar[w] = c;
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(m)$

> Where $n$ is the length of the string $pattern$ and $m$ is the length of the string $s$.

## 2. Two Hash Maps (Optimal)

Instead of storing the actual mapping, we store the index where each character or word was last seen. If a character and word form a valid pair, they should always have been last seen at the same index. This elegant approach uses the index as a signature that both the `character` and `word` must share to be valid mappings.

```cpp
class Solution {
public:
    bool wordPattern(string pattern, string s) {
        unordered_map<char, int> charToWord;
        unordered_map<string, int> wordToChar;
        istringstream in(s);
        int i = 0, n = pattern.size();
        for (string word; in >> word; ++i) {
            if (i == n || charToWord[pattern[i]] != wordToChar[word]) {
                return false;
            }
            charToWord[pattern[i]] = wordToChar[word] = i + 1;
        }
        return i == n;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(m)$

> Where $n$ is the length of the string $pattern$ and $m$ is the length of the string $s$.

## 3. Hash Set

We can use a hash map to track character to word mappings and a hash set to track which words have already been assigned to some character. When we encounter a new `character`, we check if its corresponding `word` is already used by another character. This ensures the bijection property using less memory than two full maps.

```cpp
class Solution {
public:
    bool wordPattern(string pattern, string s) {
        stringstream ss(s);
        string word;
        vector<string> words;

        while (ss >> word) {
            words.push_back(word);
        }

        if (pattern.length() != words.size()) return false;

        unordered_map<char, int> charToWord;
        set<string> store;

        for (int i = 0; i < pattern.length(); i++) {
            char c = pattern[i];

            if (charToWord.count(c)) {
                if (words[charToWord[c]] != words[i]) {
                    return false;
                }
            } else {
                if (store.count(words[i])) {
                    return false;
                }
                charToWord[c] = i;
                store.insert(words[i]);
            }
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(m)$

> Where $n$ is the length of the string $pattern$ and $m$ is the length of the string $s$.

## 4. Single Hash Map

Using only one hash map from character to index, we can still verify the bijection by iterating through existing mappings when encountering a new character. Since there are at most 26 lowercase letters, this iteration is bounded by a constant. We check if any existing `character` already maps to the current `word`, ensuring no two characters share the same word.

```cpp
class Solution {
public:
    bool wordPattern(string pattern, string s) {
        vector<string> words;
        string word;
        stringstream ss(s);
        while (ss >> word) {
            words.push_back(word);
        }

        if (pattern.size() != words.size()) {
            return false;
        }

        unordered_map<char, int> charToWord;
        for (int i = 0; i < pattern.size(); ++i) {
            char c = pattern[i];
            const string& w = words[i];

            if (charToWord.count(c)) {
                if (words[charToWord[c]] != w) {
                    return false;
                }
            } else {
                for (const auto& [key, val] : charToWord) {
                    if (words[val] == w) {
                        return false;
                    }
                }
                charToWord[c] = i;
            }
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(m)$

> Where $n$ is the length of the string $pattern$ and $m$ is the length of the string $s$.

## Standalone solution file (`cpp/0290-word-pattern.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    bool wordPattern(string pattern, string str) {
        vector<int> pat_map (26, 0);
        unordered_map<string,int> str_map;
        int i=0, n = pattern.size();
        istringstream ss (str);
        string token;
        
        for(string token; ss >> token; ++i) {
            if(i == n || pat_map[pattern[i]-'a'] != str_map[token]) return false;
            
            // 1-based indexing since map assigns 0 as a default value for keys not found.
            pat_map[pattern[i]-'a'] = str_map[token] = i+1;
        }
        
        return i == n;
    }
};
```
