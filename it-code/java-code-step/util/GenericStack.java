package util;
/*
泛型 放你想放的元素
*/
public class GenericStack<Element> {
    
    private java.util.ArrayList<Element> list = new java.util.ArrayList<Element>();

    public int getSize(){
        return list.size();
    }

    public Element peek(){
        return list.get(getSize() - 1);
    }

    public void push(Element o){
        list.add(o);
    }

    public Element pop(){
        Element o = list.get(getSize() - 1);
        list.remove(getSize() - 1);
        return o;
    }

    public boolean isEmpty(){
        return list.isEmpty();
    }
}