# 13. Roman to Integer

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/roman-to-integer/>  
- **NeetCode:** <https://neetcode.io/problems/roman-to-integer>  
- **Video:** <https://www.youtube.com/watch?v=3jdxYj3DD98>  

[← Back to index](../INDEX.md)

## 1. Hash Map

Roman numerals normally add values from left to right. The key insight is handling subtractive notation, where a smaller value before a larger one means subtraction (like IV = 4, not 6). As we scan left to right, if the current symbol is smaller than the next one, we subtract its value; otherwise, we add it. This single rule handles both regular addition and subtractive cases elegantly.

```cpp
class Solution {
public:
    int romanToInt(string s) {
        unordered_map<char, int> roman = {
            {'I', 1}, {'V', 5}, {'X', 10},
            {'L', 50}, {'C', 100}, {'D', 500}, {'M', 1000}
        };

        int res = 0;
        for (int i = 0; i < s.size(); i++) {
            if (i + 1 < s.size() && roman[s[i]] < roman[s[i + 1]]) {
                res -= roman[s[i]];
            } else {
                res += roman[s[i]];
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we have $7$ characters in the hash map.

## Standalone solution file (`cpp/0013-roman-to-integer.cpp` in the NeetCode repo)

```cpp
/*Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.

Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000
For example, 2 is written as II in Roman numeral, just two ones added together. 12 is written as XII, which is simply X + II. The number 27 is written as XXVII, which is XX + V + II.

Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not IIII. Instead, the number four is written as IV. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as IX. There are six instances where subtraction is used:

I can be placed before V (5) and X (10) to make 4 and 9. 
X can be placed before L (50) and C (100) to make 40 and 90. 
C can be placed before D (500) and M (1000) to make 400 and 900.
Given a roman numeral, convert it to an integer. 
Example 3:

Input: s = "MCMXCIV"
Output: 1994
Explanation: M = 1000, CM = 900, XC = 90 and IV = 4. */

int prec(char x){
    switch(x){
        case 'I':
            return 1;
        case 'V':
            return 2;
        case 'X':
            return 3;
        case 'L':
            return 4;
        case 'C':
            return 5;
        case 'D':
            return 6;
        case 'M':
            return 7;
        default:
            return -1;
    }
}

int val(char x){
    switch(x){
        case 'I':
            return 1;
        case 'V':
            return 5;
        case 'X':
            return 10;
        case 'L':
            return 50;
        case 'C':
            return 100;
        case 'D':
            return 500;
        case 'M':
            return 1000;
        default:
            return -1;
    }
}

class Solution {
public:

        int romanToInt(string s)
        {
           int ans = 0;
           
           for(int i=0; i<s.length(); i++){
               if(prec(s[i]) >= prec(s[i+1])){
                   ans += val(s[i]);
               }
               else if(prec(s[i]) < prec(s[i+1])){
                   ans = ans - val(s[i]) + val(s[i+1]);
                   i++;
               }
           }

           return ans;
        }
    
};
```
