# 28. Find The Index of The First Occurrence in a String

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/>  
- **NeetCode:** <https://neetcode.io/problems/find-the-index-of-the-first-occurrence-in-a-string>  
- **Video:** <https://www.youtube.com/watch?v=JoF0Z7nVSrA>  
- **Video approach:** 2. Knuth-Morris-Pratt (KMP) Algorithm (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Brute Force

The simplest way to find a substring is to try every possible starting position in the haystack. At each position, we compare characters one by one with the needle. If all characters match, we found our answer. If any character doesn't match, we move to the next starting position and try again.

```cpp
class Solution {
public:
    int strStr(string haystack, string needle) {
        int n = haystack.length(), m = needle.length();
        for (int i = 0; i < n - m + 1; i++) {
            int j = 0;
            while (j < m) {
                if (haystack[i + j] != needle[j]) {
                    break;
                }
                j++;
            }
            if (j == m) return i;
        }
        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(1)$

> Where $n$ is the length of the string $heystack$ and $m$ is the length of the string $needle$.

## 2. Knuth-Morris-Pratt (KMP) Algorithm ▶ video

The brute force approach wastes work by restarting from scratch after each mismatch. KMP improves this by preprocessing the needle to build a "longest proper prefix which is also suffix" (LPS) array. When a mismatch occurs, the LPS array tells us how many characters we can skip, leveraging the pattern structure to avoid redundant comparisons.

```cpp
class Solution {
public:
    int strStr(string haystack, string needle) {
        if (needle.empty()) return 0;

        int m = needle.size();
        vector<int> lps(m, 0);
        int prevLPS = 0, i = 1;

        while (i < m) {
            if (needle[i] == needle[prevLPS]) {
                lps[i] = prevLPS + 1;
                prevLPS++;
                i++;
            } else if (prevLPS == 0) {
                lps[i] = 0;
                i++;
            } else {
                prevLPS = lps[prevLPS - 1];
            }
        }

        i = 0;  // ptr for haystack
        int j = 0;  // ptr for needle
        while (i < haystack.size()) {
            if (haystack[i] == needle[j]) {
                i++;
                j++;
            } else {
                if (j == 0) {
                    i++;
                } else {
                    j = lps[j - 1];
                }
            }

            if (j == m) {
                return i - m;
            }
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(m)$

> Where $n$ is the length of the string $heystack$ and $m$ is the length of the string $needle$.

## 3. Z-Algorithm

The Z-algorithm computes, for each position in a string, the length of the longest substring starting from that position that matches a prefix of the string. By concatenating the needle, a separator character, and the haystack, any position where the Z-value equals the needle length indicates a match. The algorithm uses a "Z-box" to track previously computed matches and skip redundant comparisons.

```cpp
class Solution {
public:
    int strStr(string haystack, string needle) {
        if (needle.empty()) return 0;

        string s = needle + "$" + haystack;
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

        for (int i = needle.size() + 1; i < n; i++) {
            if (z[i] == needle.size()) {
                return i - needle.size() - 1;
            }
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n + m)$

> Where $n$ is the length of the string $heystack$ and $m$ is the length of the string $needle$.

## 4. Rabin-Karp Algorithm (Rolling Hash)

Instead of comparing characters one by one, we can compare hash values of substrings. If we compute the hash of the needle and the hash of each window in the haystack, matching hashes suggest a potential match. The key insight is using a rolling hash: when sliding the window by one position, we can update the hash in O(1) time by removing the contribution of the outgoing character and adding the incoming one. Using two different hash functions reduces false positives.

```cpp
class Solution {
public:
    int strStr(string haystack, string needle) {
        if (needle.empty()) return 0;

        long long base1 = 31, mod1 = 768258391;
        long long base2 = 37, mod2 = 685683731;

        int n = haystack.size(), m = needle.size();
        if (m > n) return -1;

        long long power1 = 1, power2 = 1;
        for (int i = 0; i < m; i++) {
            power1 = (power1 * base1) % mod1;
            power2 = (power2 * base2) % mod2;
        }

        long long needleHash1 = 0, needleHash2 = 0;
        long long haystackHash1 = 0, haystackHash2 = 0;

        for (int i = 0; i < m; i++) {
            needleHash1 = (needleHash1 * base1 + needle[i]) % mod1;
            needleHash2 = (needleHash2 * base2 + needle[i]) % mod2;
            haystackHash1 = (haystackHash1 * base1 + haystack[i]) % mod1;
            haystackHash2 = (haystackHash2 * base2 + haystack[i]) % mod2;
        }

        for (int i = 0; i <= n - m; i++) {
            if (haystackHash1 == needleHash1 && haystackHash2 == needleHash2) {
                return i;
            }

            if (i + m < n) {
                haystackHash1 = (haystackHash1 * base1 - haystack[i] * power1 + haystack[i + m]) % mod1;
                haystackHash2 = (haystackHash2 * base2 - haystack[i] * power2 + haystack[i + m]) % mod2;

                if (haystackHash1 < 0) haystackHash1 += mod1;
                if (haystackHash2 < 0) haystackHash2 += mod2;
            }
        }

        return -1;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(1)$

> Where $n$ is the length of the string $heystack$ and $m$ is the length of the string $needle$.

## Standalone solution file (`cpp/0028-find-the-index-of-the-first-occurrence-in-a-string.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int strStr(string haystack, string needle) {
        if(haystack.size()<needle.size()) return -1;
        int found=0;
        for(int i=0;i<haystack.size()-needle.size()+1;i++){
            if(haystack[i]==needle[0]){
                found=1;
                for(int j=1;j<needle.size();j++){
                    if(haystack[i+j]!=needle[j]){
                        found=0;break;
                    }
                }if(found==1) return i;
            }
        }return -1;
    }
};
```
