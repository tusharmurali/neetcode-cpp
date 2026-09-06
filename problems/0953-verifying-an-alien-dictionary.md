# 953. Verifying An Alien Dictionary

- **Difficulty:** Easy  
- **Pattern:** Graphs  
- **Lists:** NeetCode 250  
- **LeetCode:** <https://leetcode.com/problems/verifying-an-alien-dictionary/>  
- **NeetCode:** <https://neetcode.io/problems/verifying-an-alien-dictionary>  
- **Video:** <https://www.youtube.com/watch?v=OVgPAJIyX6o>  

[← Back to index](../INDEX.md)

## 1. Sorting

If the words are sorted according to the alien dictionary order, they should remain in the same order after sorting. The key insight is that we can create a mapping from each character to its position in the alien alphabet, then use this mapping to define a custom comparator for sorting.

```cpp
class Solution {
public:
    bool isAlienSorted(vector<string>& words, string order) {
        int orderIndex[26];
        for (int i = 0; i < order.size(); ++i)
            orderIndex[order[i] - 'a'] = i;

        auto compare = [&](const string &a, const string &b) {
            for (int i = 0; i < min(a.size(), b.size()); ++i) {
                if (a[i] != b[i])
                    return orderIndex[a[i] - 'a'] < orderIndex[b[i] - 'a'];
            }
            return a.size() < b.size();
        };

        return is_sorted(words.begin(), words.end(), compare);
    }
};
```

**Complexity**

- Time complexity: $O(n * m\log n)$
- Space complexity: $O(n * m)$

> Where $n$ is the number of words and $m$ is the average length of a word.

## 2. Comparing adjacent words

For a list to be sorted, each adjacent pair must be in the correct order. Instead of sorting, we can directly verify that each word is lexicographically less than or equal to the next word according to the alien order. This avoids the overhead of sorting.

```cpp
class Solution {
public:
    bool isAlienSorted(vector<string>& words, string order) {
        int orderIndex[26] = {0};
        for (int i = 0; i < order.size(); ++i)
            orderIndex[order[i] - 'a'] = i;

        for (int i = 0; i < words.size() - 1; ++i) {
            string w1 = words[i], w2 = words[i + 1];
            int j = 0;

            for (; j < w1.size(); ++j) {
                if (j == w2.size()) return false;
                if (w1[j] != w2[j]) {
                    if (orderIndex[w1[j] - 'a'] > orderIndex[w2[j] - 'a'])
                        return false;
                    break;
                }
            }
        }
        return true;
    }
};
```

**Complexity**

- Time complexity: $O(n * m)$
- Space complexity: $O(1)$ since we have $26$ different characters.

> Where $n$ is the number of words and $m$ is the average length of a word.

## Standalone solution file (`cpp/0953-verifying-an-alien-dictionary.cpp` in the NeetCode repo)

```cpp
/*
    Given list of words in another language, return string such that:
    Letters are sorted in lexicographical incr order wrt this language
    Ex. words = ["wrt","wrf","er","ett","rftt"]

    Build graph + record edges, BFS + topological sort, check cyclic

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    string alienOrder(vector<string> &words) {
        
        unordered_map<char, unordered_set<char>> graph;
        unordered_map<char, int> indegree;

        // indegree make all char 0
        for(auto word : words){
            for(auto c : word){
                indegree[c]=0;
            }
        }

        for(int i=0; i<words.size()-1; i++){
            string curr = words[i];
            string next = words[i+1];
            
            bool flag = false;
            int len = min(curr.length(), next.length());
            for(int j=0; j<len; j++){
                char ch1 = curr[j];
                char ch2 = next[j];

                if(ch1 != ch2){
                    unordered_set<char> set;

                    if(graph.find(ch1) != graph.end()){
                        set = graph[ch1];

                        if(set.find(ch2) == set.end()){
                            set.insert(ch2);
                            indegree[ch2]++;
                            graph[ch1] = set;
                        }
                    }
                    else{
                        set.insert(ch2);
                        indegree[ch2]++;
                        graph[ch1] = set;
                    }

                    flag = true;
                    break;
                }
                
            }

            if(flag == false and (curr.length() > next.length())) return "";
        }

        priority_queue<char, vector<char>, greater<char>> q;

        for(auto it : indegree){
            if(it.second == 0){
                //cout<<it.first<<endl;
                q.push(it.first);
            }
        }

        int count=0;
        string ans = "";

        while(q.size()>0){
            auto rem = q.top();
            q.pop();

            ans += rem;
            count++;

            if(graph.find(rem) != graph.end()){
                unordered_set<char> nbrs = graph[rem];

                for(auto nbr : nbrs){
                    indegree[nbr]--;
                    if(indegree[nbr] == 0){
                        q.push(nbr);
                    }
                }
            }
        }

        if(count == indegree.size()){
            return ans;
        }
        return "";
    }
};
```
