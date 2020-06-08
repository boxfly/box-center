package util;

import java.util.*;
public class Queues {
    public static void main(String[] args) {  
        queue();
        PriorityQueue(); 
    }
    private static void queue() {
        java.util.Queue<String> queue = new java.util.LinkedList<String>();
        queue.offer("Oklahoma");
        queue.offer("Indiana");
        queue.offer("Georgia");
        queue.offer("Texas");
        
        while(queue.size() > 0)
            System.out.print(queue.remove() + "  ");
    }
    private static void PriorityQueue() {
        PriorityQueue<String> queue1 = new PriorityQueue<String>();
        queue1.offer("Oklahoma");
        queue1.offer("Indiana");
        queue1.offer("Georgia");
        queue1.offer("Texas");

        System.out.println("Priority queue using Comparable:");
        while(queue1.size() > 0){
            System.out.print(queue1.remove() + "  ");
        }

        PriorityQueue<String> queue2 = new PriorityQueue<String>(4,Collections.reverseOrder());
        queue2.offer("Oklahoma");
        queue2.offer("Indiana");
        queue2.offer("Georgia");
        queue2.offer("Texas");

        System.out.println("\n Priority queue using Comparable:");
        while(queue2.size() > 0){
            System.out.print(queue2.remove() + "  ");
        }
    }
}
