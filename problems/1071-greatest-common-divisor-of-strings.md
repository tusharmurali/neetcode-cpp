# 1071. Greatest Common Divisor of Strings

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/greatest-common-divisor-of-strings/>  
- **NeetCode:** <https://neetcode.io/problems/greatest-common-divisor-of-strings>  
- **Video:** <https://www.youtube.com/watch?v=i5I_wrbUdzM>  

[← Back to index](../INDEX.md)

## 1. Iteration

A string `t` divides both `str1` and `str2` only if its length divides both string lengths and repeating `t` the appropriate number of times reconstructs each string. We search for the longest such divisor by checking all possible lengths from the minimum length down to `1`.

```cpp
class Solution {
public:
    string gcdOfStrings(string str1, string str2) {
        int len1 = str1.size(), len2 = str2.size();

        auto isDivisor = [&](int l) {
            if (len1 % l != 0 || len2 % l != 0) {
                return false;
            }
            string sub = str1.substr(0, l);
            int f1 = len1 / l, f2 = len2 / l;
            string repeated1 = "", repeated2 = "";
            for (int i = 0; i < f1; ++i) repeated1 += sub;
            for (int i = 0; i < f2; ++i) repeated2 += sub;
            return repeated1 == str1 && repeated2 == str2;
        };

        for (int l = min(len1, len2); l > 0; l--) {
            if (isDivisor(l)) {
                return str1.substr(0, l);
            }
        }

        return "";
    }
};
```

**Complexity**

- Time complexity: $O(min(m, n) * (m + n))$
- Space complexity: $O(m + n)$

> Where $m$ and $n$ are the lengths of the strings $str1$ and $str2$ respectively.

## 2. Iteration (Space Optimized)

Instead of constructing repeated strings and comparing them (which uses extra space), we can validate a candidate divisor by checking character-by-character using modular indexing. Each character at position `i` should match the character at position `i % l` in the candidate prefix.

```cpp
class Solution {
public:
    string gcdOfStrings(string str1, string str2) {
        int m = str1.size(), n = str2.size();
        if (m < n) {
            swap(m, n);
            swap(str1, str2);
        }

        for (int l = n; l > 0; l--) {
            if (m % l != 0 || n % l != 0) {
                continue;
            }

            bool valid = true;
            for (int i = 0; i < m; i++) {
                if (str1[i] != str2[i % l]) {
                    valid = false;
                    break;
                }
            }
            if (!valid) continue;

            for (int i = l; i < n; i++) {
                if (str2[i] != str2[i % l]) {
                    valid = false;
                    break;
                }
            }
            if (valid) {
                return str2.substr(0, l);
            }
        }

        return "";
    }
};
```

**Complexity**

- Time complexity: $O(min(m, n) * (m + n))$
- Space complexity: $O(g)$ for the output string.

> Where $m$ is the length of the string $str1$, $n$ is the length of the string $str2$, and $g$ is the length of the output string.

## 3. Greatest Common Divisor

If a common divisor string exists, then concatenating the two strings in either order must produce the same result: `str1 + str2 == str2 + str1`. This is because both strings are built from the same repeating pattern. Once verified, the GCD of the two string lengths gives us the length of the largest common divisor.

```cpp
class Solution {
public:
    string gcdOfStrings(string str1, string str2) {
        if (str1 + str2 != str2 + str1) {
            return "";
        }
        int g = __gcd((int)str1.size(), (int)str2.size());
        return str1.substr(0, g);
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity: $O(m + n)$.

> Where $m$ and $n$ are the lengths of the strings $str1$ and $str2$ respectively.

## 4. Greatest Common Divisor (Space Optimized)

We can avoid the concatenation check (which requires O(m+n) space) by directly validating the divisor property. Compute the GCD of the lengths, then verify that every character in both strings matches the corresponding character in the first `g` characters, using modular indexing.

```cpp
class Solution {
public:
    string gcdOfStrings(string str1, string str2) {
        int g = __gcd((int)str1.size(), (int)str2.size());

        for (int i = 0; i < str1.size(); i++) {
            if (str1[i] != str1[i % g]) {
                return "";
            }
        }

        for (int i = 0; i < str2.size(); i++) {
            if (str2[i] != str1[i % g]) {
                return "";
            }
        }

        return str1.substr(0, g);
    }
};
```

**Complexity**

- Time complexity: $O(m + n)$
- Space complexity: $O(g)$ for the output string.

> Where $m$ is the length of the string $str1$, $n$ is the length of the string $str2$, and $g$ is the GCD of $m$ and $n$.

## Standalone solution file (`cpp/1071-greatest-common-divisor-of-strings.cpp` in the NeetCode repo)

```cpp
/**
 *  Time Complexity: O(n^2) 
 *  Space Complexity: O(1)
 */

class Solution {
public:
    string gcdOfStrings(string str1, string str2) {
        string shortest, longest;
        
        if(str1.length() < str2.length()){
            shortest = str1;
            longest = str2;
        }
        else{
            shortest = str2;
            longest = str1;
        }

        string solution = "";   
        ushort shortest_length = shortest.length();
        ushort longest_length = longest.length();

        for(ushort i = shortest_length; i > 0; --i)
        {   
            if (longest_length % i != 0 || shortest_length % i != 0) continue;

            for(ushort j = 0; j < longest_length; ++j)
            {
                ushort first_pointer = j % i;
                ushort second_pointer = j % shortest_length;

                if(shortest[first_pointer] != longest[j] || shortest[second_pointer] != longest[j])
                {
                    solution = "";
                    break;
                }

                if(first_pointer == j) solution += longest[j];
            }
            
            if(solution != "") return solution;
        }

        return "";
    }
};
```
