#include "AvlTree.h"
#include "CFile.h"

#include <iostream>
#include <vector>

using namespace std;
typedef int T;

template <class T>
struct Lless{
	bool operator()(T a, T b){
		return a < b;
	}
};

struct Trait{
	typedef int T;
	typedef Lless<T> C;
};


int main(int argc, char* argv[]){
	long data;
	CFile cfile;
   	if (argc == 3){
		if(*argv[1]=='g' ){
			cfile.generate_file();
			cout<<"generado"<<endl;
			return 0;
		}
		else if(*argv[1]=='f')
		data = strtol(argv[2], NULL, 10);
	}
	else{
		cout<<"Mal ingreso"<<endl;
		cout<<argv[0]<< " [g] [tamaño]"<<endl ;
		cout<<argv[0]<< " [f] [dato a buscar]"<<endl;
	return 0;
	}
	AvlTree<Trait> avltree;
	
	/* INSERT */
	vector<int> m_vector = cfile.read_file();
	for (int i=0, j=0; i<m_vector.size();i++,j+=12)
		avltree.insert(m_vector[i],j);
	
	/* PRINT */
	// cout<<"print\n";
	// avltree.printLe(avltree.root);	
	// cout<<endl;
	
	/* FIND */
	cout<<int(data)<<" se encuentra: ";
	cout<<avltree.find(int(data));
	cout<<endl;




	return 0;
}
