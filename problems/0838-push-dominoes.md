# 838. Push Dominoes

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/push-dominoes/>  
- **NeetCode:** <https://neetcode.io/problems/push-dominoes>  
- **Video:** <https://www.youtube.com/watch?v=evUFsOb_iLY>  

[← Back to index](../INDEX.md)

## 1. Brute Force

For each standing domino (represented by `'.'`), we need to determine which force, if any, will knock it over. We look for the nearest `'R'` to the left and the nearest `'L'` to the right. If only one force reaches this domino, it falls in that direction. If both forces reach it, the closer one wins. If they are equidistant, the forces cancel out and the domino stays upright.

```cpp
class Solution {
public:
    string pushDominoes(string dominoes) {
        int n = dominoes.size();
        vector<char> res(dominoes.begin(), dominoes.end());

        for (int i = 0; i < n; i++) {
            if (dominoes[i] != '.') continue;

            int l = i - 1, r = i + 1;

            while (l >= 0 && dominoes[l] == '.') l--;
            while (r < n && dominoes[r] == '.') r++;

            char leftForce = (l >= 0) ? dominoes[l] : ' ';
            char rightForce = (r < n) ? dominoes[r] : ' ';

            if (leftForce == 'R' && rightForce == 'L') {
                if ((i - l) < (r - i)) res[i] = 'R';
                else if ((r - i) < (i - l)) res[i] = 'L';
            } else if (leftForce == 'R') {
                res[i] = 'R';
            } else if (rightForce == 'L') {
                res[i] = 'L';
            }
        }

        return string(res.begin(), res.end());
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$ for only the output string.

## 2. Force From Left & Right

Instead of checking neighbors for each domino individually, we can precompute how far each position is from the nearest pushing force. We make two passes: one from left to right tracking distance from the last 'R', and one from right to left tracking distance from the last 'L'. At each position, we compare these distances to determine which force dominates.

```cpp
class Solution {
public:
    string pushDominoes(string dominoes) {
        int n = dominoes.size();
        vector<int> left(n, INT_MAX);
        vector<int> right(n, INT_MAX);
        vector<char> res(dominoes.begin(), dominoes.end());

        int force = INT_MAX;
        for (int i = 0; i < n; i++) {
            if (dominoes[i] == 'R') {
                force = 0;
            } else if (dominoes[i] == 'L') {
                force = INT_MAX;
            } else {
                force = (force == INT_MAX) ? INT_MAX : force + 1;
            }
            right[i] = force;
        }

        force = INT_MAX;
        for (int i = n - 1; i >= 0; i--) {
            if (dominoes[i] == 'L') {
                force = 0;
            } else if (dominoes[i] == 'R') {
                force = INT_MAX;
            } else {
                force = (force == INT_MAX) ? INT_MAX : force + 1;
            }
            left[i] = force;
        }

        for (int i = 0; i < n; i++) {
            if (left[i] < right[i]) {
                res[i] = 'L';
            } else if (right[i] < left[i]) {
                res[i] = 'R';
            }
        }

        return string(res.begin(), res.end());
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 3. Simulation (Queue)

We can simulate the dominoes falling in real time using a queue. Initially, all dominoes that are already pushed ('L' or 'R') are added to the queue. We process them one by one, pushing adjacent dominoes as they fall. The key insight is handling collisions: when 'R' meets 'L' with one standing domino between them, that domino stays upright.

```cpp
class Solution {
public:
    string pushDominoes(string dominoes) {
        vector<char> dom(dominoes.begin(), dominoes.end());
        queue<pair<int, char>> q;

        for (int i = 0; i < dom.size(); i++) {
            if (dom[i] != '.') {
                q.push({i, dom[i]});
            }
        }

        while (!q.empty()) {
            auto [i, d] = q.front();
            q.pop();

            if (d == 'L' && i > 0 && dom[i - 1] == '.') {
                q.push({i - 1, 'L'});
                dom[i - 1] = 'L';
            } else if (d == 'R') {
                if (i + 1 < dom.size() && dom[i + 1] == '.') {
                    if (i + 2 < dom.size() && dom[i + 2] == 'L') {
                        q.pop();
                    } else {
                        q.push({i + 1, 'R'});
                        dom[i + 1] = 'R';
                    }
                }
            }
        }

        return string(dom.begin(), dom.end());
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$

## 4. Iteration (Greedy)

We can process the string in one pass by tracking whether we've seen an 'R' that might affect upcoming dominoes. As we iterate, we count consecutive dots and decide their fate when we hit an 'L' or 'R'. The key cases are: dots between 'R' and 'L' split in half, dots after 'R' all fall right, and dots before 'L' (with no prior 'R') all fall left.

```cpp
class Solution {
public:
    string pushDominoes(string dominoes) {
        string res = "";
        int dots = 0;
        bool R = false;

        for (char d : dominoes) {
            if (d == '.') {
                dots++;
            } else if (d == 'R') {
                if (R) {
                    // Previous was 'R', and current is also 'R'.
                    // Append 'R' for all the dots between them.
                    res += string(dots + 1, 'R');
                } else if (dots > 0) {
                    // Previous was not 'R'. The previous dots remain unchanged.
                    res += string(dots, '.');
                }
                dots = 0;
                R = true; // Current is 'R'.
            } else {
                if (R) {
                    // Append the previous 'R'.
                    res += 'R';
                    if (dots > 0) {
                        // Half the dots are affected by the previous 'R'.
                        res += string(dots / 2, 'R');

                        // Add a '.' if there's an odd number of dots.
                        if (dots % 2 != 0) {
                            res += '.';
                        }

                        // Append half the dots as 'L'.
                        res += string(dots / 2, 'L');
                    }
                    // Append the current 'L'.
                    res += 'L';
                    R = false;
                    dots = 0;
                } else {
                    // There is no 'R' on the left.
                    // Append 'L' for all the dots and the current 'L'.
                    res += string(dots + 1, 'L');
                    dots = 0;
                }
            }
        }

        if (R) {
            // Trailing dots are affected by the last 'R'.
            res += string(dots + 1, 'R');
        } else {
            // Trailing dots remain unchanged as there is no previous 'R'.
            res += string(dots, '.');
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(n)$ for only the output string.

## Standalone solution file (`cpp/0838-push-dominoes.cpp` in the NeetCode repo)

```cpp
/*
    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    string pushDominoes(string dominoes) {
        
        string res = "";
        char prev;
        int n = dominoes.size(), count = 1;
        
        vector<int> left(n, 0), right(n, 0);
        for (int i = 0; i < n; i++) {
            if (dominoes[i] == 'R') { count = 1; prev = 'R'; }
            else if (dominoes[i] != '.')    prev = dominoes[i];
            if (prev == 'R' && dominoes[i] == '.')   right[i] = count++;
        }
        
        prev = '.';
        for (int i = n-1; i >= 0; i--) {
            if (dominoes[i] == 'L') { count = 1; prev = 'L'; }
            else if (dominoes[i] != '.')    prev = dominoes[i];
            if (prev == 'L' && dominoes[i] == '.')   left[i] = count++;
        }
        
        for (int i = 0; i < n; i++) {
            if (!left[i] && !right[i]) res += dominoes[i];
            else if (!left[i]) res += 'R';
            else if (!right[i]) res += 'L';
            else if (left[i] == right[i]) res += '.';
            else if (left[i] < right[i]) res += 'L';
            else res += 'R';
        }
        
        return res;
    }
};
```
