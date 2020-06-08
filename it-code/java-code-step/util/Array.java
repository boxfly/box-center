package util;
import java.util.Arrays;
public class Array { 
    public static void main(String[] args) {  
        int[] a = new int[10];
        for(int i = 0;i < 10;i++){ a[i] = i; }
        System.out.println("初始值:" + Arrays.toString(a) );
        a = reserve1(a);
        System.out.println("反转后的返回值：" + Arrays.toString(a) );
        reserve2(a);
        System.out.println("引用地址反转后：" + Arrays.toString(a) );
        //二维数组的特性
        int[][] a2 = { {1,2,3}, {2,3},{1,2,3} };
        System.out.println("a2 length is " + a2.length);
        for(int i = 0;i < a2.length;i++){
            System.out.println(i+" is "+a2[i].length);
        }

    }
    
    //从方法中返回原数组的反转数组
    public static int[] reserve1(int[] list){
        int[] result = new int[list.length];
        for(int i = 0,j = result.length-1;i < list.length;i++,j--){
            result[j] = list[i];
        }
        return result;
    }
    
    //直接处理：引用传递
    public static void reserve2(int[] list){
        int temp;
        for(int i = 0,j = list.length - 1;i < list.length / 2;i++,j--){
            temp = list[i];
            list[i] = list[j];
            list[j] = temp;
        }
    }
    //可变长的参数列表 用来设计打印数组
    public static void printArray(int... num){
        if(num.length == 0){
            System.out.println("No 参数！");
        }
        else{
            for(int i = 0;i < num.length;i++){
                System.out.print(num[i] + "  ");
            }
            System.out.print("\n");
        }
    }

}