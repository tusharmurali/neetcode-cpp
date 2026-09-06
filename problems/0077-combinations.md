# 77. Combinations

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/combinations/>  
- **NeetCode:** <https://neetcode.io/problems/combinations>  
- **Video:** <https://www.youtube.com/watch?v=q0s6m7AiM7o>  
- **Video approach:** 2. Backtracking - II  

[← Back to index](../INDEX.md)

## 1. Backtracking - I

To generate all combinations of `k` numbers from `1` to `n`, we make a binary choice for each number: include it or exclude it. This forms a decision tree where each path represents a subset. We only keep subsets of exactly size `k`.

```cpp
class Solution {
    vector<vector<int>> res;
public:
    vector<vector<int>> combine(int n, int k) {
        vector<int> comb;
        backtrack(1, n, k, comb);
        return res;
    }

private:
    void backtrack(int i, int n, int k, vector<int>& comb) {
        if (i > n) {
            if (comb.size() == k) {
                res.push_back(comb);
            }
            return;
        }

        comb.push_back(i);
        backtrack(i + 1, n, k, comb);
        comb.pop_back();
        backtrack(i + 1, n, k, comb);
    }
};
```

**Complexity**

- Time complexity: $O(k * \frac {n!}{(n - k)! * k!})$
- Space complexity: $O(k * \frac {n!}{(n - k)! * k!})$ for the output array.

> Where $n$ is the number of elements and $k$ is the number of elements to be picked.

## 2. Backtracking - II ▶ video

Instead of making include/exclude decisions, we iterate through available numbers and always include one. Starting from a given position ensures we never revisit smaller numbers, avoiding duplicates. We stop when the combination reaches size `k`.

```cpp
class Solution {
public:
    vector<vector<int>> res;

    vector<vector<int>> combine(int n, int k) {
        res.clear();
        vector<int> comb;
        backtrack(1, n, k, comb);
        return res;
    }

    void backtrack(int start, int n, int k, vector<int>& comb) {
        if (comb.size() == k) {
            res.push_back(comb);
            return;
        }

        for (int i = start; i <= n; i++) {
            comb.push_back(i);
            backtrack(i + 1, n, k, comb);
            comb.pop_back();
        }
    }
};
```

**Complexity**

- Time complexity: $O(k * \frac {n!}{(n - k)! * k!})$
- Space complexity: $O(k * \frac {n!}{(n - k)! * k!})$ for the output array.

> Where $n$ is the number of elements and $k$ is the number of elements to be picked.

## 3. Iteration

We can simulate backtracking iteratively using an array of size `k` to track our current combination. An index pointer moves forward when we find valid numbers and backward when we need to backtrack. This eliminates recursion overhead.

```cpp
class Solution {
public:
    vector<vector<int>> combine(int n, int k) {
        vector<vector<int>> res;
        vector<int> comb(k, 0);
        int i = 0;

        while (i >= 0) {
            comb[i]++;
            if (comb[i] > n) {
                i--;
                continue;
            }

            if (i == k - 1) {
                res.push_back(comb);
            } else {
                i++;
                comb[i] = comb[i - 1];
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(k * \frac {n!}{(n - k)! * k!})$
- Space complexity: $O(k * \frac {n!}{(n - k)! * k!})$ for the output array.

> Where $n$ is the number of elements and $k$ is the number of elements to be picked.

## 4. Bit Manipulation

Each subset of numbers from `1` to `n` can be represented as an `n`-bit binary number, where bit `i` being set means number `(i+1)` is included. We iterate through all possible bitmasks and keep only those with exactly `k` bits set.

```cpp
class Solution {
public:
    vector<vector<int>> combine(int n, int k) {
        vector<vector<int>> res;
        for (int mask = 0; mask < (1 << n); ++mask) {
            vector<int> comb;
            for (int bit = 0; bit < n; ++bit) {
                if (mask & (1 << bit)) {
                    comb.push_back(bit + 1);
                }
            }
            if (comb.size() == k) {
                res.push_back(comb);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity: $O(k * \frac {n!}{(n - k)! * k!})$ for the output array.

> Where $n$ is the number of elements and $k$ is the number of elements to be picked.

## Standalone solution file (`cpp/0077-combinations.cpp` in the NeetCode repo)

```cpp
class Solution {
private:
    void backtrack(int start, int n, int k, vector<int> &combination, vector<vector<int>> &res){
            //base case, when size of combination is k, we wanna stop
            if(combination.size() == k){
                res.push_back(combination);
                return;
            }

            for(int i = start; i<=n; i++){
                combination.push_back(i);
                backtrack(i+1, n, k, combination, res);
                combination.pop_back();
            }
        }
public:
    vector<vector<int>> combine(int n, int k) {
        vector<vector<int>> res;

        //initial empty list to pass to the backtrack function
        vector<int> emptyCombination;

        backtrack(1, n, k, emptyCombination, res);

        return res;
    }
};
```
