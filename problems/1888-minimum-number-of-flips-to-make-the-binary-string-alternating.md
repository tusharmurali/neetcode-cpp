# 1888. Minimum Number of Flips to Make The Binary String Alternating

- **Difficulty:** Medium  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-number-of-flips-to-make-the-binary-string-alternating/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-number-of-flips-to-make-the-binary-string-alternating>  
- **Video:** <https://www.youtube.com/watch?v=MOeuK6gaC2A>  

[← Back to index](../INDEX.md)

## 1. Brute Force

An alternating string is either `"010101..."` or `"101010..."`. The type-1 operation (moving first character to end) lets us try all possible rotations of the string. For each rotation, we count how many flips are needed to match either target pattern.

We generate both alternating patterns of length `n`, then for each of the `n` possible rotations, compute the difference count against both patterns and track the minimum.

```cpp
class Solution {
public:
    int minFlips(string s) {
        int n = s.size(), res = n;
        string alt1, alt2;

        for (int i = 0; i < n; i++) {
            alt1 += (i % 2 == 0) ? '0' : '1';
            alt2 += (i % 2 == 0) ? '1' : '0';
        }

        for (int i = 0; i < n; i++) {
            string newS = s.substr(i) + s.substr(0, i);
            res = min(res, min(diff(alt1, newS), diff(alt2, newS)));
        }

        return res;
    }

private:
    int diff(const string &a, const string &b) {
        int cnt = 0;
        for (int i = 0; i < a.size(); i++) {
            if (a[i] != b[i]) cnt++;
        }
        return cnt;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Brute Force (Space Optimized)

Instead of creating explicit rotated strings, we can iterate circularly through the original string using modular arithmetic. For each starting position, we walk through all `n` characters and count mismatches against both alternating patterns on the fly.

This saves the O(n) space needed to store rotated strings while maintaining the same logic: try every rotation and count flips needed for both target patterns.

```cpp
class Solution {
public:
    int minFlips(string s) {
        int n = s.size(), res = n;

        for (int i = 0; i < n; i++) {
            int start0 = (s[i] != '0') ? 1 : 0;
            int start1 = (s[i] != '1') ? 1 : 0;
            char c = '0';
            int j = (i + 1) % n;

            while (j != i) {
                start1 += (s[j] != c) ? 1 : 0;
                start0 += (s[j] == c) ? 1 : 0;
                c = (c == '1') ? '0' : '1';
                j = (j + 1) % n;
            }

            res = min(res, min(start1, start0));
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(1)$ extra space.

## 3. Sliding Window

Concatenating the string with itself (`s + s`) simulates all rotations. A window of size `n` sliding over this doubled string represents each rotation. We can maintain mismatch counts incrementally: add the new character's contribution when expanding the window, and remove the old character's contribution when shrinking.

This transforms the O(n^2) brute force into O(n) by avoiding recalculation of the full difference for each rotation.

```cpp
class Solution {
public:
    int minFlips(string s) {
        int n = s.size();
        s += s;
        string alt1, alt2;
        for (int i = 0; i < s.size(); i++) {
            alt1 += (i % 2 == 0) ? '0' : '1';
            alt2 += (i % 2 == 0) ? '1' : '0';
        }

        int res = n, diff1 = 0, diff2 = 0, l = 0;

        for (int r = 0; r < s.size(); r++) {
            if (s[r] != alt1[r]) diff1++;
            if (s[r] != alt2[r]) diff2++;

            if (r - l + 1 > n) {
                if (s[l] != alt1[l]) diff1--;
                if (s[l] != alt2[l]) diff2--;
                l++;
            }

            if (r - l + 1 == n) {
                res = min(res, min(diff1, diff2));
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Sliding Window (Space Optimized)

We can avoid storing the doubled string and alternating patterns by computing expected characters on the fly. By tracking what character position `r` should have (toggling between '0' and '1'), we update mismatch counts directly.

Using modular indexing `s[r % n]` simulates the doubled string. We track the expected starting character for both window boundaries and toggle as we slide.

```cpp
class Solution {
public:
    int minFlips(string s) {
        int n = s.size();
        int res = n, diff1 = 0, diff2 = 0, l = 0;

        char rstart_0 = '0', lstart_0 = '0';

        for (int r = 0; r < 2 * n; r++) {
            if (s[r % n] != rstart_0) diff1++;
            if (s[r % n] == rstart_0) diff2++;

            if (r - l + 1 > n) {
                if (s[l] != lstart_0) diff1--;
                if (s[l] == lstart_0) diff2--;
                l++;
                lstart_0 = (lstart_0 == '0') ? '1' : '0';
            }

            if (r - l + 1 == n) {
                res = min(res, min(diff1, diff2));
            }

            rstart_0 = (rstart_0 == '0') ? '1' : '0';
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 5. Dynamic Programming

First, count mismatches for the original string against pattern `"1010..."`. The mismatch count for `"0101..."` is simply `n - start_1` since every position either matches one pattern or the other.

For odd-length strings, rotating changes parity. After one rotation, positions that needed a `'0'` now need a `'1'` and vice versa. We can compute the new mismatch counts by swapping and adjusting based on the character that moved from front to back.

```cpp
class Solution {
public:
    int minFlips(string s) {
        int start_1 = 0, n = s.size();

        for (int i = 0; i < n; i++) {
            if (i & 1) {
                start_1 += (s[i] == '1');
            } else {
                start_1 += (s[i] == '0');
            }
        }

        int start_0 = n - start_1;
        int ans = min(start_0, start_1);
        if (n % 2 == 0) {
            return ans;
        }

        int dp0 = start_0, dp1 = start_1;
        for (char c : s) {
            int temp = dp0;
            dp0 = dp1;
            dp1 = temp;
            if (c == '1') {
                dp0++;
                dp1--;
            } else {
                dp0--;
                dp1++;
            }
            ans = min({ans, dp0, dp1});
        }

        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## Standalone solution file (`cpp/1888-minimum-number-of-flips-to-make-the-binary-string-alternating.cpp` in the NeetCode repo)

```cpp
// O(n) time and O(n) space complexity
// Use a sliding window to update the number of differences between current string and two target strings
// Instead of doing the type-1 operation N times, we can append a copy of the string to the end of the string, and iterate with a sliding window.
// As you iterate through the window, update the count of differences
// If the sliding window is the full size, update the result with the minimum of the two counts of differences
class Solution {
public:
    int minFlips(string s) {
       int n =  s.size();
       s = s.append(s);
       string t1 = "";
       string t2 = "";
       for (int i = 0; i < s.size(); i++){
           if (i % 2 == 0) {
               t1.append("0");
               t2.append("1");
           } else {
               t1.append("1");
               t2.append("0");
           }
       }
       int res = INT_MAX;
       int diff1 = 0;
       int diff2 = 0;
       int l = 0;
       for (int r = 0; r < s.size(); r++){
           if (s[r] != t1[r]) {
               diff1++;
           }
           if (s[r] != t2[r]) {
               diff2++;
           }
           if ((r - l + 1) > n) {
               if (s[l] != t1[l]) {
                   diff1--;
               }
               if (s[l] != t2[l]) {
                   diff2--;
               }
               l++;
           }
           if (r - l + 1 == n) {
               int temp = min(res, diff1);
               res = min(temp, diff2);
           }
       }
       return res;
    }
};
```
