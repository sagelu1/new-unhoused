public class Agent{
    int asset;
    boolean disability;
    boolean jobTraining;
    boolean homeless;
    private String name;
    boolean everHomeless;

    public Agent(String name, int asset, boolean disability, 
                    boolean jobTraining, boolean homeless, boolean everHomeless){
        this.name = name;
        this.asset = asset;
        this.disability = disability;
        this.jobTraining = jobTraining;
        this.homeless = homeless;
        this.everHomeless = everHomeless;
    }

    public String getAgentName(){
        return name;
    }

    public int getAsset(){
        return asset;
    }

public void updateMonthlyAsset(){
    int newAsset = this.asset;

    int delta;

    if (homeless) {
        // When homeless, it’s harder to increase assets:
        // original range: -6..+6  (13 values)
        // homeless range: -6..+3  (10 values)  → max shifted down by 3
        delta = (int)(Math.random() * 10) - 6;   // -6, -5, ..., +3
    } else {
        // Original range for housed agents
        delta = (int)(Math.random() * 13) - 6;   // -6, -5, ..., +6
    }

    newAsset += delta;

    if (disability && newAsset >= 5) {
        newAsset -= 5;
    }
    if (jobTraining && newAsset >= 0) {
        newAsset += 5;
    }

    if (newAsset < 0) newAsset = 0;
    if (newAsset > 100) newAsset = 100;

    this.asset = newAsset;  // updates current asset
}
    
    // Added missing getters/setters used by Main.java
    public boolean getHomeless(){
        return this.homeless;
    }

    public void setHomeless(boolean h){
        this.homeless = h;
        if (h) this.everHomeless = true;
    }

    public boolean getDisability(){
        return this.disability;
    }

    public boolean getJobTraining(){
        return this.jobTraining;
    }

    public boolean getEverHomeless(){
        return this.everHomeless;
    }
}

