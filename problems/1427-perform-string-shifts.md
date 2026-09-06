# 1427. Perform String Shifts

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/perform-string-shifts/>  
- **NeetCode:** <https://neetcode.io/problems/perform-string-shifts>  

[← Back to index](../INDEX.md)

## 1. Simulation

A left shift moves characters from the front to the back, while a right shift moves characters from the back to the front. We can simulate each shift operation directly by slicing the string. Taking modulo of the shift amount by the string length handles cases where the shift exceeds the string size, since shifting by the full length returns the original string.

```cpp
class Solution {
public:
    string stringShift(string s, vector<vector<int>>& shift) {
        int len = s.length();

        for (auto move : shift) {
            int direction = move[0];
            int amount = move[1] % len;
            if (direction == 0) {
                // Move necessary amount of characters from start to end
                s = s.substr(amount) + s.substr(0, amount);
            } else {
                // Move necessary amount of characters from end to start
                s = s.substr(len - amount) +
                    s.substr(0, len - amount);
            }
        }
        return s;
    }
};
```

**Complexity**

- Time complexity: $O(N * L)$
- Space complexity: $O(L)$ extra space used

> Where $L$ is the length of the string and $N$ is the length of the `shift` array

## 2. Compute Net Shift

Instead of performing each shift individually, we can compute the net effect of all shifts. Left and right shifts cancel each other out, so we sum all left shifts as positive and all right shifts as negative (or vice versa). The final net shift tells us how much to rotate the string in one direction, avoiding redundant operations.

```cpp
class Solution {
public:
    string stringShift(string s, vector<vector<int>>& shift) {
        // Count the number of left shifts. A right shift is a negative left shift.
        int leftShifts = 0;

        for (auto& move : shift) {
            if (move[0] == 1) {
                move[1] = -move[1];
            }
            leftShifts += move[1];
        }

        // Convert back to a positive, do left shifts, and return.
        int n = s.length();
        leftShifts = ((leftShifts % n) + n) % n;
        s = s.substr(leftShifts) + s.substr(0, leftShifts);
        return s;
    }
};
```

**Complexity**

- Time complexity: $O(N + L)$
- Space complexity: $O(L)$ extra space used

> Where $L$ is the length of the string and $N$ is the length of the `shift` array
