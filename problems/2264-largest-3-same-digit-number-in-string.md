# 2264. Largest 3-Same-Digit Number in String

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/largest-3-same-digit-number-in-string/>  
- **NeetCode:** <https://neetcode.io/problems/largest-3-same-digit-number-in-string>  
- **Video:** <https://www.youtube.com/watch?v=vcrOpJQHsSE>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We need to find the largest "good integer" in the string, where a good integer is a substring of length 3 consisting of the same digit repeated three times (like "111", "222", etc.). The straightforward approach is to scan through the string, check every window of size 3, and whenever we find three consecutive identical digits, we compare its numeric value to our current best and keep the larger one.

```cpp
class Solution {
public:
    string largestGoodInteger(string num) {
        string res = "";
        int val = 0;

        for (int i = 0; i < num.length() - 2; i++) {
            if (num[i] == num[i + 1] && num[i] == num[i + 2]) {
                string tmp = num.substr(i, 3);
                if (val <= stoi(tmp)) {
                    val = stoi(tmp);
                    res = tmp;
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Iteration

Instead of tracking both the numeric value and the string separately, we can simplify by using string comparison. Since all good integers have the same length (3 characters), lexicographic comparison works correctly for finding the maximum. For example, "999" > "888" > "777" when compared as strings. We just need to handle the edge case where "000" is a valid result but we need to distinguish it from "no good integer found."

```cpp
class Solution {
public:
    string largestGoodInteger(string num) {
        string res = "0";

        for (int i = 0; i < num.length() - 2; i++) {
            if (num[i] == num[i + 1] && num[i] == num[i + 2]) {
                res = max(res, num.substr(i, 3));
            }
        }

        return res == "0" ? "" : res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 3. Iteration (Optimal)

We can optimize further by observing that we only need to track the digit itself, not the entire 3-character substring. Since all good integers are formed by repeating a single digit three times, we just need to find the largest digit that appears three times consecutively. At the end, we can construct the result by repeating that digit three times.

```cpp
class Solution {
public:
    string largestGoodInteger(string num) {
        int res = -1;

        for (int i = 0; i < num.length() - 2; i++) {
            if (num[i] == num[i + 1] && num[i] == num[i + 2]) {
                res = max(res, num[i] - '0');
            }
        }

        return res != -1 ? string(3, res + '0') : "";
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
