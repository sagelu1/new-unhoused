public class Home {
    private int[] availability;

    public Home(int[] availability){
        this.availability = availability;
    }

    public int length(){
        return availability.length;
    }

    public int getHouse(int index){
        return availability[index];
    }

    public void setHouse(int index, int value){
        availability[index] = value;
    }
}
