package animal;
 
public interface Animal { 
    public double isLife();
    public void eat();
    public void move();
    public void die();
}
/*
   Animal 
    ---> Bird --->  sparrow
    ---> Cat  --->  tabby cat 
    ---> Dog  --->  spotted dog
*/