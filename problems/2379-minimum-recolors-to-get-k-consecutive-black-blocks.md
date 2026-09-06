# 2379. Minimum Recolors to Get K Consecutive Black Blocks

- **Difficulty:** Easy  
- **Pattern:** Sliding Window  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/minimum-recolors-to-get-k-consecutive-black-blocks/>  
- **NeetCode:** <https://neetcode.io/problems/minimum-recolors-to-get-k-consecutive-black-blocks>  
- **Video:** <https://www.youtube.com/watch?v=cWz4_zUegxE>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We need to find a window of `k` consecutive blocks that requires the fewest recolors to become all black. A recolor is needed for each white block ('W') in the window. We can check every possible window of size `k` and count the white blocks in each, keeping track of the minimum count.

```cpp
class Solution {
public:
    int minimumRecolors(string blocks, int k) {
        int res = blocks.length();
        for (int i = 0; i <= blocks.length() - k; i++) {
            int count_w = 0;
            for (int j = i; j < i + k; j++) {
                if (blocks[j] == 'W') {
                    count_w++;
                }
            }
            res = min(res, count_w);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * k)$
- Space complexity: $O(1)$

## 2. Sliding Window

When sliding the window one position to the right, most of the count stays the same. We only need to subtract the contribution of the element leaving the window and add the contribution of the new element entering. This avoids recounting the entire window each time, reducing time from O(n\*k) to O(n).

```cpp
class Solution {
public:
    int minimumRecolors(string blocks, int k) {
        int count_w = 0;
        for (int i = 0; i < k; i++) {
            if (blocks[i] == 'W') {
                count_w++;
            }
        }

        int res = count_w;
        for (int i = k; i < blocks.size(); i++) {
            if (blocks[i - k] == 'W') {
                count_w--;
            }
            if (blocks[i] == 'W') {
                count_w++;
            }
            res = min(res, count_w);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$
