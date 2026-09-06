# 1056. Confusing Number

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/confusing-number/>  
- **NeetCode:** <https://neetcode.io/problems/confusing-number>  

[← Back to index](../INDEX.md)

## 1. Invert and Reverse

A confusing number looks different when rotated 180 degrees. Only digits `0`, `1`, `6`, `8`, and `9` remain valid after rotation (`6` becomes `9` and vice versa). We invert each digit, reverse the result, and check if it differs from the original.

```cpp
class Solution {
public:
    bool confusingNumber(int n) {
        // Use 'invertMap' to invert each valid digit.
        unordered_map<char, char> invertMap = {{'0','0'}, {'1','1'}, {'6','9'}, {'8','8'}, {'9','6'}};
        string rotatedNumber;

        // Iterate over each digit of 'n'.
        for (auto ch : to_string(n)) {
            if (invertMap.find(ch) == invertMap.end()) {
                return false;
            }

            // Append the inverted digit of 'ch' to the end of 'rotatedNumber'.
            rotatedNumber += invertMap[ch];
        }

        // Check if the reversed 'rotatedNumber' equals 'n'.
        reverse(begin(rotatedNumber), end(rotatedNumber));
        return stoi(rotatedNumber) != n;
    }
};
```

**Complexity**

- Time complexity: $O(L)$
- Space complexity: $O(L)$ extra space used

> Where $L$ is the maximum number of digits $n$ can have ($L = \log_{10} n$).

## 2. Use the remainder

Instead of converting to a string, we can extract digits using modular arithmetic. Processing digits from right to left while building the rotated number from left to right naturally produces the reversed rotated version.

```cpp
class Solution {
public:
    bool confusingNumber(int n) {
        // Use 'invertMap' to invert each valid digit. Since we don't want to modify
        // 'n', we create a copy of it as 'nCopy'.
        map<int, int> invertMap = {{0, 0}, {1, 1}, {6, 9}, {8, 8}, {9, 6}};
        int rotatedNumber = 0, nCopy = n;

        // Get every digit of 'nCopy' by taking the remainder of it to 10.
        while (nCopy > 0) {
            int res = nCopy % 10;
            if (invertMap.find(res) == invertMap.end()) {
                return false;
            }

            // Append the inverted digit of 'res' to the end of 'rotatedNumber'.
            rotatedNumber = rotatedNumber * 10 + invertMap[res];
            nCopy /= 10;
        }

        // Check if 'rotatedNumber' equals 'n'.
        return rotatedNumber != n;
    }
};
```

**Complexity**

- Time complexity: $O(L)$
- Space complexity: $O(L)$ extra space used

> Where $L$ is the maximum number of digits $n$ can have.
