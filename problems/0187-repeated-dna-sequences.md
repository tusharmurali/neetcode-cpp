# 187. Repeated DNA Sequences

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/repeated-dna-sequences/>  
- **NeetCode:** <https://neetcode.io/problems/repeated-dna-sequences>  
- **Video:** <https://www.youtube.com/watch?v=FzTYfsmtOso>  

[← Back to index](../INDEX.md)

## 1. Hash Set

We need to find all 10-letter sequences that appear more than once. A hash set naturally tracks what we have seen before. As we slide a window of length 10 across the string with index `l`, we check if the current substring `cur` was already encountered. If so, it is a repeated sequence. Using two sets (one for `seen` sequences and one for `res` results) avoids adding duplicates to our answer.

```cpp
class Solution {
public:
    vector<string> findRepeatedDnaSequences(string s) {
        if (s.size() < 10) return {};
        unordered_set<string> seen, res;

        for (int l = 0; l < s.size() - 9; l++) {
            string cur = s.substr(l, 10);
            if (seen.count(cur)) {
                res.insert(cur);
            }
            seen.insert(cur);
        }
        return vector<string>(res.begin(), res.end());
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Hash Map

Instead of using two sets, we can use a hash map `mp` to count occurrences of each sequence. This lets us add a sequence to the `res` exactly when its count reaches 2, ensuring we only report it once regardless of how many additional times it appears.

```cpp
class Solution {
public:
    vector<string> findRepeatedDnaSequences(string s) {
        if (s.size() < 10) {
            return {};
        }

        unordered_map<string, int> mp;
        vector<string> res;

        for (int l = 0; l < s.size() - 9; l++) {
            string cur = s.substr(l, 10);
            mp[cur]++;
            if (mp[cur] == 2) {
                res.push_back(cur);
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Rabin-Karp Algorithm (Double Hashing)

Storing full 10-character strings as keys can be memory intensive. The Rabin-Karp algorithm computes a rolling hash for each window, allowing us to represent each sequence as a number instead. Double hashing (using two different hash bases) minimizes collision probability, making numeric comparisons reliable. As the window slides with index `i`, we efficiently update the hashes `hash1` and `hash2` by removing the contribution of the outgoing character and adding the incoming one.

```cpp
class Solution {
public:
    vector<string> findRepeatedDnaSequences(string s) {
        int n = s.length();
        if (n < 10) return {};

        unordered_map<long long, int> cnt;
        vector<string> res;
        int base1 = 31, base2 = 37;
        long long hash1 = 0, hash2 = 0, power1 = 1, power2 = 1;
        int MOD1 = 685683731, MOD2 = 768258391;

        for (int i = 0; i < 9; i++) {
            power1 = (power1 * base1) % MOD1;
            power2 = (power2 * base2) % MOD2;
        }

        for (int i = 0; i < n; i++) {
            hash1 = (hash1 * base1 + s[i]) % MOD1;
            hash2 = (hash2 * base2 + s[i]) % MOD2;

            if (i >= 9) {
                long long key = (hash1 << 31) | hash2;
                cnt[key]++;
                if (cnt[key] == 2) {
                    res.push_back(s.substr(i - 9, 10));
                }

                hash1 = (hash1 - power1 * s[i - 9] % MOD1 + MOD1) % MOD1;
                hash2 = (hash2 - power2 * s[i - 9] % MOD2 + MOD2) % MOD2;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Bit Mask

DNA sequences use only four characters (A, C, G, T), each of which can be encoded with just 2 bits. A 10-character sequence therefore fits in 20 bits, well within a single integer. By treating each sequence as a `mask`, we avoid storing strings entirely and get fast integer operations for comparisons and hashing.

```cpp
class Solution {
public:
    vector<string> findRepeatedDnaSequences(string s) {
        if (s.length() < 10) return {};

        unordered_map<char, int> mp = {{'A', 0}, {'C', 1},
                                       {'G', 2}, {'T', 3}};
        unordered_map<int, int> cnt;
        vector<string> res;
        int mask = 0;

        for (int i = 0; i < s.size(); i++) {
            mask = ((mask << 2) | mp[s[i]]) & 0xFFFFF;

            if (i >= 9) {
                cnt[mask]++;
                if (cnt[mask] == 2) {
                    res.push_back(s.substr(i - 9, 10));
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/0187-repeated-dna-sequences.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    vector<string> findRepeatedDnaSequences(string s) {

        int n = s.size();
        if(n <=10){ return {};}
        vector<string> answer;

        unordered_map<string,int> hash;

        for(int i = 0;i<=s.size()-10;i++){
            string ss = s.substr(i,10);
            hash[ss]++;
            if(hash[ss]==2){
                answer.push_back(ss);
            }
        }

        return answer;
    }
};
```
