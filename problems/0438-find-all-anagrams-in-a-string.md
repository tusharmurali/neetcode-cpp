# 438. Find All Anagrams in a String

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-all-anagrams-in-a-string/>  
- **NeetCode:** <https://neetcode.io/problems/find-all-anagrams-in-a-string>  
- **Video:** <https://www.youtube.com/watch?v=G8xtZy0fDKg>  

[← Back to index](../INDEX.md)

## 1. Brute Force

An anagram is simply a rearrangement of characters. Two strings are anagrams if they contain the same characters with the same frequencies. The most direct way to check this is to sort both strings and compare them. We can slide through every substring of `s` that has the same length as `p`, sort it, and check if it matches the sorted version of `p`.

```cpp
class Solution {
public:
    vector<int> findAnagrams(string s, string p) {
        int n = s.size(), m = p.size();
        vector<int> res;
        sort(p.begin(), p.end());

        for (int i = 0; i <= n - m; i++) {
            string sub = s.substr(i, m);
            sort(sub.begin(), sub.end());
            if (sub == p) {
                res.push_back(i);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m \log m)$
- Space complexity: $O(m)$

> Where $n$ is the length of the string $s$ and $m$ is the length of the string $p$.

## 2. Prefix Count + Sliding Window

Instead of sorting substrings repeatedly, we can precompute character frequencies using prefix sums. For each position in `s`, we maintain a cumulative count of each character seen so far. To get the character frequencies for any window, we subtract the prefix count at the start from the prefix count at the end. If the window's character counts match `p`'s counts, we found an anagram.

```cpp
class Solution {
public:
    vector<int> findAnagrams(string s, string p) {
        int n = s.size(), m = p.size();
        if (m > n) return {};

        vector<int> pCount(26, 0);
        for (char c : p) pCount[c - 'a']++;

        vector<vector<int>> prefix(n + 1, vector<int>(26, 0));
        for (int i = 1; i <= n; i++) {
            prefix[i] = prefix[i - 1];
            prefix[i][s[i - 1] - 'a']++;
        }

        vector<int> res;
        int i = 0, j = m - 1;
        while (j < n) {
            bool isValid = true;
            for (int c = 0; c < 26; c++) {
                if (prefix[j + 1][c] - prefix[i][c] != pCount[c]) {
                    isValid = false;
                    break;
                }
            }
            if (isValid) res.push_back(i);
            i++;
            j++;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(n)$

> Where $n$ is the length of the string $s$ and $m$ is the length of the string $p$.

## 3. Sliding Window

We can avoid rebuilding frequency counts from scratch by using a sliding window. Start by counting characters in the first window of size `len(p)`. As we slide the window one position to the right, we add the new character entering the window and remove the character leaving it. After each slide, we compare the window's character counts with the pattern's counts.

```cpp
class Solution {
public:
    vector<int> findAnagrams(string s, string p) {
        if (p.size() > s.size()) return {};

        vector<int> pCount(26, 0), sCount(26, 0);
        for (char c : p) {
            pCount[c - 'a']++;
        }
        for (int i = 0; i < p.size(); i++) {
            sCount[s[i] - 'a']++;
        }

        vector<int> res;
        if (pCount == sCount) res.push_back(0);

        int l = 0;
        for (int r = p.size(); r < s.size(); r++) {
            sCount[s[r] - 'a']++;
            sCount[s[l] - 'a']--;
            l++;
            if (pCount == sCount) {
                res.push_back(l);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

> Where $n$ is the length of the string $s$ and $m$ is the length of the string $p$.

## 4. Sliding Window (Optimal)

Comparing two arrays of `26` elements after every slide takes extra time. We can optimize by tracking how many of the `26` character counts currently match between the window and the pattern. When we add or remove a character, we only update the match count for that specific character. If all `26` counts match, we found an anagram.

```cpp
class Solution {
public:
    vector<int> findAnagrams(string s, string p) {
        int n = s.size(), m = p.size();
        if (m > n) return {};

        vector<int> pCount(26, 0), sCount(26, 0);
        for (int i = 0; i < m; i++) {
            pCount[p[i] - 'a']++;
            sCount[s[i] - 'a']++;
        }

        int match = 0;
        for (int i = 0; i < 26; i++) {
            if (pCount[i] == sCount[i]) match++;
        }

        vector<int> res;
        if (match == 26) res.push_back(0);

        int l = 0;
        for (int r = m; r < n; r++) {
            int c = s[l] - 'a';
            if (sCount[c] == pCount[c]) match--;
            sCount[c]--;
            l++;
            if (sCount[c] == pCount[c]) match++;

            c = s[r] - 'a';
            if (sCount[c] == pCount[c]) match--;
            sCount[c]++;
            if (sCount[c] == pCount[c]) match++;

            if (match == 26) res.push_back(l);
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n + m)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

> Where $n$ is the length of the string $s$ and $m$ is the length of the string $p$.

## Standalone solution file (`cpp/0438-find-all-anagrams-in-a-string.cpp` in the NeetCode repo)

```cpp
class Solution{    
    public:    
        unordered_map<char, int> Create(string p){            
            unordered_map<char, int> Mapp;            
            for(char & i : p){                
                if(Mapp.find(i) == Mapp.end()){                    
                    Mapp.insert(make_pair(i, 1));                    
                }
                else{                    
                    Mapp[i]++;                    
                }                
            }            
            return Mapp;            
        }    
        vector<int> findAnagrams(string s, string p){            
            unordered_map<char, int> Maps, Mapp = {};            
            vector<int> nums = {};            
            int Fp, Sp;            
            int lens, lenp;            
            Fp = 0;            
            Sp = p.length();            
            lens = s.length();            
            lenp = p.length();            
            Mapp = Create(p);            
            Maps = Create(s.substr(0, p.length()));            
            for(Fp = 0; Fp < lens - lenp + 1; Fp++){   
                if(Maps == Mapp){                    
                    nums.push_back(Fp);                    
                }                
                if(Maps.find(s[Sp]) != Maps.end()){                    
                    Maps[s[Sp]]++;                
                }
                else{                    
                    Maps.insert(make_pair(s[Sp], 1));                                            
                }                                            
                Sp++;                
                Maps[s[Fp]]--;                
                if(Maps[s[Fp]] == 0){                    
                    Maps.erase(s[Fp]);                    
                }                    
            }            
            return nums;
        }    
};
```
