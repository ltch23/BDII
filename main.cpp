
/*
 g++ main.cpp -lpthread -o sgbd
./sgbd g 50000
./sgbd f [0-50000]
*/

#include "AvlTree.h"
#include "CFile.h"

#include <iostream>
#include <vector>
#include <time.h>

using namespace std;

typedef long int T;

int n_bytes=0;

template <class T>
struct Lless{
	bool operator()(T a, T b){
		return a < b;
	}
};

struct Trait{
	typedef long int T;
	typedef Lless<T> C;
};


int main(int argc, char* argv[]){
	T data;
	AvlTree<Trait> avltree;
	CFile cfile;
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
	vector<T> m_vector = cfile.read_file();
	// cout<<"m_vectior"<<endl;
	// for(int i=0;i<m_vector.size();i++)
	// 	cout<<m_vector[i]<<" ";
	cout<<endl;
	for (T i=0, j=n_bytes; i<m_vector.size();i++,j+=n_bytes)
		avltree.insert(m_vector[i],j);
	
	/* PRINT */
	// cout<<"print\n";
	// avltree.printLe(avltree.root);	
	// cout<<endl;
	
	/* FIND */
	char op='1';
	while(op=='1'){
	cout<<"data: ";cin>>data;
	cout<<data<<" se encuentra: ";
	clock_t t;
	t = clock();
	T tmp;
	if(avltree.find(data,tmp)==false){
	cout<<"error no encontrado\n"; return 0;}
	cout<<tmp<<" contiene: "<<cfile.read_file_p(tmp)<<endl;
	t = clock() - t;
	cout<<"tiempo: "<<((float)t)/CLOCKS_PER_SEC<<tmp<<endl;
	cout<<"(1): continuar: ";cin>>op;
	if(op!='1') return 0;
	}
	}


	return 0;
}
