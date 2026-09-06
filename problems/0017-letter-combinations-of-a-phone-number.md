# 17. Letter Combinations of a Phone Number

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/letter-combinations-of-a-phone-number/>  
- **NeetCode:** <https://neetcode.io/problems/combinations-of-a-phone-number>  
- **Video:** <https://www.youtube.com/watch?v=0snEunUacZY>  

[← Back to index](../INDEX.md)

## 1. Backtracking

Each digit maps to a set of characters (like on a phone keypad).  
The task is to **choose one character per digit**, in order, and generate **all possible combinations**.

Think of it as building a string **step by step**:

- At index `i`, pick **one character** from the mapping of `digits[i]`
- Move to the next digit
- When the length of the built string equals the number of digits, we have formed **one valid combination**

This is a classic **decision tree** problem:

- Each level - one digit
- Each branch - one possible character for that digit

Backtracking lets us explore all branches efficiently.

```cpp
class Solution {
public:
    vector<string> res;
    vector<string> digitToChar = {"", "", "abc", "def", "ghi", "jkl",
                                  "mno", "qprs", "tuv", "wxyz"};

    vector<string> letterCombinations(string digits) {
        if (digits.empty()) return res;
        backtrack(0, "", digits);
        return res;
    }

    void backtrack(int i, string curStr, string &digits) {
        if (curStr.size() == digits.size()) {
            res.push_back(curStr);
            return;
        }
        string chars = digitToChar[digits[i] - '0'];
        for (char c : chars) {
            backtrack(i + 1, curStr + c, digits);
        }
    }
};
```

**Complexity**

- Time complexity: $O(n * 4 ^ n)$
- Space complexity:
    - $O(n)$ extra space.
    - $O(n * 4 ^ n)$ space for the output list.

## 2. Iteration

Instead of using recursion, we **build combinations level by level**.

Start with an empty string.
For each digit:

- Take all combinations built so far
- Append every possible character mapped to the current digit
- This creates a new list of combinations

This is similar to **BFS / level-wise expansion**:

- Each digit adds a new "layer" of characters
- Combinations grow step by step until all digits are processed

```cpp
class Solution {
public:
    vector<string> letterCombinations(string digits) {
        if (digits.empty()) return {};

        vector<string> res = {""};
        vector<string> digitToChar = {
            "", "", "abc", "def", "ghi", "jkl",
            "mno", "qprs", "tuv", "wxyz"
        };

        for (char digit : digits) {
            vector<string> tmp;
            for (string &curStr : res) {
                for (char c : digitToChar[digit - '0']) {
                    tmp.push_back(curStr + c);
                }
            }
            res = tmp;
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * 4 ^ n)$
- Space complexity:
    - $O(n)$ extra space.
    - $O(n * 4 ^ n)$ space for the output list.

## Standalone solution file (`cpp/0017-letter-combinations-of-a-phone-number.cpp` in the NeetCode repo)

```cpp
/*
    Given cell phone pad, return all possible letter combos that the number could represent
    Ex. digits = "23" -> ["ad","ae","af","bd","be","bf","cd","ce","cf"]

    Hash map all digits to letters, add 1 letter at a time for each digit, then backtrack undo

    Time: O(n x 4^n)
    Space: O(n x 4^n)
*/

class Solution {
public:
    vector<string> letterCombinations(string digits) {
        if (digits.empty()) {
            return {};
        }
        
        unordered_map<char, string> m = {
            {'2', "abc"},
            {'3', "def"},
            {'4', "ghi"},
            {'5', "jkl"},
            {'6', "mno"},
            {'7', "pqrs"},
            {'8', "tuv"},
            {'9', "wxyz"}
        };
        string curr = "";
        vector<string> result;
        
        dfs(digits, 0, m, curr, result);
        return result;
    }
private:
    void dfs(string digits, int index, unordered_map<char, string>& m, string& curr, vector<string>& result) {
        if (index == digits.size()) {
            result.push_back(curr);
            return;
        }
        string str = m[digits[index]];
        for (int i = 0; i < str.size(); i++) {
            curr.push_back(str[i]);
            dfs(digits, index + 1, m, curr, result);
            curr.pop_back();
        }
    }
};
```
