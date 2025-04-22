import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;

public class ManagerCreation extends JFrame {
    private JTextField titleField;
    private ArrayList<JTextField> participantFields;
    private JPanel participantPanel;

    public ManagerCreation() {
        setTitle("Create Manager");
        setSize(300, 300);
        setLayout(new BorderLayout());

        titleField = new JTextField();
        participantFields = new ArrayList<>();

        // Adding a title field
        JPanel titlePanel = new JPanel(new GridLayout(2, 1));
        titlePanel.add(new JLabel("Manager Title:"));
        titlePanel.add(titleField);
        add(titlePanel, BorderLayout.NORTH);

        // Adding a panel for participants
        participantPanel = new JPanel(new GridLayout(0, 1));
        JButton addParticipantButton = new JButton("Add Participant");
        addParticipantButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                addParticipantField();
            }
        });

        participantPanel.add(addParticipantButton);
        add(participantPanel, BorderLayout.CENTER);

        // Creating the manager
        JButton createManagerButton = new JButton("Create Manager");
        createManagerButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                createManager();
            }
        });
        add(createManagerButton, BorderLayout.SOUTH);
    }

    private void addParticipantField() {
        JTextField participantField = new JTextField();
        participantFields.add(participantField);
        participantPanel.add(participantField);
        participantPanel.revalidate();
    }

    private void createManager() {
        String title = titleField.getText();
        ArrayList<String> participants = new ArrayList<>();
        for (JTextField field : participantFields) {
            participants.add(field.getText());
        }

        if (participants.size() < 2) {
            JOptionPane.showMessageDialog(this, "At least 2 participants are required.");
            return;
        }

        MainMenu menu = new MainMenu(title, participants);
        menu.setVisible(true);
        dispose();
    }
}
