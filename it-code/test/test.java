// We have imported the necessary tool classes.
// If you need to import additional packages or classes, please import here.
import java.util.*;
public class test {
    public static void main(String[] args) {
        String indexOf = "indexOf";
        System.out.println();
        System.out.println(indexOf.indexOf("indexOf"));
        
        int [] arr = {1,2,3};
        min(arr);     
    }
    public static void min(int[] num) { 
        int a[] = { 1, 2, 5, 3, 7, 234, 214, 1342432421, 4, 2 }; 
        Arrays.sort(a);  
        System.out.println("max:"+a[a.length-1]);
        List nums =  new ArrayList();nums.add(2); nums.add(5);    
        System.out.println( Collections.max(nums));
        //设置最大值Max    
        String[] strings = {"1", "2", "3"};
        int[] array = Arrays.stream(strings).mapToInt(Integer::parseInt).toArray();  
        System.out.println(Arrays.toString(array));    
      
        int minnum = num[0]; 
        for (int i=0;i<num.length;i++){if(num[i]<minnum){minnum = num[i];}}
        System.out.println("min number is :"+minnum);        
    }
}
