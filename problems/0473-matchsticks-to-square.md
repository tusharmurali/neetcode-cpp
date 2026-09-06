# 473. Matchsticks to Square

- **Difficulty:** Medium  
- **Pattern:** Backtracking  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/matchsticks-to-square/>  
- **NeetCode:** <https://neetcode.io/problems/matchsticks-to-square>  
- **Video:** <https://www.youtube.com/watch?v=hUe0cUKV-YY>  
- **Video approach:** 2. Backtracking (Pruning)  

[← Back to index](../INDEX.md)

## 1. Backtracking (Brute Force)

To form a square, we need to partition matchsticks into `4` groups with equal sums. Each matchstick must be assigned to exactly one side. We try placing each matchstick on each of the `4` sides recursively. If we successfully place all matchsticks and all `4` sides have equal length, we found a valid square.

```cpp
class Solution {
public:
    bool makesquare(vector<int>& matchsticks) {
        int sum = accumulate(matchsticks.begin(), matchsticks.end(), 0);
        if (sum % 4 != 0) return false;

        vector<int> sides(4, 0);
        return dfs(matchsticks, sides, 0);
    }

private:
    bool dfs(vector<int>& matchsticks, vector<int>& sides, int i) {
        if (i == matchsticks.size()) {
            return sides[0] == sides[1] && sides[1] == sides[2] && sides[2] == sides[3];
        }

        for (int j = 0; j < 4; j++) {
            sides[j] += matchsticks[i];
            if (dfs(matchsticks, sides, i + 1)) return true;
            sides[j] -= matchsticks[i];
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(4 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 2. Backtracking (Pruning) ▶ video

The brute force approach explores many redundant paths. We can prune significantly with two optimizations. First, sort matchsticks in descending order so larger sticks are placed first, failing faster when a configuration is impossible. Second, skip trying to place a matchstick on an empty side if we already tried another empty side, since empty sides are interchangeable.

```cpp
class Solution {
public:
    bool makesquare(vector<int>& matchsticks) {
        int totalLength = accumulate(matchsticks.begin(), matchsticks.end(), 0);
        if (totalLength % 4 != 0) return false;

        int length = totalLength / 4;
        vector<int> sides(4, 0);
        sort(matchsticks.rbegin(), matchsticks.rend());

        return dfs(matchsticks, sides, 0, length);
    }

private:
    bool dfs(vector<int>& matchsticks, vector<int>& sides, int index, int length) {
        if (index == matchsticks.size()) {
            return true;
        }

        for (int i = 0; i < 4; i++) {
            if (sides[i] + matchsticks[index] <= length) {
                sides[i] += matchsticks[index];
                if (dfs(matchsticks, sides, index + 1, length)) return true;
                sides[i] -= matchsticks[index];
            }

            if (sides[i] == 0) break;
        }

        return false;
    }
};
```

**Complexity**

- Time complexity: $O(4 ^ n)$
- Space complexity: $O(n)$ for recursion stack.

## 3. Dynamic Programming (Bit Mask)

We can represent which matchsticks have been used with a bitmask. For each subset of matchsticks, we track the current "partial side" length (sum modulo target side length). If we can use all matchsticks such that each completed side reaches exactly the target length, we have a valid square. Memoization avoids recomputing results for the same subset.

```cpp
class Solution {
    vector<int> dp;
    int length, n;

public:
    bool makesquare(vector<int>& matchsticks) {
        int totalLength = accumulate(matchsticks.begin(), matchsticks.end(), 0);
        if (totalLength % 4 != 0) return false;

        length = totalLength / 4;
        if (*max_element(matchsticks.begin(), matchsticks.end()) > length) {
            return false;
        }

        sort(matchsticks.rbegin(), matchsticks.rend());
        n = matchsticks.size();
        dp.resize(1 << n, INT_MIN);

        return dfs((1 << n) - 1, matchsticks) == 0;
    }

private:
    int dfs(int mask, vector<int>& matchsticks) {
        if (mask == 0) return 0;
        if (dp[mask] != INT_MIN) return dp[mask];

        for (int i = 0; i < n; i++) {
            if (mask & (1 << i)) {
                int res = dfs(mask ^ (1 << i), matchsticks);
                if (res >= 0 && res + matchsticks[i] <= length) {
                    dp[mask] = (res + matchsticks[i]) % length;
                    return dp[mask];
                }

                if (mask == (1 << n) - 1) {
                    dp[mask] = -1;
                    return -1;
                }
            }
        }

        dp[mask] = -1;
        return dp[mask];
    }
};
```

**Complexity**

- Time complexity: $O(n * 2 ^ n)$
- Space complexity: $O(n + 2 ^ n)$

## Standalone solution file (`cpp/0473-matchsticks-to-square.cpp` in the NeetCode repo)

```cpp
class Solution {
    int a,b,c,d;
    bool fun(vector<int>& matchsticks,int i){
        if(i==matchsticks.size()){
            if(a==0 && b==0 && c==0 && d==0) return true;
            else return false;
        }
        
        if(matchsticks[i]<=a){
            a-=matchsticks[i];
            if(fun(matchsticks,i+1)) return true;
            a+=matchsticks[i];
        }
        
        if(matchsticks[i]<=b){
            b-=matchsticks[i];
            if(fun(matchsticks,i+1)) return true;
            b+=matchsticks[i];
        }
        
        if(matchsticks[i]<=c){
            c-=matchsticks[i];
            if(fun(matchsticks,i+1)) return true;
            c+=matchsticks[i];
        }
        
        if(matchsticks[i]<=d){
            d-=matchsticks[i];
            if(fun(matchsticks,i+1)) return true;
            d+=matchsticks[i];
        }
		
        return false;
    }
public:
    bool makesquare(vector<int>& matchsticks) {
        if(matchsticks.size()<4) return false;
		int sum = accumulate(matchsticks.begin(), matchsticks.end(),0);
        if(sum % 4 != 0) return false;
		int sizeSum=sum/4;
        a=sizeSum,b=sizeSum,c=sizeSum,d=sizeSum;
		sort(matchsticks.rbegin(), matchsticks.rend());
		return fun(matchsticks,0);
    }
};
```
