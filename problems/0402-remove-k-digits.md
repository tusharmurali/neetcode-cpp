# 402. Remove K Digits

- **Difficulty:** Medium  
- **Pattern:** Stack  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/remove-k-digits/>  
- **NeetCode:** <https://neetcode.io/problems/remove-k-digits>  
- **Video:** <https://www.youtube.com/watch?v=cFabMOnJaq0>  

[← Back to index](../INDEX.md)

## 1. Brute Force

To make the smallest possible number, we want smaller digits to appear earlier.
If a digit is followed by a smaller digit, removing the larger one produces a smaller result.
We repeatedly find the first position where a digit is greater than its successor and remove it.
After `k` removals, we strip leading zeros and return the result.

```cpp
class Solution {
public:
    string removeKdigits(string num, int k) {
        while (k > 0) {
            int i = 1;
            while (i < num.size() && num[i] >= num[i - 1]) {
                i++;
            }
            num.erase(i - 1, 1);
            k--;
        }

        int i = 0;
        while (i < num.size() && num[i] == '0') {
            i++;
        }

        num = num.substr(i);
        return num.empty() ? "0" : num;
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(1)$ or $O(n)$ depending on the language.

## 2. Greedy + Stack

The brute force approach rescans the string after each removal, which is inefficient.
A stack lets us make decisions in a single pass.
As we process each digit, we pop from the stack whenever the top is larger than the current digit and we still have removals left.
This greedily ensures that smaller digits bubble up to the front.

```cpp
class Solution {
public:
    string removeKdigits(string num, int k) {
        string stack;
        for (char c : num) {
            while (k > 0 && !stack.empty() && stack.back() > c) {
                stack.pop_back();
                k--;
            }
            stack.push_back(c);
        }

        while (k > 0 && !stack.empty()) {
            stack.pop_back();
            k--;
        }

        int i = 0;
        while (i < stack.size() && stack[i] == '0') {
            i++;
        }

        string res = stack.substr(i);
        return res.empty() ? "0" : res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Two Pointers

Instead of using a separate stack, we can simulate stack behavior in place using two pointers.
The left pointer `l` represents the top of our virtual stack, while the right pointer `r` scans through the input.
When we see a smaller digit, we backtrack `l` to remove larger digits, then place the current digit.
This achieves the same greedy logic with better space efficiency.

```cpp
class Solution {
public:
    string removeKdigits(string num, int k) {
        int l = 0;
        for (int r = 0; r < num.size(); r++) {
            while (l > 0 && k > 0 && num[l - 1] > num[r]) {
                l--;
                k--;
            }
            num[l++] = num[r];
        }

        l -= k;
        int i = 0;
        while (i < l && num[i] == '0') {
            i++;
        }
        if (i == l) return "0";
        return num.substr(i, l - i);
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ or $O(n)$ depending on the language.

## Standalone solution file (`cpp/0402-remove-k-digits.cpp` in the NeetCode repo)

```cpp
// Time Complexity is O(N) where N is the size of the input string.
// Space complexity is O(N) as well
class Solution {
public:
    string removeKdigits(string num, int k) {
      int n = num.size();
      
      stack<char>s;
      int count = k;
      
      for(int i = 0 ; i < n; i++)
      {
        while(!s.empty() && count > 0 && s.top() > num[i])
        {
          s.pop();
          count--;
        }
        s.push(num[i]);
      }
      
      // In case the num was already in a non increasing order (e.x: 123456)
      while(s.size() != n - k) s.pop();
     
      string res = "";
      while(!s.empty())
      {
        res += s.top();
        s.pop();
      }
      reverse(res.begin() , res.end());
      // Remove the zeros from the left if they exist.
      while (res[0] == '0') res.erase(0 , 1);
    
      
      return (res == "") ? "0": res;
    }
};
```
