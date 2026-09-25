#include <iostream>
#include <vector>
#include <queue>
#include <limits>
using namespace std;
vector<int> mergeSort(const vector<int>& a){if(a.size()<=1)return a;int m=a.size()/2;vector<int>l(a.begin(),a.begin()+m),r(a.begin()+m,a.end());l=mergeSort(l);r=mergeSort(r);vector<int>o;int i=0,j=0;while(i<l.size()||j<r.size()){if(j==r.size()||(i<l.size()&&l[i]<=r[j]))o.push_back(l[i++]);else o.push_back(r[j++]);}return o;}
int binarySearch(const vector<int>&a,int x){int l=0,r=a.size()-1;while(l<=r){int m=l+(r-l)/2;if(a[m]==x)return m;if(a[m]<x)l=m+1;else r=m-1;}return -1;}
vector<int>bfs(const vector<vector<int>>&g,int s){vector<int>v(g.size()),o;queue<int>q;q.push(s);v[s]=1;while(!q.empty()){int u=q.front();q.pop();o.push_back(u);for(int x:g[u])if(!v[x])v[x]=1,q.push(x);}return o;}
void dfs(int u,const vector<vector<int>>&g,vector<int>&v,vector<int>&o){v[u]=1;o.push_back(u);for(int x:g[u])if(!v[x])dfs(x,g,v,o);}
vector<long long>dijkstra(const vector<vector<pair<int,int>>>&g,int s){const long long I=numeric_limits<long long>::max()/4;vector<long long>d(g.size(),I);priority_queue<pair<long long,int>,vector<pair<long long,int>>,greater<pair<long long,int>>>q;d[s]=0;q.push({0,s});while(!q.empty()){auto [du,u]=q.top();q.pop();if(du!=d[u])continue;for(auto [v,w]:g[u])if(d[v]>du+w)d[v]=du+w,q.push({d[v],v});}return d;}
int main(){vector<int>a={9,4,7,1,6,2};auto s=mergeSort(a);for(int x:s)cout<<x<<" ";cout<<"\nIndex of 6: "<<binarySearch(s,6)<<"\n";vector<vector<int>>g={{1,2},{3},{3},{4},{}};auto b=bfs(g,0);cout<<"BFS: ";for(int x:b)cout<<x<<" ";cout<<"\n";vector<int>v(g.size()),o;dfs(0,g,v,o);cout<<"DFS: ";for(int x:o)cout<<x<<" ";cout<<"\n";}