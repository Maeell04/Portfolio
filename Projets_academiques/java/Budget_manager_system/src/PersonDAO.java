import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;

public class PersonDAO {
    public void savePerson(Connection conn, String person) throws Exception {
        String sql = "INSERT INTO participants (name) VALUES (?)";
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, person);
            ps.executeUpdate();
        }
    }

    public ArrayList<String> loadParticipants(Connection conn) throws Exception {
        String sql = "SELECT * FROM participants";
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ResultSet rs = ps.executeQuery();
            ArrayList<String> participants = new ArrayList<>();
            while (rs.next()) {
                participants.add(rs.getString("name"));
            }
            return participants;
        }
    }
}
