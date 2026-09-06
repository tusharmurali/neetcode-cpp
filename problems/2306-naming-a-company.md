# 2306. Naming a Company

- **Difficulty:** Hard  
- **Pattern:** Arrays & Hashing  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/naming-a-company/>  
- **NeetCode:** <https://neetcode.io/problems/naming-a-company>  
- **Video:** <https://www.youtube.com/watch?v=NrHpgTScOcY>  

[← Back to index](../INDEX.md)

## 1. Brute Force

To form a valid company name, we pick two distinct ideas and swap their first letters. The resulting two names must both be new (not in the original list). A straightforward approach checks every pair of ideas, performs the swap, and verifies that neither swapped name exists in the original set. We track valid combinations in a set to avoid counting duplicates.

This works but is slow because we examine O(n^2) pairs, and string operations add additional cost.

```cpp
class Solution {
public:
    long long distinctNames(vector<string>& ideas) {
        int n = ideas.size();
        unordered_set<string> res;
        unordered_set<string> ideasSet(ideas.begin(), ideas.end());

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                string A = ideas[j][0] + ideas[i].substr(1);
                string B = ideas[i][0] + ideas[j].substr(1);

                if (!ideasSet.count(A) && !ideasSet.count(B)) {
                    res.insert(A + " " + B);
                    res.insert(B + " " + A);
                }
            }
        }

        return res.size();
    }
};
```

**Complexity**

- Time complexity: $O(m * n ^ 2)$
- Space complexity: $O(m * n ^ 2)$

> Where $n$ is the size of the array $ideas$ and $m$ is the average length of the strings.

## 2. Group By First Letter (Hash Map)

The key insight is that swapping first letters only matters between ideas that start with different letters. If two ideas share the same first letter, swapping produces the same names back.

Group ideas by their first letter, storing only the suffixes (the part after the first character). For two groups with different first letters, a swap is valid if the suffix appears in exactly one group (not both). If a suffix appears in both groups, swapping would produce an existing name.

For groups A and B, count how many suffixes are shared (the intersection). The number of valid pairs is (size of A minus intersection) times (size of B minus intersection).

```cpp
class Solution {
public:
    long long distinctNames(vector<string>& ideas) {
        unordered_map<char, unordered_set<string>> wordMap;
        for (const string& word : ideas) {
            wordMap[word[0]].insert(word.substr(1));
        }

        long long res = 0;
        for (auto& [char1, set1] : wordMap) {
            for (auto& [char2, set2] : wordMap) {
                if (char1 == char2) continue;

                int intersect = 0;
                for (const string& w : set1) {
                    if (set2.count(w)) {
                        intersect++;
                    }
                }

                int distinct1 = set1.size() - intersect;
                int distinct2 = set2.size() - intersect;
                res += distinct1 * 1LL * distinct2;
            }
        }

        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $n$ is the size of the array $ideas$ and $m$ is the average length of the strings.

## 3. Group By First Letter (Array)

This approach is the same as the hash map solution, but uses a fixed-size array of 26 sets instead of a hash map. Since we only deal with lowercase letters, indexing by (character minus 'a') gives us direct array access, which can be slightly faster.

We also optimize by only iterating over pairs (i, j) where i < j, then multiplying the result by 2 to account for both orderings.

```cpp
class Solution {
public:
    long long distinctNames(vector<string>& ideas) {
        unordered_set<string> suffixes[26];
        for (const string& w : ideas) {
            suffixes[w[0] - 'a'].insert(w.substr(1));
        }

        long long res = 0;
        for (int i = 0; i < 26; i++) {
            for (int j = i + 1; j < 26; j++) {
                int intersect = 0;
                for (const string& s : suffixes[i]) {
                    if (suffixes[j].count(s)) {
                        intersect++;
                    }
                }
                res += 2LL * (suffixes[i].size() - intersect) * (suffixes[j].size() - intersect);
            }
        }
        return res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $n$ is the size of the array $ideas$ and $m$ is the average length of the strings.

## 4. Counting

Instead of computing intersections for each pair of letters, we can build a count matrix incrementally. For each suffix, we know which first letters it appears with. We process suffixes one by one and maintain count[i][j], which tracks how many suffixes have appeared with letter i but not with letter j.

When we encounter a suffix that appears with letter i but not letter j, any previous suffix that appeared with letter j but not letter i forms a valid pair. We look up count[j][i] to find how many such suffixes exist.

```cpp
class Solution {
public:
    long long distinctNames(vector<string>& ideas) {
        unordered_map<string, array<bool, 26>> mp;
        long long count[26][26] = {};
        long long res = 0;

        for (const string& s : ideas) {
            int firstChar = s[0] - 'a';
            string suffix = s.substr(1);
            mp[suffix][firstChar] = true;
        }

        for (auto& [suffix, arr] : mp) {
            for (int i = 0; i < 26; i++) {
                if (arr[i]) {
                    for (int j = 0; j < 26; j++) {
                        if (!arr[j]) {
                            count[i][j]++;
                            res += count[j][i];
                        }
                    }
                }
            }
        }
        return 2 * res;
    }
};
```

**Complexity**

- Time complexity: $O(m * n)$
- Space complexity: $O(m * n)$

> Where $n$ is the size of the array $ideas$ and $m$ is the average length of the strings.

## Standalone solution file (`cpp/2306-naming-a-company.cpp` in the NeetCode repo)

```cpp
//time O(n)
//space O(n)

class Solution {
public:
    long long distinctNames(vector<string>& ideas) {
        
        unordered_map<char,unordered_set<string>> dict;
        
        for(const string& idea : ideas){
            dict[idea[0]].insert(idea.substr(1));
        } 
        
        if(dict.size() < 2){
            return 0;
        }
         
        long long count = 0;
        
        for(char a = 'a'; a <= 'z' ; a++){
             
            if(dict.find(a) == dict.end())
                continue;
                        
            for(char b = a+1; b <= 'z'; b++){
                
                if(dict.find(b) == dict.end())
                    continue;
                
                int aKeys = dict[a].size();
                int bKeys = dict[b].size();
                 
                for(const string& suffix : dict[a]){
                    if(dict[b].find(suffix) != dict[b].end()){
                        aKeys--;
                        bKeys--;
                    }
                }
                
                count += 2 * (aKeys*bKeys);
            }
        }
        
        return count;
    }
};
```
