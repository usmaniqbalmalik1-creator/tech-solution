#include <iostream>
#include <vector>
#include <unordered_map>
#include <stack>
#include <string>
using namespace std;
pair<int,int>twoSum(const vector<int>&a,int target){unordered_map<int,int>p;for(int i=0;i<a.size();++i){int n=target-a[i];if(p.count(n))return{p[n],i};p[a[i]]=i;}return{-1,-1};}
bool validParentheses(const string&s){stack<char>st;for(char c:s){if(c=='('||c=='['||c=='{')st.push(c);else{if(st.empty())return false;char t=st.top();st.pop();if((c==')'&&t!='(')||(c==']'&&t!='[')||(c=='}'&&t!='{'))return false;}}return st.empty();}
int main(){vector<int>a={2,7,11,15};auto p=twoSum(a,9);cout<<"Two Sum: "<<p.first<<","<<p.second<<"\n";cout<<"Parentheses: "<<(validParentheses("{[()]}")?"valid":"invalid")<<"\n";}