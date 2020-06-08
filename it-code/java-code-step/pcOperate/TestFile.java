package pcOperate;

import java.io.FileNotFoundException;

public class TestFile {
    public static void main(String[] args) {
        fileFunction();
        testWrite();
        testScanner();
    }

    public static void fileFunction() {
        java.io.File file = new java.io.File("image/gif");
        System.out.println("Does it exist? " + file.exists());
        System.out.println("The file has " + file.length() + " bytes");
        System.out.println("can it be read? " + file.canRead());
        System.out.println("can it be written? " + file.canWrite());
        System.out.println("Is it a directory? " + file.isDirectory());
        System.out.println("Is it a file? " + file.isFile());
        System.out.println("Is it absolute? " + file.isAbsolute());
        System.out.println("Is it a Hidden? " + file.isHidden());
        System.out.println("Absolute path is " + file.getAbsolutePath());
        System.out.println("Last modified on " + new java.util.Date(file.lastModified()));
    }

    public static void testWrite() {
        java.io.File file = new java.io.File("test.txt"); // 建立文件对象
        if (file.exists()) {
            System.out.println("File already exist");
            System.exit(0);
        }

        java.io.PrintWriter output = null;
        try {
            output = new java.io.PrintWriter(file);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        output.print("this is test code ");
        output.print(10086);
        output.println("!"); 
        output.close();
    } 
    public static void testScanner() {
        /*
        next()方法读取一个由分隔符分隔的字符串，
        nextLine()读取一个以行分隔符结束的行
        */
        java.io.File file = new java.io.File("test.txt"); // 1 bobi 25
         java.util.Scanner sc = null;
        try {
            sc = new java.util.Scanner(file);
        } catch (FileNotFoundException e) { 
            e.printStackTrace();
        } // 扫描来源
        //java.util.Scanner sc = new java.util.Scanner(System.in);
        
        while(sc.hasNext()){
            String a = sc.next();
            String b = sc.next();
            int c = sc.nextInt();
            System.out.println(a + b + c);
        }
        
        sc.close();            
    }

}