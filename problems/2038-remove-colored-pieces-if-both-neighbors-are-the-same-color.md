# 2038. Remove Colored Pieces if Both Neighbors are the Same Color

- **Difficulty:** Medium  
- **Pattern:** Greedy  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/remove-colored-pieces-if-both-neighbors-are-the-same-color/>  
- **NeetCode:** <https://neetcode.io/problems/remove-colored-pieces-if-both-neighbors-are-the-same-color>  
- **Video:** <https://www.youtube.com/watch?v=T54GScWobZ4>  

[← Back to index](../INDEX.md)

## 1. Brute Force

We simulate the game turn by turn. Alice looks for a piece 'A' surrounded by two other 'A's and removes it. Then Bob does the same for 'B'. If a player cannot make a move on their turn, they lose. This straightforward simulation mirrors the actual gameplay but is slow because we repeatedly scan and modify the string.

```cpp
class Solution {
public:
    bool winnerOfGame(string colors) {
        while (true) {
            if (!removeChar(colors, 'A')) return false;
            if (!removeChar(colors, 'B')) return true;
        }
    }

private:
    bool removeChar(string& s, char c) {
        for (int i = 1; i < s.size() - 1; i++) {
            if (s[i] != c) continue;

            if (s[i - 1] == c && s[i + 1] == c) {
                s.erase(i, 1);
                return true;
            }
        }
        return false;
    }
};
```

**Complexity**

- Time complexity: $O(n ^ 2)$
- Space complexity: $O(n)$

## 2. Greedy + Two Pointers

The key insight is that each player's moves are independent. Removing an 'A' from a sequence of A's doesn't affect Bob's sequences of B's, and vice versa. So instead of simulating the game, we can count how many moves each player has available. For a run of consecutive same-colored pieces of length `k`, a player can remove `k - 2` pieces (since they need neighbors on both sides). Alice wins if she has more moves than Bob.

```cpp
class Solution {
public:
    bool winnerOfGame(string colors) {
        int alice = 0, bob = 0, l = 0;

        for (int r = 0; r < colors.size(); r++) {
            if (colors[l] != colors[r]) {
                l = r;
            }

            int extra = r - l - 1;
            if (extra > 0) {
                if (colors[l] == 'A') {
                    alice++;
                } else {
                    bob++;
                }
            }
        }

        return alice > bob;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.

## 3. Greedy

This is a cleaner way to count available moves. For each position in the middle of the string, we check if it forms a "triplet" of same-colored pieces. Each such triplet represents one potential move for that player. Since removing a piece from a longer run still leaves valid triplets, we simply count all triplet centers for each player.

```cpp
class Solution {
public:
    bool winnerOfGame(string colors) {
        int alice = 0, bob = 0;

        for (int i = 1; i < colors.size() - 1; i++) {
            if (colors[i - 1] == colors[i] && colors[i] == colors[i + 1]) {
                if (colors[i] == 'A') {
                    alice++;
                }
                if (colors[i] == 'B') {
                    bob++;
                }
            }
        }

        return alice > bob;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ extra space.
