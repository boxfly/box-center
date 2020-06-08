package test;
import util.*;
public class Test { 
    public static void main(String[] args) {  
        // testTV();
        // InnerTest.testTV();
        System.out.println(new InnerTest().getPrivateTestDay());
        
    }
    public static void testTV() {  
        TV tv = new TV();
        tv.turnOn();
        tv.setChannel(30);
        tv.setVolume(3); 
       
        System.out.println("count1 = " + tv.numplus());
        System.out.println("count2 = " + tv.numplus());
        System.out.println("tv1's channel is" + tv.channel  
        + "\n number is " + tv.num
        + "\n volume level is " + tv.volumeLevel
        );
    }
}