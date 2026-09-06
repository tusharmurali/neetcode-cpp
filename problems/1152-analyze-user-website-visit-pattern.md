# 1152. Analyze User Website Visit Pattern

- **Difficulty:** Medium  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/analyze-user-website-visit-pattern/>  
- **NeetCode:** <https://neetcode.io/problems/analyze-user-website-visit-pattern>  

[← Back to index](../INDEX.md)

## 1. Hash Map

We need to find the most common 3-website pattern visited by users in sequential order. The key insight is that we should group each user's website visits in chronological order, then generate all possible 3-site combinations for each user. By counting how many distinct users visit each pattern, we can find the most popular one.

Since we want patterns across different users (not repeated visits by the same user), we use a `set` for each user's patterns before counting. This ensures each user contributes at most once to each pattern's `count`.

```cpp
class Solution {
public:
    vector<string> mostVisitedPattern(vector<string>& username, vector<int>& timestamp, vector<string>& website) {
        int n = timestamp.size();
        vector<pair<int,int>> arr;
        for (int i = 0; i < n; ++i) arr.push_back({timestamp[i], i});
        sort(arr.begin(), arr.end(),
             [](auto& a, auto& b){ return a.first < b.first; });

        unordered_map<string, vector<string>> mp;
        for (auto& p : arr) mp[username[p.second]].push_back(website[p.second]);

        unordered_map<string,int> count;
        for (auto& kv : mp) {
            auto& cur = kv.second;
            unordered_set<string> patterns;
            for (int i = 0; i < (int)cur.size(); ++i)
                for (int j = i + 1; j < (int)cur.size(); ++j)
                    for (int k = j + 1; k < (int)cur.size(); ++k)
                        patterns.insert(cur[i] + "#" + cur[j] + "#" + cur[k]);
            for (auto& p : patterns) ++count[p];
        }

        int maxCnt = 0;
        string res;
        for (auto& kv : count)
            if (kv.second > maxCnt ||
               (kv.second == maxCnt && (res.empty() || kv.first < res))) {
                maxCnt = kv.second;
                res = kv.first;
            }

        vector<string> ans;
        string tmp;
        for (char ch : res) {
            if (ch == '#') {
                ans.push_back(tmp);
                tmp.clear();
            } else {
                tmp += ch;
            }
        }
        ans.push_back(tmp);
        return ans;
    }
};
```

**Complexity**

- Time complexity: $O(n \log n + n * u +  n ^ 3 * w)$
- Space complexity: $O(n * u + n ^ 3 * w)$

> Where $n$ is the size of the array $timestamp$, $u$ is the maximum length of any string in the array $username$, and $w$ is the maximum length of any string in the array $website$.
