import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import javax.swing.*;

public class AddExpense extends JFrame {
    private JTextField titleField;
    private JTextField amountField;
    private JComboBox<String> payerCombo;
    private JCheckBox[] participantCheckboxes;
    private MainMenu mainMenu;

    public AddExpense(ArrayList<String> participants, MainMenu mainMenu) {
        this.mainMenu = mainMenu;
        setTitle("Add Expense");
        setSize(300, 200);
        setLayout(new GridLayout(4, 1));

        titleField = new JTextField();
        amountField = new JTextField();
        payerCombo = new JComboBox<>(participants.toArray(new String[0]));

        participantCheckboxes = new JCheckBox[participants.size()];
        JPanel participantsPanel = new JPanel(new GridLayout(participants.size(), 1));
        for (int i = 0; i < participants.size(); i++) {
            participantCheckboxes[i] = new JCheckBox(participants.get(i));
            participantsPanel.add(participantCheckboxes[i]);
        }

        JButton addExpenseButton = new JButton("Add");
        addExpenseButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                addExpense();
            }
        });

        add(new JLabel("Expense Title:"));
        add(titleField);
        add(new JLabel("Amount:"));
        add(amountField);
        add(new JLabel("Pay:"));
        add(payerCombo);
        add(participantsPanel);
        add(addExpenseButton);
    }

    private void addExpense() {
        try {
            String title = titleField.getText();
            double amount = Double.parseDouble(amountField.getText());
            String payer = (String) payerCombo.getSelectedItem();

            ArrayList<String> selectedParticipants = new ArrayList<>();
            for (JCheckBox checkbox : participantCheckboxes) {
                if (checkbox.isSelected()) {
                    selectedParticipants.add(checkbox.getText());
                }
            }

            Expense newExpense = new Expense(title, amount, payer, selectedParticipants);
            mainMenu.addExpense(newExpense);
            dispose();
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Please enter a valid amount.");
        }
    }
}
