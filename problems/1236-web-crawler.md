# 1236. Web Crawler

- **Difficulty:** Medium  
- **Pattern:** Graphs  
- **Lists:** NeetCode All  
- **LeetCode:** <https://leetcode.com/problems/web-crawler/>  
- **NeetCode:** <https://neetcode.io/problems/web-crawler>  

[← Back to index](../INDEX.md)

## 1. Depth-first search

Web crawling naturally fits a graph traversal problem where URLs are nodes and links between them are edges. The key insight is that we need to explore all reachable URLs from the starting URL while staying within the same hostname. `dfs` allows us to follow links deeply before backtracking, using a `visited` set to avoid infinite loops from cycles.

```cpp
class Solution {
public:
    vector<string> crawl(string startUrl, HtmlParser htmlParser) {
        function<string(string)> getHostname = [](string url) -> string {
            // find the next slash in the url after "http://"
            // that is after the 7-th position inclusively
            // if there is no such slash, pos will be equal to url.size()
            int pos = min(url.size(), url.find('/', 7));
            // return the substring that starts after "http://" and ends
            // before the next slash of at the end of the string
            return url.substr(7, pos - 7);
        };

        string startHostname = getHostname(startUrl);
        unordered_set<string> visited;

        function<void(string)> dfs = [&](string url) -> void {
            visited.insert(url);
            for (string nextUrl : htmlParser.getUrls(url)) {
                if (getHostname(nextUrl) == startHostname && !visited.count(nextUrl)) {
                    dfs(nextUrl);
                }
            }
        };

        dfs(startUrl);
        return vector<string>(visited.begin(), visited.end());
    }
};
```

**Complexity**

- Time complexity: $O(m \cdot l)$
- Space complexity: $O(m \cdot l)$

> Where $m$ is the number of edges in the graph, and $l$ is the maximum length of a URL (`urls[i].length`).

## 2. Breadth-first search

`bfs` provides an alternative traversal that explores URLs level by level, visiting all URLs at distance 1 before distance 2, and so on. This approach uses a queue instead of recursion and naturally discovers URLs in order of their distance from the starting URL.

```cpp
class Solution {
public:
    vector<string> crawl(string startUrl, HtmlParser htmlParser) {
        function<string(string)> getHostname = [](string url) -> string {
            // find the next slash in the url after "http://"
            // that is after the 7-th position inclusively
            // if there is no such slash, pos will be equal to url.size()
            int pos = min(url.size(), url.find('/', 7));
            // return the substring that starts after "http://" and ends
            // before the next slash or at the end of the string
            return url.substr(7, pos - 7);
        };

        queue<string> q;
        q.push(startUrl);
        unordered_set<string> visited{startUrl};
        string startHostname = getHostname(startUrl);
        while (!q.empty()) {
            string url = q.front();
            q.pop();
            for (string nextUrl : htmlParser.getUrls(url)) {
                if (getHostname(nextUrl) == startHostname && !visited.count(nextUrl)) {
                    q.push(nextUrl);
                    visited.insert(nextUrl);
                }
            }
        }
        return vector<string>(visited.begin(), visited.end());
    }
};
```

**Complexity**

- Time complexity: $O(m \cdot l)$
- Space complexity: $O(n \cdot l)$

> Where $m$ is the number of edges in the graph, $l$ is the maximum length of a URL (`urls[i].length`), and $n$ is the total number of URLs (`urls.length`).
