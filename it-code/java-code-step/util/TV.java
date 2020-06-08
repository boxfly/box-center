package util;
public class TV {
    public boolean on = false;
    public int channel = 1;
    public int volumeLevel = 1;
    public static int num = 0; // 静态方法才能修改静态变量
    static final int PRODUCT_NUM = 20200202;  //常量
    public TV(){

    }
    public static int numplus(){
        num++;
        return num;
    }
    public void turnOn(){
        on = true;
    }

    public void turnOff(){
        on = false;
    }

    public void setChannel(int newChannel){
        if(on && newChannel >= 1 && newChannel <= 120)
            channel = newChannel;
    }

    public void setVolume(int newVolumeLevel){
        if(on && newVolumeLevel >= 1 && newVolumeLevel <= 7){
            volumeLevel = newVolumeLevel;
        }
    }

    public void channelUp(){
        if(on && channel < 120)
            channel++;
    }

    public void channelDown(){
        if(on && channel >1){
            channel--;
        }
    }

    public void volumeUp(){
        if(on && volumeLevel < 7){
            volumeLevel++;
        }
    }

    public void volumeDown(){
        if(on && volumeLevel > 1){
            volumeLevel--;
        }
    }
}