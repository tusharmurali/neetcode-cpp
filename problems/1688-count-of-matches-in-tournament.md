# 1688. Count of Matches in Tournament

- **Difficulty:** Easy  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/count-of-matches-in-tournament/>  
- **NeetCode:** <https://neetcode.io/problems/count-of-matches-in-tournament>  
- **Video:** <https://www.youtube.com/watch?v=lslcc0tumpU>  

[← Back to index](../INDEX.md)

## 1. Simulation

We can simulate the tournament round by round. In each round, teams are paired up. If the number of teams is even, half play and half are eliminated. If odd, one team gets a bye and the rest pair up. We continue until only one team remains.

```cpp
class Solution {
public:
    int numberOfMatches(int n) {
        int res = 0;

        while (n > 1) {
            res += n / 2;
            n = (n + 1) / 2;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(\log n)$
- Space complexity: $O(1)$

## 2. Math

Every match eliminates exactly one team. To go from `n` teams to `1` winner, we need to eliminate `n - 1` teams. Therefore, exactly `n - 1` matches are played regardless of the tournament bracket structure.

```cpp
class Solution {
public:
    int numberOfMatches(int n) {
        return n - 1;
    }
};
```

**Complexity**

- Time complexity: $O(1)$
- Space complexity: $O(1)$
