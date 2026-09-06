# 12. Integer to Roman

- **Difficulty:** Medium  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/integer-to-roman/>  
- **NeetCode:** <https://neetcode.io/problems/integer-to-roman>  
- **Video:** <https://www.youtube.com/watch?v=ohBNdSJyLh8>  

[← Back to index](../INDEX.md)

## 1. Math - I

Roman numerals are built by combining symbols that represent specific values. The key insight is to process values from largest to smallest, repeatedly subtracting the largest possible value and appending its symbol. We include the subtractive combinations (like IV for 4, IX for 9) in our value list to handle them naturally.

```cpp
class Solution {
public:
    string intToRoman(int num) {
        vector<pair<string, int>> symList = {
            {"I", 1}, {"IV", 4}, {"V", 5}, {"IX", 9},
            {"X", 10}, {"XL", 40}, {"L", 50}, {"XC", 90},
            {"C", 100}, {"CD", 400}, {"D", 500}, {"CM", 900},
            {"M", 1000}
        };

        string res = "";
        for (int i = symList.size() - 1; i >= 0; i--) {
            string sym = symList[i].first;
            int val = symList[i].second;
            int count = num / val;
            if (count > 0) {
                res.append(count, sym[0]);
                if (sym.size() == 2) res.append(1, sym[1]);
                num %= val;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## 2. Math - II

Since the input is constrained to 1-3999, we can precompute all possible Roman representations for each digit place (ones, tens, hundreds, thousands). Then we simply look up each digit and concatenate the results. This trades space for simplicity and speed.

```cpp
class Solution {
public:
    string intToRoman(int num) {
        string thousands[] = {"", "M", "MM", "MMM"};
        string hundreds[] = {"", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"};
        string tens[] = {"", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"};
        string ones[] = {"", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"};

        return thousands[num / 1000] +
               hundreds[(num % 1000) / 100] +
               tens[(num % 100) / 10] +
               ones[num % 10];
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0012-integer-to-roman.cpp` in the NeetCode repo)

```cpp
/* Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.

Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000
For example, 2 is written as II in Roman numeral, just two one's added together. 12 is written as XII, which is simply X + II. The number 27 is written as XXVII, which is XX + V + II.

Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not IIII. Instead, the number four is written as IV. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as IX. There are six instances where subtraction is used:

I can be placed before V (5) and X (10) to make 4 and 9. 
X can be placed before L (50) and C (100) to make 40 and 90. 
C can be placed before D (500) and M (1000) to make 400 and 900.
Given an integer, convert it to a roman numeral.
Example 
Input: num = 1994
Output: "MCMXCIV"
Explanation: M = 1000, CM = 900, XC = 90 and IV = 4. */

class Solution {
public:
    string intToRoman(int num) {
       string s="";
       while(num>=1000)
       {
           s+="M";
           num=num-1000;
       }
       if(num>=900)
       {
           s+="CM";
           num=num-900;
       }
       while(num>=500)
       {
           s+="D";
           num=num-500;
       }
       if(num>=400)
       {
           s+="CD";
           num=num-400;
       }
       while(num>=100)
       {
           s+="C";
           num=num-100;
       }
       if(num>=90)
       {
           s+="XC";
           num=num-90;
       }
       while(num>=50)
       {
           s+="L";
           num=num-50;
       }
       if(num>=40)
       {
           s+="XL";
           num=num-40;
       }
       while(num>=10)
       {
           s+="X";
           num=num-10;
       }
       if(num>=9)
       {
           s+="IX";
           num=num-9;
       }
       while(num>=5)
       {
           s+="V";
           num=num-5;
       }
       if(num>=4)
       {
           s+="IV";
           num=num-4;
       }
       while(num>=1)
       {
           s+="I";
           num=num-1;
       }
       return s; 
    }
};
```
