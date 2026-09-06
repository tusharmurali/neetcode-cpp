# 2125. Number of Laser Beams in a Bank

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/number-of-laser-beams-in-a-bank/>  
- **NeetCode:** <https://neetcode.io/problems/number-of-laser-beams-in-a-bank>  
- **Video:** <https://www.youtube.com/watch?v=KLeKv59LAFY>  

[← Back to index](../INDEX.md)

## 1. Counting

Laser beams only form between adjacent rows that contain at least one security device. If one row has `a` devices and the next non-empty row has `b` devices, they form `a * b` beams. We track the count from the previous non-empty row and multiply it by the current row's `count` whenever we encounter a new row with devices.

```cpp
class Solution {
public:
    int numberOfBeams(vector<string>& bank) {
        int prev = countOnes(bank[0]);
        int res = 0;

        for (int i = 1; i < bank.size(); i++) {
            int curr = countOnes(bank[i]);
            if (curr > 0) {
                res += prev * curr;
                prev = curr;
            }
        }

        return res;
    }

private:
    int countOnes(const string& s) {
        return count(s.begin(), s.end(), '1');
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(1)$ extra space.

> Where $m$ is the number of rows and $n$ is the number of columns.
