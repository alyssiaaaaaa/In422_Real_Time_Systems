int comparaison (int x, int y){
    
    if (x>y){
       printf("%d\n", x); 
       return 1;
    }
    if (y>x){        
        printf("%d\n", y);
        return -1;
    }
    else{
        return 0;
    }
}

int compter_for(){
    for (int n = 0; n<100; n++){
        printf("%d\n", n);        
    }
    return 0;
}

int compter_while(){
    int n = 0;
    while (n<100){
        printf("%d\n", n);
        n++;
    }
    return 0;
}

int assign_value(int i, char c){
    return 0; // i don't undernstand the question
}

int somme(int n, int m){
    int s = n+m;
    return s;
}

