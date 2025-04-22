import java.sql.Connection;
import java.sql.DriverManager;

public class DatabaseConnection {
    private static final String URL = "jdbc:mariadb://localhost:3306/expense_manager";
    private static final String USER = "root";
    private static final String PASSWORD = "toor";

    public static Connection getConnection() throws Exception {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }
}
