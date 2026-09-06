# 2002. Maximum Product of The Length of Two Palindromic Subsequences

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-product-of-the-length-of-two-palindromic-subsequences/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-product-of-the-length-of-two-palindromic-subsequences>  
- **Video:** <https://www.youtube.com/watch?v=aoHbYlO8vDg>  

[← Back to index](../INDEX.md)

## 1. Recursion (Backtracking)

We need two disjoint palindromic subsequences with maximum product of their lengths. For each character, we have three choices: add it to the first subsequence, add it to the second subsequence, or skip it entirely. At the end, if both subsequences are palindromes, we compute their product.

```cpp
class Solution {
public:
    bool isPal(const string &s) {
        int i = 0, j = s.length() - 1;
        while (i < j) {
            if (s[i] != s[j]) return false;
            i++;
            j--;
        }
        return true;
    }

    void rec(int i, string& s, string& seq1, string& seq2, int &res) {
        if (i == s.length()) {
            if (isPal(seq1) && isPal(seq2)) {
                res = max(res, (int)seq1.length() * (int)seq2.length());
            }
            return;
        }

        rec(i + 1, s, seq1, seq2, res);
        seq1.push_back(s[i]);
        rec(i + 1, s, seq1, seq2, res);
        seq1.pop_back();
        seq2.push_back(s[i]);
        rec(i + 1, s, seq1, seq2, res);
        seq2.pop_back();
    }

    int maxProduct(string s) {
        int res = 0;
        string seq1 = "", seq2 = "";
        rec(0, s, seq1, seq2, res);
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * 3 ^ n)$
- Space complexity: $O(n)$

## 2. Bit Mask

Since the string length is small (up to 12), we can represent each subsequence as a bitmask. We first enumerate all possible subsequences, check which ones are palindromes, and store them. Then we check all pairs of palindromic subsequences. Two subsequences are disjoint if their masks have no overlapping bits (bitwise AND equals `0`).

```cpp
class Solution {
public:
    int maxProduct(string s) {
        int N = s.length();
        int res = 0;
        unordered_map<int, int> pali;

        for (int mask = 1; mask < (1 << N); mask++) {
            string subseq = "";
            for (int i = 0; i < N; i++) {
                if (mask & (1 << i)) {
                    subseq += s[i];
                }
            }

            if (isPal(subseq)) {
                pali[mask] = subseq.length();
            }
        }

        for (auto& m1 : pali) {
            for (auto& m2 : pali) {
                if ((m1.first & m2.first) == 0) {
                    res = max(res, m1.second * m2.second);
                }
            }
        }

        return res;
    }

private:
    bool isPal(const string& s) {
        int i = 0, j = s.length() - 1;
        while (i < j) {
            if (s[i] != s[j]) {
                return false;
            }
            i++;
            j--;
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(4 ^ n)$
- Space complexity: $O(2 ^ n)$

## 3. Bit Mask + Longest Palindromic Subsequence

Instead of checking all pairs of palindromic masks, we can optimize by iterating through palindromic masks for the first subsequence and computing the longest palindromic subsequence (LPS) in the remaining characters. This avoids redundant pair comparisons while still finding the optimal solution.

```cpp
class Solution {
public:
    int longestPalindromeSubseq(string& s) {
        int n = s.length();
        if (n == 0) return 0;

        vector<int> dp(n, 1);
        for (int i = n - 1; i >= 0; i--) {
            int prev = 0;
            for (int j = i + 1; j < n; j++) {
                int tmp = dp[j];
                if (s[i] == s[j]) {
                    dp[j] = 2 + prev;
                } else {
                    dp[j] = max(dp[j - 1], dp[j]);
                }
                prev = tmp;
            }
        }
        return dp[n - 1];
    }

    int maxProduct(string s) {
        int n = s.length();
        int res = 0;

        for (int i = 1; i < (1 << n); i++) {
            string seq1 = "", seq2 = "";

            for (int j = 0; j < n; j++) {
                if ((i & (1 << j)) != 0) seq1 += s[j];
                else seq2 += s[j];
            }

            if (!isPal(seq1)) continue;

            int lps = longestPalindromeSubseq(seq2);
            res = max(res, int(seq1.length()) * lps);
        }

        return res;
    }

    bool isPal(string& s) {
        int i = 0, j = s.length() - 1;
        while (i < j) {
            if (s[i] != s[j]) {
                return false;
            }
            i++;
            j--;
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * 2 ^ n)$
- Space complexity: $O(n)$

## 4. Bit Mask + LPS (Optimal)

We can further optimize by computing the LPS directly on the original string while using the mask to skip characters that belong to the first subsequence. This avoids creating new strings and reduces overhead. We also validate palindromes efficiently using two pointers with mask-based skipping.

```cpp
class Solution {
public:
    int longestPalindromeSubseq(string& s, int mask, vector<int>& dp) {
        int n = s.length();
        for (int i = n - 1; i >= 0; i--) {
            if ((mask & (1 << i)) != 0) continue;

            int prev = 0;
            for (int j = i + 1; j < n; j++) {
                int tmp = dp[j];
                if ((mask & (1 << j)) == 0 && s[i] == s[j]) {
                    dp[j] = 2 + prev;
                } else {
                    dp[j] = max(dp[j - 1], dp[j]);
                }
                prev = tmp;
            }
        }
        return dp[n - 1];
    }

    int maxProduct(string s) {
        int n = s.length();
        int res = 0;
        vector<int> dp(n, 1);

        for (int i = 1; i < (1 << n); i++) {
            int m1 = palsize(s, i);
            if (m1 == 0) continue;

            for (int j = 0; j < n; j++) {
                if ((i & (1 << j)) == 0) {
                    dp[j] = 1;
                } else {
                    dp[j] = 0;
                }
            }
            int m2 = longestPalindromeSubseq(s, i, dp);
            res = max(res, m1 * m2);
        }

        return res;
    }

    int palsize(string& s, int mask) {
        int i = 0, j = s.length() - 1;
        int res = 0;
        while (i <= j) {
            if ((mask & (1 << i)) == 0) i++;
            else if ((mask & (1 << j)) == 0) j--;
            else {
                if (s[i] != s[j]) return 0;
                res += (i == j) ? 1 : 2;
                i++;
                j--;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2 * 2 ^ n)$
- Space complexity: $O(n)$

## Standalone solution file (`cpp/2002-maximum-product-of-the-length-of-two-palindromic-subsequences.cpp` in the NeetCode repo)

```cpp
 /*
    Approach: 
    Need to create all the disjoin subsequence and check if they are palindrome.
    keep track of maximum product 

    Time complexity : O(N*N^3)
    Space complexity: O(N)

    N is length of the string
*/


class Solution {
public:

    int answer = INT_MIN;

    // function to check if the string is a palindrome
    bool isPalindrome(string &s){
        int start = 0;
        int end = s.length() - 1;

        while(start<end){
            if(s[start]!=s[end]){
                return false;
            }
            start++;
            end--;
        }

        return true;
    }

    // function to generate all the disjoint subsequence
    void generateAll(int idx, string &s1, string &s2, string& s){

        if(idx >= s.length())
        {
            if(isPalindrome(s1)&&isPalindrome(s2)){
                int l = s1.length()*s2.length();
                answer = max(answer,l);
            }
            return;
        }
        
        char c = s[idx];

        /* 
        we have three options
        1. Add the char to the first string
        2. Add the char to the second string
        3. Add the char to none of the string
        */

        // add the character in the first string
        s1.push_back(c);
        generateAll(idx+1,s1,s2,s);
        s1.pop_back();

        // add the character in the second string
        s2.push_back(c);
        generateAll(idx+1,s1,s2,s);
        s2.pop_back();

        // add character in no string
        generateAll(idx+1,s1,s2,s);
    }

    int maxProduct(string s) {

        string s1 = "";
        string s2 = "";
        int idx = 0;

        generateAll(idx,s1,s2,s);

        return answer;
    }

    
};
```
