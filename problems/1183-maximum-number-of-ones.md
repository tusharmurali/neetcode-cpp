# 1183. Maximum Number of Ones

- **Difficulty:** Hard  
- **Pattern:** Math & Geometry  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-number-of-ones/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-number-of-ones>  

[← Back to index](../INDEX.md)

## 1. Greedy

The key observation is that the matrix can be viewed as a tiling of `sideLength x sideLength` squares. Each position within this square pattern repeats throughout the entire matrix. If we place a `1` at position `(r, c)` within the pattern, it appears at all positions that map to `(r, c)` when tiled across the matrix.

To maximize the total number of ones, we should place our `maxOnes` ones at the positions within the pattern that appear most frequently in the full matrix. Positions near the top-left corner of the pattern tile more times because the matrix dimensions may not divide evenly by `sideLength`.

For each position `(r, c)` in the pattern, we calculate how many times it appears in the full matrix. Then we greedily pick the `maxOnes` positions with the highest counts.

```cpp
class Solution {
public:
    int maximumNumberOfOnes(int width, int height, int sideLength, int maxOnes) {
        vector<int> count;

        for (int r = 0; r < sideLength; ++r) {
            for (int c = 0; c < sideLength; ++c) {
                count.push_back((1 + (width - 1 - c) / sideLength) *
                                (1 + (height - 1 - r) / sideLength));
            }
        }

        sort(count.begin(), count.end(), greater<int>());

        int answer = 0;
        for (int i = 0; i < maxOnes; ++i) {
            answer += count[i];
        }

        return answer;
    }
};
```

**Complexity**

- Time complexity: $O(sideLength^2 \cdot \log sideLength^2)$

- Space complexity: $O(sideLength^2)$

## 2. Optimally Fill the Remainder Grids

Instead of computing and sorting all positions, we can directly calculate the answer by analyzing the structure of the tiled matrix. The matrix divides into regions based on how the `sideLength` pattern tiles:

- Full tiles that appear `(height / sideLength) * (width / sideLength)` times.
- Partial tiles along the right edge, bottom edge, and bottom-right corner.

Positions in the corner remainder region (bottom-right) appear the most frequently because they get counted in the main grid plus both edge strips plus the corner. We should fill these first, then the positions in the edge strips, prioritizing the edge with more repetitions.

```cpp
class Solution {
public:
    int maximumNumberOfOnes(int width, int height, int sideLength, int maxOnes) {
        int answer = maxOnes * ((height / sideLength) * (width / sideLength));
        int remain = maxOnes;

        int cnt1 = min((height % sideLength) * (width % sideLength), remain);
        answer += ((height / sideLength) + (width / sideLength) + 1) * cnt1;
        remain -= cnt1;

        if (height / sideLength > width / sideLength) {
            int cnt2 = min(((width % sideLength) * sideLength) - ((height % sideLength) * (width % sideLength)), remain);
            answer += (height / sideLength) * cnt2;
            remain -= cnt2;

            int cnt3 = min(((height % sideLength) * sideLength) - ((height % sideLength) * (width % sideLength)), remain);
            answer += (width / sideLength) * cnt3;
            remain -= cnt3;
        } else {
            int cnt2 = min(((height % sideLength) * sideLength) - ((height % sideLength) * (width % sideLength)), remain);
            answer += (width / sideLength) * cnt2;
            remain -= cnt2;

            int cnt3 = min(((width % sideLength) * sideLength) - ((height % sideLength) * (width % sideLength)), remain);
            answer += (height / sideLength) * cnt3;
            remain -= cnt3;
        }

        return answer;
    }
};
```

**Complexity**

- Time complexity: $O(1)$

- Space complexity: $O(1)$
