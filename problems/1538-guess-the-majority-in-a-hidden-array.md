# 1538. Guess the Majority in a Hidden Array

- **Difficulty:** Medium  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/guess-the-majority-in-a-hidden-array/>  
- **NeetCode:** <https://neetcode.io/problems/guess-the-majority-in-a-hidden-array>  

[← Back to index](../INDEX.md)

## 1. n Queries

We cannot access array elements directly, only through queries that return the count of identical elements among four indices. The key observation is that comparing two queries that differ by exactly one index tells us whether that differing element matches the rest.

If `query(0, 1, 2, 3)` equals `query(1, 2, 3, 4)`, then indices `0` and `4` must have the same value (since replacing one with the other kept the count unchanged). Using this principle, we can determine which elements match index `0` and which differ, without knowing the actual values.

```cpp
class Solution {
    int cntEqual = 1, cntDiffer = 0, indexDiffer = -1;

public:
    int guessMajority(ArrayReader& reader) {
        int n = reader.length(), query0123 = reader.query(0, 1, 2, 3), query1234 = reader.query(1, 2, 3, 4);

        function<void(bool, int)> f = [this](bool equal, int i) {
            if (equal) {
                cntEqual++;
            } else {
                cntDiffer++;
                indexDiffer = i;
            }
        };

        f(query1234 == query0123, 4);

        for (int i = 5; i < n; i++) {
            f(reader.query(1, 2, 3, i) == query0123, i);
        }

        f(reader.query(0, 2, 3, 4) == query1234, 1);
        f(reader.query(0, 1, 3, 4) == query1234, 2);
        f(reader.query(0, 1, 2, 4) == query1234, 3);

        return cntEqual > cntDiffer ? 0 : cntDiffer > cntEqual ? indexDiffer : -1;
    }
};
```

**Complexity**

- Time complexity: $O(n)$

- Space complexity: $O(1)$

> Where $n$ is the number of queries.
