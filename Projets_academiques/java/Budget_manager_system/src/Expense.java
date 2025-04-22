import java.io.Serializable;
import java.util.ArrayList;

public class Expense implements Serializable {
    private static final long serialVersionUID = 1L;
    private String title;
    private double amount;
    private String payer;
    private ArrayList<String> participants;

    public Expense(String title, double amount, String payer, ArrayList<String> participants) {
        this.title = title;
        this.amount = amount;
        this.payer = payer;
        this.participants = participants;
    }

    public String getTitle() {
        return title;
    }

    public double getAmount() {
        return amount;
    }

    public String getPayer() {
        return payer;
    }

    public ArrayList<String> getParticipants() {
        return participants;
    }

    @Override
    public String toString() {
        return title + " - " + amount + "€ paid by " + payer;
    }
}
