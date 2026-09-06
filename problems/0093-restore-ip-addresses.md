# 93. Restore IP Addresses

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/restore-ip-addresses/>  
- **NeetCode:** <https://neetcode.io/problems/restore-ip-addresses>  
- **Video:** <https://www.youtube.com/watch?v=61tN4YEdiTM>  

[← Back to index](../INDEX.md)

## 1. Backtracking

A valid IP address has exactly four segments, each containing 1 to 3 digits with a value between 0 and 255. Leading zeros are not allowed except for the segment "0" itself. Backtracking lets us explore all possible ways to place three dots in the string. At each step, we try taking 1, 2, or 3 characters for the current segment, validate it, and recurse for the remaining segments.

```cpp
class Solution {
        vector<string> res;

public:
    vector<string> restoreIpAddresses(string s) {
        if (s.length() > 12) return res;
        backtrack(s, 0, 0, "");
        return res;
    }

private:
    void backtrack(string& s, int i, int dots, string curIP) {
        if (dots == 4 && i == s.size()) {
            res.push_back(curIP.substr(0, curIP.size() - 1));
            return;
        }
        if (dots > 4) return;

        for (int j = i; j < min(i + 3, (int)s.size()); j++) {
            if (i != j && s[i] == '0') continue;
            if (stoi(s.substr(i, j - i + 1)) < 256) {
                backtrack(s, j + 1, dots + 1, curIP + s.substr(i, j - i + 1) + ".");
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(m ^ n * n)$
- Space complexity: $O(m * n)$

> Where $m$ is equals to $3$ as there are at most three digits in a valid segment and $n$ is equals to $4$ as there are four segments in a valid IP.

## 2. Iteration

Since there are exactly four segments and each can have 1, 2, or 3 characters, we can enumerate all 81 combinations (3^4) of segment lengths directly. For each combination, we check if the total length matches the input string and whether each resulting segment is valid. This avoids recursion overhead while still exploring all possibilities.

```cpp
class Solution {
public:
    vector<string> restoreIpAddresses(string s) {
        vector<string> res;
        if (s.size() > 12) return res;

        auto valid = [&](string& num) {
            if (num.size() > 1 && num[0] == '0') return false;
            int value = stoi(num);
            return value <= 255;
        };

        for (int seg1 = 1; seg1 < 4; ++seg1) {
            for (int seg2 = 1; seg2 < 4; ++seg2) {
                for (int seg3 = 1; seg3 < 4; ++seg3) {
                    for (int seg4 = 1; seg4 < 4; ++seg4) {
                        if (seg1 + seg2 + seg3 + seg4 != s.size()) continue;

                        string num1 = s.substr(0, seg1);
                        string num2 = s.substr(seg1, seg2);
                        string num3 = s.substr(seg1 + seg2, seg3);
                        string num4 = s.substr(seg1 + seg2 + seg3);

                        if (valid(num1) && valid(num2) && valid(num3) && valid(num4)) {
                            res.push_back(num1 + "." + num2 + "." + num3 + "." + num4);
                        }
                    }
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m ^ n * n)$
- Space complexity: $O(m * n)$

> Where $m$ is equals to $3$ as there are at most three digits in a valid segment and $n$ is equals to $4$ as there are four segments in a valid IP.
