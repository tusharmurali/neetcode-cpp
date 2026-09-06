# 1189. Maximum Number of Balloons

- **Difficulty:** Easy  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/maximum-number-of-balloons/>  
- **NeetCode:** <https://neetcode.io/problems/maximum-number-of-balloons>  
- **Video:** <https://www.youtube.com/watch?v=G9xeB2-7PqY>  
- **Video approach:** 1. Hash Map - I (auto-matched)  

[← Back to index](../INDEX.md)

## 1. Hash Map - I ▶ video

To form the word "balloon", we need specific counts of each letter: one each of 'b', 'a', 'n', and two each of 'l' and 'o'. The number of times we can spell "balloon" is limited by whichever required letter runs out first. By counting all letters in the text and then dividing by the required amounts, we find how many complete words we can form.

```cpp
class Solution {
public:
    int maxNumberOfBalloons(string text) {
        unordered_map<char, int> countText;
        for (char c : text) {
            countText[c]++;
        }

        unordered_map<char, int> balloon = {{'b', 1}, {'a', 1},
                                            {'l', 2}, {'o', 2}, {'n', 1}};

        int res = text.length();
        for (auto& entry : balloon) {
            res = min(res, countText[entry.first] / entry.second);
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since we have at most $26$ different characters.

## 2. Hash Map - II

We can optimize by only counting the five relevant characters ('b', 'a', 'l', 'o', 'n') instead of all 26 letters. After counting, we adjust for 'l' and 'o' by dividing their counts by 2 since each "balloon" requires two of each. The minimum count then gives our answer directly.

```cpp
class Solution {
public:
    int maxNumberOfBalloons(string text) {
        unordered_map<char, int> mp;
        for (char c : text) {
            if (string("balon").find(c) != string::npos) {
                mp[c]++;
            }
        }

        if (mp.size() < 5) {
            return 0;
        }

        mp['l'] /= 2;
        mp['o'] /= 2;
        return min({mp['b'], mp['a'], mp['l'], mp['o'], mp['n']});
    }
};
```

**Complexity**

- Time complexity: $O(n)$
- Space complexity: $O(1)$ since $balloon$ has $5$ different characters.

## Standalone solution file (`cpp/1189-maximum-number-of-balloons.cpp` in the NeetCode repo)

```cpp
class Solution {
public:
    int maxNumberOfBalloons(string text) {
        map<char, int> countText;
        map<char, int> balloon;
        for(char c: text)
            countText[c]++;
        for(char c: std::string("balloon"))
            balloon[c]++;
        
        int res = text.length();
        for(const auto &[key, value]: balloon)
            res = min(res, countText[key] / value);
        return res;
    }
};
```
