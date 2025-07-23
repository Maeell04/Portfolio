import java.util.HashMap;
import java.util.Map;

public class Balance {
    private Map<String, Double> balances;

    public Balance() {
        balances = new HashMap<>();
    }

    public void addBalance(String participant, double amount) {
        balances.put(participant, balances.getOrDefault(participant, 0.0) + amount);
    }

    public void displayBalance() {
        StringBuilder sb = new StringBuilder();
        for (Map.Entry<String, Double> entry : balances.entrySet()) {
            sb.append(entry.getKey()).append(" has a balance of ").append(entry.getValue()).append("€\n");
        }
        System.out.println(sb.length() > 0 ? sb.toString() : "No balances to show.");
    }

    public Map<String, Double> getBalances() {
        return balances;
    }
}
