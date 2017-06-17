/*
 g++ main.cpp -o sgbd
./sgbd i 
*/

#include "AvlTree.h"
#include "CFile.h"

#include <iostream>
#include <vector>
#include <time.h>
#include <stdio.h>
#include <string.h>

using namespace std;

typedef string t;
// typedef unsigned long int t;
typedef unsigned long int N;
int col=2;

int n_bytes=0;

template <class T>
struct Sless{
	bool operator()(T a, T b){
		char *cstr_a = new char[a.length() + 1];
		strcpy(cstr_a, a.c_str());
		
		char *cstr_b = new char[b.length() + 1];
		strcpy(cstr_b, b.c_str());

		
		// do stuff

		// delete [] cstr_a;
		// delete [] cstr_b;
		return strcmp(cstr_a, cstr_b);
	}
};
template <class T>
struct Lless{
	bool operator()(T a, T b){
		return a < b;
	}
};

struct Trait{
	typedef t T;
	typedef Sless<T> C;
};


int main(int argc, char* argv[]){
	t data;
	// string data;
	AvlTree<Trait> avltree;
	CFile cfile;
	char op='1';
	clock_t ti;

   	if (argc != 2){
		cout<<"Mal ingreso"<<endl;
		cout<<argv[0]<< " [g] "<<endl ;
		cout<<argv[0]<< " [i] "<<endl;
		return 0;
	}
	if(*argv[1]=='g' ){
		cfile.generate_file();
		cout<<"generado"<<endl;
		return 0;
	}
	else if(*argv[1]=='i'){

	/* INSERT */
	n_bytes=cfile.number_bytes();
	cout<<"n_bytes: "<<n_bytes<<endl;
	vector<T> m_vector = cfile.read_file(col);
	// cout<<"m_vectior"<<endl;
	// for(int i=0;i<m_vector.size();i++)
	// 	cout<<m_vector[i]<<" ";
	cout<<endl;
	for (N i=0, j=n_bytes; i<m_vector.size();i++,j+=n_bytes)
		avltree.insert(m_vector[i],j);
		// avltree.insert(stol(m_vector[i]),j);
	/* PRINT */
	cout<<"print\n";
	avltree.printLe(avltree.root);	
	cout<<endl;
	
	/* FIND */
	while(op=='1'){
	cout<<"data:\n";
	cin.ignore(); 
	getline(cin,data);
	// cin>>data;
	cout<<data<<" se encuentra: ";
	
	N tmp=0;
	ti = clock();
	if(avltree.find(data,tmp)==false){
		cout<<"error no encontrado\n"; return 0;}
		cout<<tmp<<" contiene: "<<cfile.read_file_p(tmp)<<endl;
		ti = clock() - ti;
		cout<<"tiempo: "<<((float)ti)/CLOCKS_PER_SEC<<tmp<<endl;
		cout<<"(1): continuar: ";cin>>op;
	if(op!='1') return 0;
	}
	}


	return 0;
}
