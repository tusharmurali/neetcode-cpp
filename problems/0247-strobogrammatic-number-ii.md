# 247. Strobogrammatic Number II

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/strobogrammatic-number-ii/>  
- **NeetCode:** <https://neetcode.io/problems/strobogrammatic-number-ii>  

[← Back to index](../INDEX.md)

## 1. Recursion

A strobogrammatic number looks the same when rotated 180 degrees. Only certain digit pairs maintain their appearance after rotation: (0,0), (1,1), (6,9), (8,8), and (9,6). We can build these numbers recursively from the inside out. Start with the base cases: empty string for even length or single symmetric digits (0, 1, 8) for odd length. Then wrap each smaller solution with valid digit pairs. The key insight is that leading zeros are invalid, so we skip adding '0' at the outermost layer.

```cpp
class Solution {
public:
    vector<vector<char>> reversiblePairs = {
        {'0', '0'}, {'1', '1'},
        {'6', '9'}, {'8', '8'}, {'9', '6'}
    };

    vector<string> generateStroboNumbers(int n, int finalLength) {
        if (n == 0) {
            // 0-digit strobogrammatic number is an empty string.
            return { "" };
        }

        if (n == 1) {
            // 1-digit strobogrammatic numbers.
            return { "0", "1", "8" };
        }

        vector<string> prevStroboNums = generateStroboNumbers(n - 2, finalLength);
        vector<string> currStroboNums;

        for (string& prevStroboNum : prevStroboNums) {
            for (vector<char>& pair : reversiblePairs) {
                // We can only append 0's if it is not first digit.
                if (pair[0] != '0' || n != finalLength) {
                    currStroboNums.push_back(pair[0] + prevStroboNum + pair[1]);
                }
            }
        }

        return currStroboNums;
    }

    vector<string> findStrobogrammatic(int n) {
        return generateStroboNumbers(n, n);
    }
};
```

**Complexity**

- Time complexity: $O(N \cdot 5^{\lfloor N/2 \rfloor + 1})$

- Space complexity: $O(N \cdot 5^{\lfloor N/2 \rfloor})$

> Where $N$ is the length of strobogrammatic numbers we need to find.

## 2. Iteration (Level Order Traversal)

Instead of recursion, we can build strobogrammatic numbers iteratively using a BFS-like approach. Start from the center and expand outward level by level. For odd-length numbers, begin with single digits (0, 1, 8). For even-length numbers, begin with an empty string. Each iteration adds two digits to the current strings, growing them symmetrically until we reach the target length.

```cpp
class Solution {
public:
    vector<vector<char>> reversiblePairs = {
        {'0', '0'}, {'1', '1'},
        {'6', '9'}, {'8', '8'}, {'9', '6'}
    };

    vector<string> findStrobogrammatic(int n) {
        queue<string> q;
        int currStringsLength;

        // When n is even, it means when decreasing by 2 we will go till 0.
        if (n % 2 == 0) {
            // We will start with 0-digit strobogrammatic numbers.
            currStringsLength = 0;
            q.push("");
        } else {
            // We will start with 1-digit strobogrammatic numbers.
            currStringsLength = 1;
            q.push("0");
            q.push("1");
            q.push("8");
        }

        while (currStringsLength < n) {
            currStringsLength += 2;
            for (int i = q.size(); i > 0; --i) {
                string number = q.front();
                q.pop();

                for (vector<char>& pair : reversiblePairs) {
                    if (currStringsLength != n || pair[0] != '0') {
                        q.push(pair[0] + number + pair[1]);
                    }
                }
            }
        }

        vector<string> stroboNums;
        while (!q.empty()) {
            stroboNums.push_back(q.front());
            q.pop();
        }

        return stroboNums;
    }
};
```

**Complexity**

- Time complexity: $O(N \cdot 5^{\lfloor N/2 \rfloor + 1})$

- Space complexity: $O(N \cdot 5^{\lfloor N/2 \rfloor})$
    - Note: In javascript and python, in the last iteration the arrary, is the output array. Thus it will not be considered in auxiliary space. But still, the overall order of the complexity remains the same.

> Where $N$ is the length of strobogrammatic numbers we need to find.
