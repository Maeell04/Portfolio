import java.io.*;
import javax.swing.*;

public class ManagerLoader {
    public static MainMenu loadManager() {
        File saveDir = new File("save");

        if (!saveDir.exists() || saveDir.listFiles().length == 0) {
            JOptionPane.showMessageDialog(null, "No saved managers found.");
            return null;
        }

        File[] savedFiles = saveDir.listFiles((dir, name) -> name.endsWith("_manager.ser"));
        if (savedFiles == null || savedFiles.length == 0) {
            JOptionPane.showMessageDialog(null, "No saved managers found.");
            return null;
        }

        String[] fileNames = new String[savedFiles.length];
        for (int i = 0; i < savedFiles.length; i++) {
            fileNames[i] = savedFiles[i].getName();
        }

        String selectedFile = (String) JOptionPane.showInputDialog(null, "Select a manager to open:",
                "Open Manager", JOptionPane.QUESTION_MESSAGE, null, fileNames, fileNames[0]);

        if (selectedFile == null) {
            return null;
        }

        try (FileInputStream fileIn = new FileInputStream("save/" + selectedFile);
             ObjectInputStream in = new ObjectInputStream(fileIn)) {
            MainMenu manager = (MainMenu) in.readObject();
            manager.restoreState();
            return manager;
        } catch (Exception e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(null, "Error during loading: " + e.getMessage());
            return null;
        }
    }
}
