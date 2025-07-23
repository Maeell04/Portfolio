import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;

public class ExpenseDAO {
    public void saveExpense(Connection conn, Expense expense) throws Exception {
        String sql = "INSERT INTO expenses (title, amount, payer, participants) VALUES (?, ?, ?, ?)";
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, expense.getTitle());
            ps.setDouble(2, expense.getAmount());
            ps.setString(3, expense.getPayer());
            ps.setString(4, String.join(",", expense.getParticipants()));
            ps.executeUpdate();
        }
    }

    public ArrayList<Expense> loadExpenses(Connection conn) throws Exception {
        String sql = "SELECT * FROM expenses";
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ResultSet rs = ps.executeQuery();
            ArrayList<Expense> expenses = new ArrayList<>();
            while (rs.next()) {
                String title = rs.getString("title");
                double amount = rs.getDouble("amount");
                String payer = rs.getString("pay");
                String participantsStr = rs.getString("participants");
                ArrayList<String> participants = new ArrayList<>();
                for (String p : participantsStr.split(",")) {
                    participants.add(p);
                }
                expenses.add(new Expense(title, amount, payer, participants));
            }
            return expenses;
        }
    }
}
