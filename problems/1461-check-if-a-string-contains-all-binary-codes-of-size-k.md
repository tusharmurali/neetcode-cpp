# 1461. Check if a String Contains all Binary Codes of Size K

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/check-if-a-string-contains-all-binary-codes-of-size-k/>  
- **NeetCode:** <https://neetcode.io/problems/check-if-a-string-contains-all-binary-codes-of-size-k>  
- **Video:** <https://www.youtube.com/watch?v=qU32rTy_kOM>  

[← Back to index](../INDEX.md)

## 1. Brute Force

The most straightforward approach is to generate all possible binary codes of length `k` and check if each one exists as a substring in the given string `s`. There are exactly $2^k$ such binary codes (from 0 to $2^k - 1$), and we need to verify that every single one appears somewhere in `s`.

```cpp
class Solution {
public:
    bool hasAllCodes(string s, int k) {
        int n = s.size();
        if (n < (1 << k)) {
            return false;
        }

        for (int num = 0; num < (1 << k); num++) {
            string binaryCode = bitset<20>(num).to_string().substr(20 - k);
            if (s.find(binaryCode) == string::npos) {
                return false;
            }
        }

        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ k)$
- Space complexity: $O(k)$

> Where $n$ is the length of the string $s$ and $k$ is the length of the binary code.

## 2. Hash Set

Instead of checking each possible binary code one by one, we can flip the approach: extract all substrings of length `k` from `s` and store them in a set. If the set contains exactly $2^k$ unique substrings, then all binary codes are present. This is more efficient because we process each substring only once.

```cpp
class Solution {
public:
    bool hasAllCodes(std::string s, int k) {
        if (s.size() < (1 << k)) {
            return false;
        }

        std::unordered_set<std::string> codeSet;
        for (int i = 0; i <= s.size() - k; i++) {
            codeSet.insert(s.substr(i, k));
        }

        return codeSet.size() == (1 << k);
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(2 ^ k)$

> Where $n$ is the length of the string $s$ and $k$ is the length of the binary code.

## 3. Sliding Window

We can improve upon the hash set approach by using bit manipulation to represent each substring as an integer. Instead of storing strings, we maintain a sliding window of `k` bits. As we move through the string, we update the integer representation by removing the leftmost bit and adding the new rightmost bit. This converts string operations into faster bitwise operations.

```cpp
class Solution {
public:
    bool hasAllCodes(string s, int k) {
        int n = s.size();
        if (n < (1 << k)) {
            return false;
        }

        vector<bool> codeSet(1 << k, false);
        int cur = 0;
        int i = 0, j = 0, bit = k - 1;

        while (j < k) {
            if (s[j] == '1') {
                cur |= (1 << bit);
            }
            bit--;
            j++;
        }

        int have = 1;
        codeSet[cur] = true;

        while (j < n) {
            if (s[i] == '1') {
                cur ^= (1 << (k - 1));
            }
            i++;

            cur <<= 1;
            if (s[j] == '1') {
                cur |= 1;
            }
            j++;

            if (!codeSet[cur]) {
                have++;
                codeSet[cur] = true;
            }
        }

        return have == (1 << k);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(2 ^ k)$

> Where $n$ is the length of the string $s$ and $k$ is the length of the binary code.

## 4. Sliding Window (Optimal)

This approach simplifies the sliding window technique by using a bitmask to automatically handle the window size. Instead of explicitly removing the leftmost bit, we use a bitwise AND with a mask ($2^k - 1$) after shifting. This mask keeps only the rightmost `k` bits, effectively removing any bits that overflow beyond the window size.

```cpp
class Solution {
public:
    bool hasAllCodes(string s, int k) {
        int n = s.size();
        if (n < (1 << k)) {
            return false;
        }

        vector<bool> codeSet(1 << k, false);
        int cur = 0, have = 0;

        for (int i = 0; i < n; i++) {
            cur = ((cur << 1) & ((1 << k) - 1)) | (s[i] - '0');

            if (i >= k - 1) {
                if (!codeSet[cur]) {
                    codeSet[cur] = true;
                    have++;
                }
            }
        }

        return have == (1 << k);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(2 ^ k)$

> Where $n$ is the length of the string $s$ and $k$ is the length of the binary code.

## Standalone solution file (`cpp/1461-check-if-a-string-contains-all-binary-codes-of-size-k.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    bool hasAllCodes(string s, int k) {
        
        set<string> all_substrings;
        int total = 1 <<k; // this is equal to 2 power k (2^k)

        // get all the substring of len k and store it in a set
        for(int i =0;i+k<=s.length();i++){
            all_substrings.insert(s.substr(i,k));
            // size of set equals 2 power k
            if (all_substrings.size() == total){
                return true;
            }
        }
        
        return false;
    }
};
```
