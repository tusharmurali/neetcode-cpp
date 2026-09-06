# 1291. Sequential Digits

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/sequential-digits/>  
- **NeetCode:** <https://neetcode.io/problems/sequential-digits>  
- **Video:** <https://www.youtube.com/watch?v=Q-ca65wRJyI>  

[← Back to index](../INDEX.md)

## 1. Brute Force

A sequential digit number has digits that increase by exactly 1 from left to right (like 123 or 4567). The straightforward approach is to check every number in the range `[low, high]` and verify if it has sequential digits by comparing adjacent digit characters. While simple to implement, this becomes impractical for large ranges.

```cpp
class Solution {
public:
    vector<int> sequentialDigits(int low, int high) {
        vector<int> res;
        for (int num = low; num <= high; num++) {
            string s = to_string(num);
            bool flag = true;
            for (int i = 1; i < s.size(); i++) {
                if (s[i] - s[i - 1] != 1) {
                    flag = false;
                    break;
                }
            }
            if (flag) {
                res.push_back(num);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$

## 2. Simulation

Instead of checking every number, we can generate only the valid sequential digit numbers directly. For a number with `d` digits starting with digit `s`, we can build it by appending consecutive digits. For example, starting with 3 and building a 4-digit number gives us 3456. We iterate over all valid digit lengths and starting digits, constructing each candidate and checking if it falls within `[low, high]`.

```cpp
class Solution {
public:
    vector<int> sequentialDigits(int low, int high) {
        vector<int> res;
        int lowDigit = to_string(low).length();
        int highDigit = to_string(high).length();

        for (int digits = lowDigit; digits <= highDigit; digits++) {
            for (int start = 1; start < 10; start++) {
                if (start + digits > 10) {
                    break;
                }
                int num = start;
                int prev = start;
                for (int i = 1; i < digits; i++) {
                    num = num * 10 + (++prev);
                }
                if (num >= low && num <= high) {
                    res.push_back(num);
                }
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

> Since, we have at most $36$ valid numbers as per the given constraints.

## 3. Breadth First Search

We can think of generating sequential digit numbers as a BFS traversal. Start with single digits 1 through 9 in a queue. For each number, we can extend it by appending the next consecutive digit (if the last digit is less than 9). Processing the queue level by level naturally generates numbers in increasing order of length, and within each length, in increasing order of value.

```cpp
class Solution {
public:
    vector<int> sequentialDigits(int low, int high) {
        vector<int> res;
        queue<int> queue;

        for (int i = 1; i < 10; i++) {
            queue.push(i);
        }

        while (!queue.empty()) {
            int n = queue.front();
            queue.pop();

            if (n > high) {
                continue;
            }
            if (n >= low && n <= high) {
                res.push_back(n);
            }
            int ones = n % 10;
            if (ones < 9) {
                queue.push(n * 10 + (ones + 1));
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

> Since, we have at most $36$ valid numbers as per the given constraints.

## 4. Depth First Search

DFS provides another way to enumerate sequential digit numbers. Starting from each single digit (1 to 9), we recursively extend the number by appending the next digit. The recursion naturally explores all valid sequential numbers. Since we start from different initial digits and explore in order, the results may not be sorted, so we sort at the end.

```cpp
class Solution {
public:
    vector<int> sequentialDigits(int low, int high) {
        vector<int> res;
        for (int i = 1; i < 10; i++) {
            dfs(i, low, high, res);
        }
        sort(res.begin(), res.end());
        return res;
    }

private:
    void dfs(int num, int low, int high, vector<int>& res) {
        if (num > high) {
            return;
        }
        if (num >= low) {
            res.push_back(num);
        }
        int lastDigit = num % 10;
        if (lastDigit < 9) {
            dfs(num * 10 + (lastDigit + 1), low, high, res);
        }
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

> Since, we have at most $36$ valid numbers as per the given constraints.

## 5. Sliding Window

All sequential digit numbers are substrings of "123456789". A 2-digit sequential number is a substring of length 2, a 3-digit one is length 3, and so on. By sliding a window of each valid length across this master string and converting substrings to integers, we generate all possible sequential digit numbers directly.

```cpp
class Solution {
public:
    vector<int> sequentialDigits(int low, int high) {
        string nums = "123456789";
        vector<int> res;

        for (int d = 2; d <= 9; d++) {
            for (int i = 0; i <= 9 - d; i++) {
                int num = stoi(nums.substr(i, d));
                if (num > high) {
                    break;
                }
                if (num >= low && num <= high) {
                    res.push_back(num);
                }
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$

> Since, we have at most $36$ valid numbers as per the given constraints.
