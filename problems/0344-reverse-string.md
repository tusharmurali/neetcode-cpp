# 344. Reverse String

- **Difficulty:** Easy  
- **Pattern:** Two Pointers  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/reverse-string/>  
- **NeetCode:** <https://neetcode.io/problems/reverse-string>  
- **Video:** <https://www.youtube.com/watch?v=_d0T_2Lk2qA>  

[← Back to index](../INDEX.md)

## 1. Array

The simplest approach is to build the reversed string in a separate array. We iterate through the original array from the end to the beginning, collecting characters in a new temporary array. Then we copy the reversed characters back to the original array. This works because reading backward gives us characters in reverse order.

```cpp
class Solution {
public:
    void reverseString(vector<char>& s) {
        vector<char> tmp;
        for (int i = s.size() - 1; i >= 0; i--) {
            tmp.push_back(s[i]);
        }
        for (int i = 0; i < s.size(); i++) {
            s[i] = tmp[i];
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 2. Recursion

We can reverse a string recursively by thinking of it as swapping the outermost characters, then reversing the inner substring. If we have pointers at both ends (`l` and `r`), we first recurse to handle the inner portion, then swap the current pair on the way back up. This naturally reverses the array through the call stack.

```cpp
class Solution {
public:
    void reverseString(vector<char>& s) {
        reverse(s, 0, s.size() - 1);
    }

private:
    void reverse(vector<char>& s, int l, int r) {
        if (l < r) {
            reverse(s, l + 1, r - 1);
            swap(s[l], s[r]);
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for recursion stack.

## 3. Stack

A stack follows Last-In-First-Out (LIFO) order, which is perfect for reversing. If we push all characters onto a `stack`, then pop them off one by one, we get the characters in reverse order. This exploits the stack's natural behavior to achieve the reversal.

```cpp
class Solution {
public:
    void reverseString(vector<char>& s) {
        stack<char> stk;
        for (char& c : s) {
            stk.push(c);
        }
        int i = 0;
        while (!stk.empty()) {
            s[i++] = stk.top();
            stk.pop();
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Built-In Function

Most programming languages provide a built-in method to reverse arrays or lists. These functions are typically optimized and handle the reversal in place efficiently. While this approach is the simplest to write, it hides the underlying algorithm.

```cpp
class Solution {
public:
    void reverseString(vector<char>& s) {
        reverse(s.begin(), s.end());
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 5. Two Pointers

The most efficient approach uses two pointers starting at opposite ends of the array. We swap the characters at these pointers, then move them toward each other. When the pointers meet or cross, every character has been swapped exactly once, and the array is reversed. This achieves O(1) space since we only swap in place.

```cpp
class Solution {
public:
    void reverseString(vector<char>& s) {
        int l = 0, r = s.size() - 1;
        while (l < r) {
            swap(s[l++], s[r--]);
        }
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## Standalone solution file (`cpp/0344-reverse-string.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    void reverseString(vector<char>& s) {
        int left = 0, right = s.size() - 1;
        
        while (left < right){
            swap(s[left], s[right]);
            
            left++;
            right--;
        }
    }
};
```
