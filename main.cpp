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

int n_bytes=0;
template <class T>
struct Lless{
	bool operator()(T a, T b){
		return a < b;
	}
};

struct Trait{
	typedef t T;
	typedef Lless<T> C;
};


int main(int argc, char* argv[]){
	t data;
	int col;

	// string data;
	AvlTree<Trait> avltree;
	CFile cfile;
	char op='1';
	clock_t ti;

   	if (argc != 3){
		cout<<"Mal ingreso"<<endl;
		cout<<argv[0]<< " [g] "<<endl ;
		cout<<argv[0]<< " [i] [col]"<<endl;
		return 0;
	}
	if(*argv[1]=='g' ){
		cfile.generate_file();
		cout<<"generado"<<endl;
		return 0;
	}
	else if(*argv[1]=='i'){
	col=int(strtol(argv[2], NULL, 10));

	/* INSERT */
	n_bytes=cfile.number_bytes();
	cout<<"n_bytes: "<<n_bytes<<endl;
	vector<T> m_vector = cfile.read_file(col);
	// cout<<"m_vectior"<<endl;
	// for(int i=0;i<m_vector.size();i++)
	// 	cout<<m_vector[i]<<" ";
	for (N i=0, j=n_bytes; i<m_vector.size();i++,j+=n_bytes)
		avltree.insert(m_vector[i],j);
		// avltree.insert(stol(m_vector[i]),j);
	/* PRINT */
	
	cout<<"print\n";
	avltree.printLe2(avltree.root);	
	cout<<endl;
	
	/* FIND */

	while(data!="0"){
	cout<<"data: ";
	cin.ignore(); 
	getline(cin,data);
	cout<<data<<" se encuentra: ";
	vector<N> tmp;
	// ti = clock();
	if(avltree.find2(data,tmp)==false){
	cout<<"error no encontrado\n"; return 0;}
	
	for(int i=0;i<tmp.size();i++)
		cout<<tmp[i]<<" contiene: "<<cfile.read_file_p(tmp[i])<<endl;
	ti = clock() - ti;
	cout<<"tiempo: "<<((float)ti)/CLOCKS_PER_SEC<<endl;
		}
	}

	return 0;
}
