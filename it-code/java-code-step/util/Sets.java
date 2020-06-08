package util;

import java.util.*;
public class Sets {
    public static void main(String[] args) {  
        HashSet();
        LinkedHashSet();
        TreeSet();
    }
    private static void HashSet() {
        Set<String> set = new HashSet<String>();
        set.add("London");
        set.add("London");
        set.add("Paris");
        set.add("New York");
        //迭代器迭代
        Iterator<String> iterator = set.iterator();
        while(iterator.hasNext()){
            System.out.println(iterator.next().toUpperCase());
        }
    }
    public static void LinkedHashSet() {
        Set<String> set = new LinkedHashSet<String>();
        set.add("London");
        set.add("Paris");
        for(Object element:set) System.out.println(element.toString());
    }
    public static void TreeSet() {
        Set<String> set = new HashSet<String>();
        set.add("London");
        set.add("Paris");
        set.add("New York");
        
        TreeSet<String> treeSet = new TreeSet<String>(set);
        System.out.println("Sorted tree set: " + treeSet);
        
        System.out.println("first()" + treeSet.first());
        System.out.println("last()" + treeSet.last());
        System.out.println("headSet(): " + treeSet.headSet("New York"));
        System.out.println("tailSet(): " + treeSet.tailSet("New York"));
        
        System.out.println("lower(\"P\"): " + treeSet.lower("P"));
        System.out.println("higher(\"P\"): " + treeSet.higher("P"));
        System.out.println("floor(\"P\"): " + treeSet.floor("P"));
        System.out.println("ceiling(\"P\"): " + treeSet.ceiling("P"));
        System.out.println("pollFirst(): " + treeSet.pollFirst());
        System.out.println("pollLast() : " + treeSet.pollLast());
        System.out.println("New tree set: " + treeSet);
    }
}
