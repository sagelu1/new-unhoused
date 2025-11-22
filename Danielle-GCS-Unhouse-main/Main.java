import java.util.*;
import java.io.*;

public class Main {
    public static void main(String[] args) {
        int months = 12;
        ArrayList<Agent> agentList = new ArrayList<>();

        ArrayList<ArrayList<Integer>> assetsByMonth = new ArrayList<>();
        ArrayList<ArrayList<Boolean>> homelessByMonth = new ArrayList<>();
        ArrayList<ArrayList<Boolean>> disabilityByMonth = new ArrayList<>();
        ArrayList<ArrayList<Boolean>> jobTrainingByMonth = new ArrayList<>();

        // --- Read agent data from file ---
        try {
            BufferedReader br = new BufferedReader(new FileReader("agent_input.txt"));
            String line = br.readLine(); // skip "each"
            while ((line = br.readLine()) != null) {
                String[] parts = line.split(",");
                int asset = Integer.parseInt(parts[0]);
                boolean disability = Boolean.parseBoolean(parts[1]);
                boolean jobTraining = Boolean.parseBoolean(parts[2]);
                boolean homeless = Boolean.parseBoolean(parts[3]);
                boolean everHomeless = Boolean.parseBoolean(parts[4]);
                agentList.add(new Agent("Agent_" + (agentList.size() + 1),
                        asset, disability, jobTraining, homeless, everHomeless));
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }

        int[] homesList = {1,1,1,1,1,1,1,1,1,1};
        Home availHomes = new Home(homesList);

        // --- Simulation loop ---
        for (int m = 1; m <= months; m++) {

            // ➤ Apply monthly asset updates only AFTER month 1
            if (m > 1) {
                for (Agent a : agentList) {
                    a.updateMonthlyAsset();
                }
            }

            // --- Record month BEFORE sorting ---
            ArrayList<Integer> monthAssets = new ArrayList<>();
            ArrayList<Boolean> monthHomeless = new ArrayList<>();
            ArrayList<Boolean> monthDisability = new ArrayList<>();
            ArrayList<Boolean> monthJobTraining = new ArrayList<>();

            for (Agent ag : agentList) {
                monthAssets.add(ag.getAsset());
                monthHomeless.add(ag.getHomeless());
                monthDisability.add(ag.getDisability());
                monthJobTraining.add(ag.getJobTraining());
            }

            assetsByMonth.add(monthAssets);
            homelessByMonth.add(monthHomeless);
            disabilityByMonth.add(monthDisability);
            jobTrainingByMonth.add(monthJobTraining);

            // --- Now sort agents ONLY for housing logic ---
            agentList.sort((a,b) -> Integer.compare(b.getAsset(), a.getAsset()));

            // --- Housing logic (unchanged) ---
            for (int n = 0; n < agentList.size(); n++) {
                int agentAsset = agentList.get(n).getAsset();
                if (agentAsset >= 20) {
                    for (int house = 0; house < availHomes.length(); house++) {
                        if (availHomes.getHouse(house) == 0 && agentList.get(n).getHomeless() && !agentList.get(n).getEverHomeless()) {
                            availHomes.setHouse(house,1);
                            agentList.get(n).setHomeless(false);
                        }
                    }
                } else if (agentAsset >= 10) {
                    for (int house = 0; house < availHomes.length()/2; house++) {
                        if (availHomes.getHouse(house) == 0 && agentList.get(n).getHomeless() && !agentList.get(n).getEverHomeless()) {
                            availHomes.setHouse(house,1);
                            agentList.get(n).setHomeless(false);
                        }
                    }
                } else {
                    agentList.get(n).setHomeless(true);
                    availHomes.setHouse(n,0);
                }
            }
        }

        // --- CSV Export ---
        try {
            // Assets
            FileWriter fw = new FileWriter("assets.csv");
            fw.write("Month");
            for (int a=0; a<agentList.size(); a++) fw.write(",Agent_" + (a+1));
            fw.write("\n");
            for (int m=0; m<months; m++) {
                fw.write("" + (m+1));
                for (int a=0; a<agentList.size(); a++) fw.write("," + assetsByMonth.get(m).get(a));
                fw.write("\n");
            }
            fw.close();

            // Homeless
            fw = new FileWriter("homeless.csv");
            fw.write("Month");
            for (int a=0; a<agentList.size(); a++) fw.write(",Agent_" + (a+1));
            fw.write("\n");
            for (int m=0; m<months; m++) {
                fw.write("" + (m+1));
                for (int a=0; a<agentList.size(); a++) fw.write("," + (homelessByMonth.get(m).get(a) ? 1 : 0));
                fw.write("\n");
            }
            fw.close();

            // Disability
            fw = new FileWriter("disability.csv");
            fw.write("Month,Disability_Total\n");
            for (int m=0; m<months; m++) {
                int totalDisability = 0;
                for (int a=0; a<agentList.size(); a++)
                    if (disabilityByMonth.get(m).get(a)) totalDisability++;
                fw.write((m+1) + "," + totalDisability + "\n");
            }
            fw.close();

            // Job Training
            fw = new FileWriter("jobtraining.csv");
            fw.write("Month,JobTraining_Total\n");
            for (int m=0; m<months; m++) {
                int totalTraining = 0;
                for (int a=0; a<agentList.size(); a++)
                    if (jobTrainingByMonth.get(m).get(a)) totalTraining++;
                fw.write((m+1) + "," + totalTraining + "\n");
            }
            fw.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
