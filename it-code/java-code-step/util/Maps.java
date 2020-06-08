package util;

import java.util.*;
public class Maps {
    public static void main(String[] args) {  
        /*
        HashMap  
        TreeMap 
        LinkedHashMap 
        */
        test();
    }
    private static void test() {
        Map<String,Integer> hashMap = new HashMap<String,Integer>();
        hashMap.put("Smith", 30);
        hashMap.put("Anderson", 31);
        hashMap.put("Lewis", 29);
        hashMap.replace("Lewis", 35);
        System.out.println(hashMap.containsKey("Anderson"));
        
        System.out.println("Display entries in HashMap");
        System.out.println(hashMap );
        Map<String,Integer> treeMap = new TreeMap<String,Integer>(hashMap);
        System.out.println("Display entries in ascending order of key");
        System.out.println(treeMap);
        Map<String,Integer> linkedHashMap = new LinkedHashMap<String,Integer>(16,0.75f,true);
        linkedHashMap.put("Smith", 30);
        linkedHashMap.put("Anderson",31);
        linkedHashMap.put("Lewis", 29);
        linkedHashMap.put("Cook", 29);
        
        System.out.println("The age for " + "Lewis is " + linkedHashMap.get("Lewis").intValue());
        
        System.out.println("Display entries in LinkedHashMap");
        System.out.println(linkedHashMap);
    }
}
