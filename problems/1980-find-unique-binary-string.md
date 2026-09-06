# 1980. Find Unique Binary String

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/find-unique-binary-string/>  
- **NeetCode:** <https://neetcode.io/problems/find-unique-binary-string>  
- **Video:** <https://www.youtube.com/watch?v=aHqn4Dynd1k>  
- **Video approach:** 1. Backtracking (Recursion) (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Backtracking (Recursion) ▶ video

We need to find any binary string of length `n` that is not in the given array. Since there are `2^n` possible strings but only `n` strings in the input, at least one must be missing. We can systematically try building strings character by character, checking at each complete string whether it exists in the set.

```cpp
class Solution {
public:
    string findDifferentBinaryString(vector<string>& nums) {
        unordered_set<string> strSet(nums.begin(), nums.end());
        string cur(nums.size(), '0');
        return backtrack(0, cur, strSet, nums.size());
    }

private:
    string backtrack(int i, string& cur, unordered_set<string>& strSet, int n) {
        if (i == n) {
            return strSet.count(cur) ? "" : cur;
        }

        string res = backtrack(i + 1, cur, strSet, n);
        if (!res.empty()) return res;

        cur[i] = '1';
        return backtrack(i + 1, cur, strSet, n);
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Backtracking (Iteration)

Instead of recursive backtracking, we can iterate through all possible binary strings from 0 to n (we only need n+1 candidates since there are n input strings). Convert each number to its binary representation, pad it to length n, and check if it exists in the set.

```cpp
class Solution {
public:
    string findDifferentBinaryString(vector<string>& nums) {
        unordered_set<string> strSet(nums.begin(), nums.end());
        int n = nums.size();

        for (int num = 0; num < (n + 1); num++) {
            string res = toBinaryString(num, n);
            if (strSet.find(res) == strSet.end()) {
                return res;
            }
        }

        return "";
    }

private:
    string toBinaryString(int num, int length) {
        string res = "";
        for (int i = length - 1; i >= 0; i--) {
            res += (num & (1 << i)) ? '1' : '0';
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 3. Cantor's Diagonal Argument

Cantor's diagonal argument provides an elegant O(n) solution. For each string `nums[i]`, we look at its `i`-th character and flip it. The resulting string differs from `nums[0]` at position 0, from `nums[1]` at position 1, and so on. This guarantees the constructed string differs from every input string at at least one position.

```cpp
class Solution {
public:
    string findDifferentBinaryString(vector<string>& nums) {
        string res;
        for (int i = 0; i < nums.size(); i++) {
            res += (nums[i][i] == '0') ? '1' : '0';
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity:
    - $O(1)$ extra space.
    - $O(n)$ space for the output string.

## 4. Randomization

Since there are `2^n` possible strings but only `n` are in the input, randomly generating a string has a high probability of being unique. For small `n`, this probability is at least `(2^n - n) / 2^n`, which approaches 1 quickly. We keep generating random strings until we find one not in the set.

```cpp
class Solution {
public:
    string findDifferentBinaryString(vector<string>& nums) {
        unordered_set<string> strSet(nums.begin(), nums.end());
        int n = nums.size();

        while (true) {
            string res = "";
            for (int i = 0; i < n; i++) {
                res += (rand() % 2) ? '1' : '0';
            }
            if (strSet.find(res) == strSet.end()) {
                return res;
            }
        }
    }
};
```

**Complexity**

- Time complexity: $O(∞)$ in worst case.
- Space complexity: $O(n)$

## 5. Trie

A Trie (prefix tree) stores all input strings and allows us to find a missing string by traversing the tree. At each node, if one of the two children (0 or 1) is missing, we can take that path and fill the rest arbitrarily. This finds a missing string in O(n) time after O(n^2) preprocessing.

```cpp
class Node {
public:
    Node *children[2];

    Node() {
        this->children[0] = nullptr;
        this->children[1] = nullptr;
    }

    bool containsBit(int bit) {
        return this->children[bit] != nullptr;
    }

    void put(int bit) {
        this->children[bit] = new Node();
    }

    Node* get(int bit) {
        return this->children[bit];
    }
};

class Trie {
public:
    Node* root;

    Trie() {
        this->root = new Node();
    }

    void insert(const string& s) {
        Node* curr = root;
        for (char c : s) {
            int bit = c - '0';
            if (!curr->containsBit(bit)) {
                curr->put(bit);
            }
            curr = curr->get(bit);
        }
    }

    bool search(string& res, Node* curr) {
        while (curr->containsBit(0) || curr->containsBit(1)) {
            if (!curr->containsBit(0)) {
                res += '0';
                return true;
            }
            if (!curr->containsBit(1)) {
                res += '1';
                return true;
            }

            res += '1';
            curr = curr->get(1);
        }

        return false;
    }
};

class Solution {
public:
    string findDifferentBinaryString(vector<string>& nums) {
        Trie trie;
        for (const string& s : nums) {
            trie.insert(s);
        }

        string res;
        trie.search(res, trie.root);

        while (res.length() < nums.size()) {
            res += '1';
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n ^ 2)$

## Standalone solution file (`cpp/1980-find-unique-binary-string.cpp` in the NeetCode repo)

```cpp
/*
    This class implements a solution to find a binary string that differs from a given list of binary strings.
    
    Approach:
    1. Define a backtrack function to explore all possible binary strings of the same length as the input strings.
    2. Use a set to store the input strings to efficiently check for duplicates.
    3. Backtrack through all possible binary strings of length equal to the input strings.
    4. If a binary string is found that does not exist in the set of input strings, update the result and return.
    
    Variables:
    - result: Holds the result, initialized to an empty string.
    - backtrack(): Recursive function to generate binary strings and check for uniqueness.
    - inputStrings: Input vector of binary strings.
    - currentString: Current binary string being constructed during backtracking.
    - stringLength: Length of binary strings in the input.
    - stringSet: Set to store input binary strings for fast duplicate checking.

    Time Complexity: O(2^N * N), where N is the length of the binary strings.
        - The function 'backtrack' explores all possible binary strings of length N, which is O(2^N).
        - Checking for uniqueness in the set takes O(1) time on average.
    Space Complexity: O(2^N * N) considering the space required to store the generated binary strings during backtracking.
*/

class Solution {
public:
    string result = "";
    
    void backtrack(vector<string>& inputStrings, string& currentString, int stringLength, set<string>& stringSet) {
        if (!result.empty()) return;
        if (currentString.size() == stringLength && stringSet.find(currentString) == stringSet.end()) {
            result = currentString;
            return;
        }
        if (currentString.size() > stringLength) return;

        for (char ch = '0'; ch <= '1'; ++ch) {
            currentString.push_back(ch);
            backtrack(inputStrings, currentString, stringLength, stringSet);
            currentString.pop_back();
        }
    }
    
    string findDifferentBinaryString(vector<string>& inputStrings) {
        int stringLength = inputStrings[0].size();
        string currentString = "";
        set<string> stringSet(inputStrings.begin(), inputStrings.end());

        backtrack(inputStrings, currentString, stringLength, stringSet);
        return result;
    }
};
```
