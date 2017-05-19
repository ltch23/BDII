#ifndef CFILE_H
#define CFILE_H


#include <iostream>
#include <fstream>
#include <thread>
#include <vector>
#include <stdio.h>

using namespace std;

class CFile{
public:
    vector<thread> m_threads;
    vector<string> m_vector ;
    vector<string> m_vector2 ;
    vector<string> zeros;
    unsigned int n;
    unsigned int m_part;
    unsigned int N;
    
    CFile();
    void save_file();
    void generate_file();
    void fill_file(int);
    string read_file_p(int);
    vector<int> read_file(); 
};

CFile::CFile(){
    N=5000;
    n = 4;
    m_vector.resize(N) ;
    m_vector2.resize(N) ;
    zeros = {"0000","000","00","0",""};
    m_part=N/n;
}

void CFile::save_file(){
    ofstream file("numbers.txt") ;
    for(int i=0; i<N ;i++){
        file << m_vector[i]<<" ";
        file << m_vector2[i]<< "\n";
    }
    file.close();
}

void CFile::fill_file(int n_thread){
    int size=0,i,j;
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

    for (int i=0; i < n ; i++)
    m_threads.push_back(thread(&CFile::fill_file,this,i));

    for (int i=0; i < n ; i++)
    m_threads[i].join();
    save_file();
}

string CFile::read_file_p(int pos){
    string data;
    FILE* ptr_file = fopen("numbers.txt","r");
    fseek(ptr_file,pos,SEEK_SET);
    for (int i=0;i<11;i++)
    data+=getc(ptr_file);
    //int pos=ftell(ptr_file);
    fclose(ptr_file);
    return data;
}
vector<int> CFile::read_file(){
    string line;
    vector<int> rpta(N);
    ifstream is_file("numbers.txt");
    int i=0;
    while ( getline (is_file,line)){
        line=line.erase(5,6);
        rpta[i]=stoi(line);
        i++;
    }
    is_file.close(); 
    return rpta;
    
}

#endif //CFILE