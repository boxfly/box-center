package test;
import util.*;
public class InnerTest {
    private String testDay = "20200202";
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
    public String getPrivateTestDay(){// 外部通过方法访问私有变量
        return this.testDay;
    }
}