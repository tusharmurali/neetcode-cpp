# 557. Reverse Words in a String III

- **Difficulty:** Easy  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/reverse-words-in-a-string-iii/>  
- **NeetCode:** <https://neetcode.io/problems/reverse-words-in-a-string-iii>  
- **Video:** <https://www.youtube.com/watch?v=7kUEwiwwnlA>  

[← Back to index](../INDEX.md)

## 1. Convert To String Array

The most straightforward approach splits the string into individual words, reverses each word separately, then joins them back together. By treating each word as an independent unit, we can use built-in string reversal methods on each one. This approach is simple to understand but requires extra space for the split words.

```cpp
class Solution {
public:
    string reverseWords(string s) {
        stringstream ss(s);
        string word, res;
        bool first = true;

        while (ss >> word) {
            reverse(word.begin(), word.end());
            if (first) {
                res += word;
                first = false;
            } else {
                res += " " + word;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. String Manipulation

Instead of splitting into an array, we can build the result string character by character. As we scan through the input, we accumulate characters for each word in reverse order by prepending each new character. When we hit a space, we append the reversed word to our result and reset for the next word. This avoids explicit array operations but involves string concatenation.

```cpp
class Solution {
public:
    string reverseWords(string s) {
        string tmpStr = "";
        string res = "";

        for (int r = 0; r <= s.size(); r++) {
            if (r == s.size() || s[r] == ' ') {
                res += tmpStr;
                tmpStr = "";
                if (r != s.size()) {
                    res += " ";
                }
            } else {
                tmpStr = s[r] + tmpStr;
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 3. Two Pointers - I

We can reverse each word in place by identifying word boundaries and using two pointers to swap characters within each word. As we scan through the string, we track where each word starts. When we encounter a space or reach the end, we know the word boundaries and can reverse that segment. This approach modifies a character array copy of the string directly.

```cpp
class Solution {
public:
    string reverseWords(string s) {
        int l = 0;
        for (int r = 0; r < s.size(); r++) {
            if (r == s.size() - 1 || s[r] == ' ') {
                int tempL = l, tempR = s[r] == ' ' ? r - 1 : r;
                while (tempL < tempR) {
                    swap(s[tempL], s[tempR]);
                    tempL++;
                    tempR--;
                }
                l = r + 1;
            }
        }
        return s;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Two Pointers - II

This is a cleaner variation of the two-pointer approach. Instead of checking for word boundaries at every position, we explicitly find each word by scanning for non-space characters. Once we locate a word's start, we scan to find its end, reverse the word in place, then jump to the next word. This makes the logic more explicit and easier to follow.

```cpp
class Solution {
public:
    string reverseWords(string s) {
        int n = s.size();
        for (int i = 0; i < n; i++) {
            if (s[i] != ' ') {
                int j = i;
                while (j < n && s[j] != ' ') {
                    j++;
                }
                reverse(s, i, j - 1);
                i = j;
            }
        }
        return s;
    }

private:
    void reverse(string& s, int i, int j) {
        while (i < j) {
            swap(s[i], s[j]);
            i++;
            j--;
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$
