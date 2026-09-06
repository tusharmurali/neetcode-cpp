# 2300. Successful Pairs of Spells and Potions

- **Difficulty:** Medium  
- **Pattern:** Binary Search  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/successful-pairs-of-spells-and-potions/>  
- **NeetCode:** <https://neetcode.io/problems/successful-pairs-of-spells-and-potions>  
- **Video:** <https://www.youtube.com/watch?v=OKnm5oyAhWg>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each spell, we need to count how many potions form a successful pair. A pair is successful when `spell * potion >= success`. The simplest approach is to check every spell against every potion and count the valid combinations.

```cpp
class Solution {
public:
    vector<int> successfulPairs(vector<int>& spells, vector<int>& potions, long long success) {
        vector<int> res(spells.size());

        for (int i = 0; i < spells.size(); i++) {
            int cnt = 0;
            for (int p : potions) {
                if ((long long) spells[i] * p >= success) {
                    cnt++;
                }
            }
            res[i] = cnt;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(1)$

> The output array is not counted towards space complexity, as the [standard convention](https://en.wikipedia.org/wiki/DSPACE) measures only auxiliary working space.

> Where $n$ and $m$ are the sizes of the arrays $spells$ and $potions$ respectively.

## 2. Sorting + Binary Search

If we sort the potions array, all successful potions for a given spell will be contiguous at the end. For a spell `s`, we need the minimum potion strength `p` such that `s * p >= success`, which means `p >= success / s`. Binary search can efficiently find this threshold index, and all potions from that index onward form successful pairs.

```cpp
class Solution {
public:
    vector<int> successfulPairs(vector<int>& spells, vector<int>& potions, long long success) {
        sort(potions.begin(), potions.end());
        vector<int> res(spells.size());

        for (int i = 0; i < spells.size(); i++) {
            int l = 0, r = potions.size() - 1, idx = potions.size();

            while (l <= r) {
                int m = (l + r) / 2;
                if ((long long) spells[i] * potions[m] >= success) {
                    r = m - 1;
                    idx = m;
                } else {
                    l = m + 1;
                }
            }

            res[i] = potions.size() - idx;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O((m + n) * \log m)$
- Space complexity:
    - $O(1)$ or $O(m)$ extra space depending on the sorting algorithm.
    - $O(n)$ space for the output array.

> Where $n$ and $m$ are the sizes of the arrays $spells$ and $potions$ respectively.

## 3. Sorting + Two Pointers

If we sort both arrays, we can use the two pointer technique. A weaker spell needs a stronger potion to succeed, and a stronger spell needs at least as weak a potion. By processing spells in ascending order and potions in descending order, we can reuse the potion pointer position. Once a potion works for a spell, it works for all stronger spells too.

```cpp
class Solution {
public:
    vector<int> successfulPairs(vector<int>& spells, vector<int>& potions, long long success) {
        int n = spells.size(), m = potions.size();
        vector<int> S = spells;
        unordered_map<int, int> count;
        sort(spells.begin(), spells.end());
        sort(potions.begin(), potions.end());

        int j = m - 1;
        for (int i = 0; i < n; i++) {
            while (j >= 0 && (long long) spells[i] * potions[j] >= success) {
                j--;
            }
            count[spells[i]] = m - j - 1;
        }

        vector<int> res(n);
        for (int i = 0; i < n; i++) {
            res[i] = count[S[i]];
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n + m\log m)$
- Space complexity:
    - $O(1)$ or $O(m + n)$ extra space depending on the sorting algorithm.
    - $O(n)$ space for the output array.

> Where $n$ and $m$ are the sizes of the arrays $spells$ and $potions$ respectively.

## 4. Sorting + Two Pointers (Optimal)

The previous approach uses extra space to map spell values to their counts. We can avoid this by sorting indices of spells rather than the spells themselves. This way, we can directly write results to the correct positions in the output array without needing a lookup map.

```cpp
class Solution {
public:
    vector<int> successfulPairs(vector<int>& spells, vector<int>& potions, long long success) {
        int n = spells.size(), m = potions.size();
        vector<int> sIdx(n);
        for (int i = 0; i < n; i++) sIdx[i] = i;

        sort(sIdx.begin(), sIdx.end(), [&](int a, int b) {
            return spells[a] < spells[b];
        });

        sort(potions.begin(), potions.end());

        int j = m - 1;
        vector<int> res(n);
        for (int i = 0; i < n; i++) {
            while (j >= 0 && (long long) spells[sIdx[i]] * potions[j] >= success) {
                j--;
            }
            res[sIdx[i]] = m - j - 1;
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n + m\log m)$
- Space complexity:
    - $O(1)$ or $O(m + n)$ extra space depending on the sorting algorithm.
    - $O(n)$ space for the output array.

> Where $n$ and $m$ are the sizes of the arrays $spells$ and $potions$ respectively.

## Standalone solution file (`cpp/2300-successful-pairs-of-spells-and-potions.cpp` in the NeetCode repo)

```cpp
// Time: O(N * logN)
// Space: O(N)

class Solution {
public:
    vector<int> successfulPairs(vector<int>& spells, vector<int>& potions, long long success) {
        sort(potions.begin(), potions.end());

        int n = spells.size();
        int m = potions.size();
        vector<int> pairs(n);

        for(int i = 0; i < n; i++) {
            int spell = spells[i];

            int start = 0, end = m - 1;
            int curr;

            while(start <= end) {
                curr = start + (end-start)/2;
                long long strength = (long long)potions[curr] * (long long)spell;
                if(strength < success) {
                    start = curr + 1;
                }
                else {
                    end = curr - 1;
                }
            }
            pairs[i] = m - start;
        }

        return pairs;
    }
};
```
