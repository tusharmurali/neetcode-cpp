# 168. Excel Sheet Column Title

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/excel-sheet-column-title/>  
- **NeetCode:** <https://neetcode.io/problems/excel-sheet-column-title>  
- **Video:** <https://www.youtube.com/watch?v=X_vJDpCCuoA>  

[← Back to index](../INDEX.md)

## 1. Recursion

Excel columns use a bijective base-26 system where A=1, B=2, ..., Z=26. Unlike standard base conversion where digits range from 0 to base-1, here digits range from 1 to 26. This means we need to adjust by subtracting 1 before finding each digit.

After subtracting 1, we can use modulo 26 to find the rightmost character and divide by 26 to get the remaining prefix. Recursion handles this naturally: first solve for the prefix (if any), then append the current character.

```cpp
class Solution {
public:
    string convertToTitle(int columnNumber) {
        if (columnNumber == 0) {
            return "";
        }
        int n = columnNumber - 1;
        return convertToTitle(n / 26) + char('A' + n % 26);
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(\log n)$ for recursion stack.

> Where $n$ is the given column number.

## 2. Iteration

The iterative approach works from right to left, building the result string in reverse. At each step, we extract the rightmost character, then reduce the number for the next iteration. Since we build characters from least significant to most significant, we reverse the result at the end.

This avoids recursion overhead and makes the process explicit: subtract 1, find the character via modulo, divide by 26, and repeat until the number becomes 0.

```cpp
class Solution {
public:
    string convertToTitle(int columnNumber) {
        string res;
        while (columnNumber > 0) {
            columnNumber--;
            int offset = columnNumber % 26;
            res += ('A' + offset);
            columnNumber /= 26;
        }
        reverse(res.begin(), res.end());
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$ extra space.

> Where $n$ is the given column number.
