#ifndef CFILE_H
#define CFILE_H


#include <iostream>
#include <fstream>
#include <thread>
#include <vector>
#include <stdio.h>
#define col 17
typedef long int T;

using namespace std;

class CFile{
public:
    vector<thread> m_threads;
    vector<string> m_vector ;
    vector<string> m_vector2 ;
    vector<string> zeros;
    int n;
    T m_part;
    T N;
    int n_bytes;
    
    CFile();
    void save_file();
    void generate_file();
    void fill_file(int);
    int number_bytes();
    string read_file_p(T);
    vector<T> read_file(); 
};

CFile::CFile(){
    N=20001;
    n = 4;
    m_vector.resize(N) ;
    m_vector2.resize(N) ;
    zeros = {"0000","000","00","0",""};
    m_part=N/n;

}

void CFile::save_file(){
    ofstream file("numbers.txt") ;
    for(T i=0; i<N ;i++){
        file << m_vector[i]<<" ";
        file << m_vector2[i]<< "\n";
    }
    file.close();
}

void CFile::fill_file(int n_thread){
    T size=0,i,j;
    for(i=m_part*n_thread,j=N-i-1;i<m_part*(n_thread+1);i++,j--){
        m_vector[i]=to_string(i);
        size=m_vector[i].size();
        m_vector[i].insert(0,zeros[size-1]);   
        m_vector2[i]=to_string(j);
        size=m_vector2[i].size();
        m_vector2[i].insert(0,zeros[size-1]);   
    }
    
}

void CFile::generate_file(){

    //cout<<N<<endl;
    for (int i=0; i < n ; i++)
    m_threads.push_back(thread(&CFile::fill_file,this,i));

    for (int i=0; i < n ; i++)
    m_threads[i].join();
    save_file();
}

string CFile::read_file_p(T pos){
    string data;
    FILE* ptr_file = fopen("numbers.txt","r");
    fseek(ptr_file,pos,SEEK_SET);
    for (int i=0;i<n_bytes;i++)
        data+=getc(ptr_file);
    //int pos=ftell(ptr_file);
    fclose(ptr_file);
    return data;
}
int CFile::number_bytes(){
    string line;
    ifstream is_file("numbers.txt");
    getline (is_file,line);
    n_bytes=line.size();
    is_file.close();
    return n_bytes;
}

vector<T> CFile::read_file(){
    string line;
    vector<T> rpta(N);
    ifstream is_file("numbers.txt");
    T i=0;
    getline (is_file,line);
    while ( getline (is_file,line)){
        line=line.erase(col,n_bytes-col);
        rpta[i]=stol(line);
        i++;
    }
    is_file.close(); 
    return rpta;
    
}

#endif //CFILE
