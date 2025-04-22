import java.io.Serializable;
import java.util.ArrayList;

public class ExpenseManager implements Serializable {
    private static final long serialVersionUID = 1L;
    private String title;
    private ArrayList<String> participants;
    private ArrayList<Expense> expenses;
    private ArrayList<Transfer> transfers;

    public ExpenseManager(String title, ArrayList<String> participants) {
        this.title = title;
        this.participants = participants;
        this.expenses = new ArrayList<>();
        this.transfers = new ArrayList<>();
    }

    public String getTitle() {
        return title;
    }

    public ArrayList<String> getParticipants() {
        return participants;
    }

    public ArrayList<Expense> getExpenses() {
        return expenses;
    }

    public ArrayList<Transfer> getTransfers() {
        return transfers;
    }

    public void addExpense(Expense expense) {
        expenses.add(expense);
    }

    public void addTransfer(Transfer transfer) {
        transfers.add(transfer);
    }

    @Override
    public String toString() {
        return "ExpenseManager{" +
                "title='" + title + '\'' +
                ", participants=" + participants +
                ", expenses=" + expenses +
                ", transfers=" + transfers +
                '}';
    }
}
