# 2864. Maximum Odd Binary Number

- **Difficulty:** Easy  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-odd-binary-number/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-odd-binary-number>  
- **Video:** <https://www.youtube.com/watch?v=EUKLOAv4-IQ>  

[← Back to index](../INDEX.md)

## 1. Sorting

A binary number is odd if and only if its last bit is `1`. To maximize the number, we want as many `1`s as possible in the higher-order positions (leftmost).

We can sort the string in descending order to push all `1`s to the front. Then, we swap one `1` to the last position to ensure the number is odd. Since we sorted in descending order, the rightmost `1` is easy to find.

```cpp
class Solution {
public:
    string maximumOddBinaryNumber(string s) {
        sort(s.begin(), s.end(), greater<char>());

        int n = s.size(), i = n - 1;
        while (i >= 0 && s[i] == '0') {
            i--;
        }

        swap(s[i], s[n - 1]);
        return s;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n)$
- Space complexity: $O(n)$

## 2. Greedy

We do not actually need to sort. The optimal answer has a simple structure: place all but one `1` at the beginning, followed by all `0`s, and end with a single `1`.

We just need to count the `1`s. If there are `count` ones, the result is `(count - 1)` ones, then `(n - count)` zeros, then one `1`.

```cpp
class Solution {
public:
    string maximumOddBinaryNumber(string s) {
        int count = 0;
        for (char c : s) {
            if (c == '1') count++;
        }

        string result((count - 1), '1');
        result += string(s.length() - count, '0');
        result += '1';

        return result;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Two Pointers

We can rearrange the string in-place using a two-pointer technique similar to the partition step in quicksort. We move all `1`s to the left side of the array, then swap one `1` to the last position.

This achieves the same result as sorting but with a single O(n) pass.

```cpp
class Solution {
public:
    string maximumOddBinaryNumber(string s) {
        vector<char> arr(s.begin(), s.end());
        int left = 0;

        for (int i = 0; i < arr.size(); i++) {
            if (arr[i] == '1') {
                swap(arr[left], arr[i]);
                left++;
            }
        }

        swap(arr[left - 1], arr[arr.size() - 1]);
        return string(arr.begin(), arr.end());
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
