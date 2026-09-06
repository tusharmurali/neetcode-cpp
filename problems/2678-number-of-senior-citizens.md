# 2678. Number of Senior Citizens

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-senior-citizens/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-senior-citizens>  
- **Video:** <https://www.youtube.com/watch?v=l6_wwKzFmVo>  

[← Back to index](../INDEX.md)

## 1. String Parsing

Each passenger detail string has a fixed format where the age is encoded at positions 11 and 12 (0-indexed). We need to extract these two characters as a substring, convert them to an integer, and check if the age exceeds 60. This is a straightforward string slicing operation.

```cpp
class Solution {
public:
    int countSeniors(vector<string>& details) {
        int res = 0;
        for (const string& d : details) {
            if (stoi(d.substr(11, 2)) > 60) {
                res++;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Character-Based Extraction

Instead of creating a substring and parsing it, we can directly extract the two digit characters and compute the age mathematically. By subtracting the ASCII value of '0' from each character, we get the numeric value of that digit. The tens digit is at index 11 and the ones digit is at index 12. Combining them gives us the age without any string allocation overhead.

```cpp
class Solution {
public:
    int countSeniors(vector<string>& details) {
        int res = 0;
        for (const string& d : details) {
            int ten = d[11] - '0';
            int one = d[12] - '0';
            int age = one + 10 * ten;
            if (age > 60) {
                res++;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
