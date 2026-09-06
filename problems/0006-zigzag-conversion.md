# 6. Zigzag Conversion

- **Difficulty:** Medium  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/zigzag-conversion/>  
- **NeetCode:** <https://neetcode.io/problems/zigzag-conversion>  
- **Video:** <https://www.youtube.com/watch?v=Q2Tw6gcVEwc>  

[← Back to index](../INDEX.md)

## 1. Iteration - I

When writing characters in a zigzag pattern, each row follows a predictable spacing pattern. The key insight is that the distance between characters in the same row follows a cycle of length `2 * (numRows - 1)`. For the first and last rows, characters appear at regular intervals of this cycle length. For middle rows, there are two characters per cycle: one at the regular position and one at a calculated offset within the `cycle`.

```cpp
class Solution {
public:
    string convert(string s, int numRows) {
        if (numRows == 1) {
            return s;
        }

        string res;
        int len = s.size();

        for (int r = 0; r < numRows; r++) {
            int increment = 2 * (numRows - 1);
            for (int i = r; i < len; i += increment) {
                res += s[i];
                if (r > 0 && r < numRows - 1 && i + increment - 2 * r < len) {
                    res += s[i + increment - 2 * r];
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for the ouput string.

## 2. Iteration - II

Instead of calculating positions mathematically, we can simulate the actual zigzag writing process. We maintain a current `row` and a `direction`. As we traverse the string, we place each character in its corresponding row. When we hit the top or bottom row, we reverse `direction`. This approach directly models how characters would be written in the zigzag pattern.

```cpp
class Solution {
public:
    string convert(string s, int numRows) {
        if (numRows == 1 || numRows >= s.size()) {
            return s;
        }

        vector<string> res(numRows);
        int row = 0, dir = 1;

        for (char& c : s) {
            res[row] += c;
            row += dir;
            if (row == 0 || row == numRows - 1) {
                dir *= -1;
            }
        }

        string result;
        for (string& rowString : res) {
            result += rowString;
        }
        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for the output string.

## Standalone solution file (`cpp/0006-zigzag-conversion.cpp` in the NeetCode repo)

```cpp
/*
    For each row the next chracter is at index 2 * (n -1) and 
    For middle rows there will be extra characters
    Time: O(n)
    Space: O(1)
*/
class Solution {
public:
    string convert(string s, int n) {
        // Edge case
        if(n == 1) return s;
        // Other cases
        // Take string to store answer
        string ans = "";
        // We are going to traverse each row
        for(int row = 0; row < n ; row++){
            // for each row the next chracter is at index 2 *  (n -1) 
            int increment = 2 *  (n -1);
            // For first and last rows 
            for(int i = row; i < s.length(); i+= increment){
                ans += s[i];
                // For middle rows there will be extra characters
                if(row > 0 && row < n-1 && i+increment - 2 * row < s.length()){
                    ans += s[i+increment - 2 * row];
                }
            }
        }
        return ans;
    }
};
```
