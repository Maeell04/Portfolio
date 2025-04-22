import java.io.FileOutputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.ArrayList;

public class Manager implements Serializable {
    private String title;
    private ArrayList<String> participants;
    private ArrayList<Expense> expenses;

    public Manager(String title, ArrayList<String> participants) {
        this.title = title;
        this.participants = participants;
        this.expenses = new ArrayList<>();
    }

    public void addExpense(Expense expense) {
        this.expenses.add(expense);
    }

    public void saveManager(String filename) {
        try (FileOutputStream fileOut = new FileOutputStream(filename);
             ObjectOutputStream out = new ObjectOutputStream(fileOut)) {
            out.writeObject(this);
            System.out.println("Manager saved in " + filename);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
