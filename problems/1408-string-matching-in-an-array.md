# 1408. String Matching in an Array

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/string-matching-in-an-array/>  
- **NeetCode:** <https://neetcode.io/problems/string-matching-in-an-array>  
- **Video:** <https://www.youtube.com/watch?v=7K2BjgjCFDo>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each word, we check if it appears as a substring in any other word. If it does, we add it to our result. Since we need to check every word against every other word, we use two nested loops. Once we find that a word is a substring of another, we can stop checking and move to the next word.

```cpp
class Solution {
public:
    vector<string> stringMatching(vector<string>& words) {
        vector<string> res;

        for (int i = 0; i < words.size(); i++) {
            for (int j = 0; j < words.size(); j++) {
                if (i == j) {
                    continue;
                }

                if (words[j].find(words[i]) != string::npos) {
                    res.push_back(words[i]);
                    break;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * m ^ 2)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n * m)$ space for the output list.

> Where $n$ is the number of words, and $m$ is the length of the longest word.

## 2. Sorting

A shorter word can only be a substring of a longer word, never the other way around. By sorting words by length, we only need to check each word against longer words that come after it. This gives a minor optimization by reducing unnecessary comparisons, though the worst-case complexity remains the same.

```cpp
class Solution {
public:
    vector<string> stringMatching(vector<string>& words) {
        vector<string> res;
        sort(words.begin(), words.end(), [](const string& a, const string& b) {
            return a.length() < b.length();
        });

        for (int i = 0; i < words.size(); i++) {
            for (int j = i + 1; j < words.size(); j++) {
                if (words[j].find(words[i]) != string::npos) {
                    res.push_back(words[i]);
                    break;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * m ^ 2)$
- Space complexity:
    - $O(1)$ or $O(n)$ depending on the sorting algorithm.
    - $O(n * m)$ space for the output list.

> Where $n$ is the number of words, and $m$ is the length of the longest word.

## 3. Knuth-Morris-Pratt (KMP) Algorithm

Instead of using the built-in substring search, we can use the KMP algorithm which preprocesses the pattern to enable efficient matching. KMP builds a "longest proper prefix which is also suffix" (LPS) array that allows us to skip characters during mismatches rather than starting over. This improves substring matching to linear time in the combined length of the strings.

```cpp
class Solution {
public:
    vector<string> stringMatching(vector<string>& words) {
        vector<string> res;
        sort(words.begin(), words.end(), [](const string& a, const string& b) {
            return a.length() < b.length();
        });

        for (int i = 0; i < words.size(); i++) {
            for (int j = i + 1; j < words.size(); j++) {
                if (kmp(words[j], words[i]) != -1) {
                    res.push_back(words[i]);
                    break;
                }
            }
        }

        return res;
    }

private:
    int kmp(const string& word1, const string& word2) {
        vector<int> lps(word2.size(), 0);
        int prevLPS = 0, i = 1;

        while (i < word2.size()) {
            if (word2[i] == word2[prevLPS]) {
                lps[i++] = ++prevLPS;
            } else if (prevLPS == 0) {
                lps[i++] = 0;
            } else {
                prevLPS = lps[prevLPS - 1];
            }
        }

        i = 0;
        int j = 0;
        while (i < word1.size()) {
            if (word1[i] == word2[j]) {
                i++;
                j++;
            } else {
                if (j == 0) {
                    i++;
                } else {
                    j = lps[j - 1];
                }
            }

            if (j == word2.size()) {
                return i - word2.size();
            }
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * m)$
- Space complexity:
    - $O(m)$ extra space.
    - $O(1)$ or $O(n)$ space depending on the sorting algorithm.
    - $O(n * m)$ space for the output list.

> Where $n$ is the number of words, and $m$ is the length of the longest word.

## 4. Rabin-Karp Algorithm (Rolling Hash)

Rabin-Karp uses hashing to speed up substring matching. We compute a hash of the pattern and then slide a window over the text, computing the hash of each window using a rolling hash technique. If the hashes match, we have a potential match (with possible false positives). Using double hashing with two different bases and moduli reduces false positive probability to near zero.

```cpp
class Solution {
public:
    vector<string> stringMatching(vector<string>& words) {
        vector<string> res;
        sort(words.begin(), words.end(), [](const string& a, const string& b) {
            return a.length() < b.length();
        });

        for (int i = 0; i < words.size(); i++) {
            for (int j = i + 1; j < words.size(); j++) {
                if (rabinKarp(words[j], words[i]) != -1) {
                    res.push_back(words[i]);
                    break;
                }
            }
        }

        return res;
    }

private:
    int rabinKarp(const string& word1, const string& word2) {
        int base1 = 31, mod1 = 768258391;
        int base2 = 37, mod2 = 685683731;
        int n = word1.size(), m = word2.size();

        long long power1 = 1, power2 = 1;
        for (int i = 0; i < m; i++) {
            power1 = (power1 * base1) % mod1;
            power2 = (power2 * base2) % mod2;
        }

        long long word1Hash1 = 0, word1Hash2 = 0;
        long long word2Hash1 = 0, word2Hash2 = 0;

        for (int i = 0; i < m; i++) {
            word1Hash1 = (word1Hash1 * base1 + word2[i]) % mod1;
            word1Hash2 = (word1Hash2 * base2 + word2[i]) % mod2;
            word2Hash1 = (word2Hash1 * base1 + word1[i]) % mod1;
            word2Hash2 = (word2Hash2 * base2 + word1[i]) % mod2;
        }

        for (int i = 0; i <= n - m; i++) {
            if (word2Hash1 == word1Hash1 && word2Hash2 == word1Hash2) {
                return i;
            }

            if (i + m < n) {
                word2Hash1 = (word2Hash1 * base1 - word1[i] * power1 + word1[i + m]) % mod1;
                word2Hash2 = (word2Hash2 * base2 - word1[i] * power2 + word1[i + m]) % mod2;

                if (word2Hash1 < 0) word2Hash1 += mod1;
                if (word2Hash2 < 0) word2Hash2 += mod2;
            }
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * m)$
- Space complexity:
    - $O(1)$ or $O(n)$ space depending on the sorting algorithm.
    - $O(n * m)$ space for the output list.

> Where $n$ is the number of words, and $m$ is the length of the longest word.

## 5. Z-Algorithm

The Z-algorithm builds a Z-array where Z[i] represents the length of the longest substring starting at position i that matches a prefix of the string. By concatenating the pattern, a separator, and the text, we can find all occurrences of the pattern by looking for positions where Z[i] equals the pattern length.

```cpp
class Solution {
public:
    vector<string> stringMatching(vector<string>& words) {
        vector<string> res;
        sort(words.begin(), words.end(), [](const string& a, const string& b) {
            return a.length() < b.length();
        });

        for (int i = 0; i < words.size(); i++) {
            for (int j = i + 1; j < words.size(); j++) {
                if (zAlgorithm(words[j], words[i]) != -1) {
                    res.push_back(words[i]);
                    break;
                }
            }
        }

        return res;
    }

private:
    int zAlgorithm(const string& word1, const string& word2) {
        string s = word2 + "$" + word1;
        int n = s.size();
        vector<int> z(n, 0);
        int l = 0, r = 0;

        for (int i = 1; i < n; i++) {
            if (i <= r) {
                z[i] = min(r - i + 1, z[i - l]);
            }
            while (i + z[i] < n && s[z[i]] == s[i + z[i]]) {
                z[i]++;
            }
            if (i + z[i] - 1 > r) {
                l = i;
                r = i + z[i] - 1;
            }
        }

        for (int i = word2.size() + 1; i < n; i++) {
            if (z[i] == word2.size()) {
                return i - word2.size() - 1;
            }
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * m)$
- Space complexity:
    - $O(m)$ extra space.
    - $O(1)$ or $O(n)$ space depending on the sorting algorithm.
    - $O(n * m)$ space for the output list.

> Where $n$ is the number of words, and $m$ is the length of the longest word.

## 6. Trie

We can use a suffix trie to solve this problem. For each word, we insert all its suffixes into the trie. Each node tracks how many times it has been visited. When searching for a word, if the terminal node has been visited more than once, the word appears as a substring in another word (since we inserted all suffixes, any substring of any word is a prefix of some suffix).

```cpp
class TrieNode {
public:
    TrieNode* children[26];
    int cnt;

    TrieNode() {
        for (int i = 0; i < 26; i++) children[i] = nullptr;
        cnt = 0;
    }
};

class Trie {
public:
    TrieNode* root;

    Trie() {
        root = new TrieNode();
    }

    void insertSuffixes(const string& word) {
        for (int i = 0; i < word.size(); i++) {
            TrieNode* node = root;
            for (int j = i; j < word.size(); j++) {
                int idx = word[j] - 'a';
                if (!node->children[idx]) {
                    node->children[idx] = new TrieNode();
                }

                node = node->children[idx];
                node->cnt++;
            }
        }
    }

    bool search(const string& word) {
        TrieNode* node = root;
        for (char c : word) {
            int idx = c - 'a';
            node = node->children[idx];
        }
        return node->cnt > 1;
    }
};

class Solution {
public:
    vector<string> stringMatching(vector<string>& words) {
        vector<string> res;
        Trie trie;

        for (const string& word : words) {
            trie.insertSuffixes(word);
        }

        for (const string& word : words) {
            if (trie.search(word)) {
                res.push_back(word);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m ^ 2)$
- Space complexity:
    - $O(n * m ^ 2)$ extra space.
    - $O(n * m)$ space for the output list.

> Where $n$ is the number of words, and $m$ is the length of the longest word.
