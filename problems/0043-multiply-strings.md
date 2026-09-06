# 43. Multiply Strings

- **Difficulty:** Medium  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode 150, NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/multiply-strings/>  
- **NeetCode:** <https://neetcode.io/problems/multiply-strings>  
- **Video:** <https://www.youtube.com/watch?v=1vZswirL8Y8>  

[← Back to index](../INDEX.md)

## 1. Multiplication & Addition

This approach mimics how we multiply numbers by hand. We multiply the larger number by each digit of the smaller number (starting from the rightmost digit), shifting the result appropriately by appending zeros. Then we add all these partial products together. This simulates the grade-school multiplication algorithm but operates entirely on strings to handle arbitrarily large numbers.

```cpp
class Solution {
public:
    string multiply(string num1, string num2) {
        if (num1 == "0" || num2 == "0") return "0";

        if (num1.size() < num2.size()) {
            return multiply(num2, num1);
        }

        string res = "";
        int zero = 0;
        for (int i = num2.size() - 1; i >= 0; --i) {
            string cur = mul(num1, num2[i], zero);
            res = add(res, cur);
            zero++;
        }

        return res;
    }

    string mul(string s, char d, int zero) {
        int i = s.size() - 1, carry = 0;
        int digit = d - '0';
        string cur;

        while (i >= 0 || carry) {
            int n = (i >= 0) ? s[i] - '0' : 0;
            int prod = n * digit + carry;
            cur.push_back((prod % 10) + '0');
            carry = prod / 10;
            i--;
        }

        reverse(cur.begin(), cur.end());
        return cur + string(zero, '0');
    }

    string add(string num1, string num2) {
        int i = num1.size() - 1, j = num2.size() - 1, carry = 0;
        string res;

        while (i >= 0 || j >= 0 || carry) {
            int n1 = (i >= 0) ? num1[i] - '0' : 0;
            int n2 = (j >= 0) ? num2[j] - '0' : 0;
            int total = n1 + n2 + carry;
            res.push_back((total % 10) + '0');
            carry = total / 10;
            i--;
            j--;
        }

        reverse(res.begin(), res.end());
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(min(m, n) * (m + n))$
- Space complexity: $O(m + n)$

> Where $m$ is the length of the string $num1$ and $n$ is the length of the string $num2$.

## 2. Multiplication

Instead of generating partial products and adding them as separate strings, we can use a single result array to accumulate all digit multiplications in place. When we multiply digit `i` of `num1` by digit `j` of `num2`, the result contributes to position `i + j` in the final answer. By reversing both strings first, we can work with indices that naturally align with place values. After processing all digit pairs, we handle carries and convert the result array back to a string.

```cpp
class Solution {
public:
    string multiply(string num1, string num2) {
        if (num1 == "0" || num2 == "0") {
            return "0";
        }

        vector<int> res(num1.length() + num2.length(), 0);
        reverse(num1.begin(), num1.end());
        reverse(num2.begin(), num2.end());
        for (int i1 = 0; i1 < num1.length(); i1++) {
            for (int i2 = 0; i2 < num2.length(); i2++) {
                int digit = (num1[i1] - '0') * (num2[i2] - '0');
                res[i1 + i2] += digit;
                res[i1 + i2 + 1] += res[i1 + i2] / 10;
                res[i1 + i2] %= 10;
            }
        }

        stringstream result;
        int i = res.size() - 1;
        while (i >= 0 && res[i] == 0) {
            i--;
        }
        while (i >= 0) {
            result << res[i--];
        }
        return result.str();
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m + n)$

> Where $m$ is the length of the string $num1$ and $n$ is the length of the string $num2$.

## Standalone solution file (`cpp/0043-multiply-strings.cpp` in the NeetCode repo)

```cpp
/*
    Given 2 ints represented as strings, return product, also represented as a string
    Ex. num1 = "2" num2 = "3" -> "6", num1 = "123" num2 = "456" -> "56088"

    Standard multiplication, right to left per digit, compute sums & carries at each pos

    Time: O(m x n)
    Space: O(m + n)
*/

class Solution {
public:
    string multiply(string num1, string num2) {
        int m = num1.size();
        int n = num2.size();
        
        string result(m + n, '0');
        
        for (int i = m - 1; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                int sum = (num1[i] - '0') * (num2[j] - '0') + (result[i + j + 1] - '0');
                result[i + j + 1] = sum % 10 + '0';
                result[i + j] += sum / 10;
            }
        }
        
        for (int i = 0; i < m + n; i++) {
            if (result[i] != '0') {
                return result.substr(i);
            }
        }
        return "0";
    }
};
```
