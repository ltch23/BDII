#include "AvlTree.h"
#include <iostream>
using namespace std;

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


int main()
{
	AvlTree<Trait> avltree;
	avltree.insert(5,10);
	avltree.insert(2,20);
	avltree.insert(1,30);
	avltree.insert(3,15);
	avltree.insert(7,17);
	cout<<"print\n";
	avltree.printLe(avltree.root);	
	cout<<endl;
	// avltree.remove(1);
	// cout<<"print\n";
	// avltree.printLe(avltree.root);	
	// cout<<endl;
	

	return 0;
}
