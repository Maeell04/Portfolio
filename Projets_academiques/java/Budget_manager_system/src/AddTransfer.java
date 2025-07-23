import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;

public class AddTransfer extends JFrame {
    private JTextField titleField;
    private JTextField amountField;
    private JComboBox<String> sourceCombo;
    private JComboBox<String> destinationCombo;
    private MainMenu mainMenu;

    public AddTransfer(ArrayList<String> participants, MainMenu mainMenu) {
        this.mainMenu = mainMenu;
        setTitle("Add Transfer");
        setSize(300, 200);
        setLayout(new GridLayout(5, 1));

        titleField = new JTextField("Reimbursement");
        amountField = new JTextField();
        sourceCombo = new JComboBox<>(participants.toArray(new String[0]));
        destinationCombo = new JComboBox<>(participants.toArray(new String[0]));

        JButton addTransferButton = new JButton("Add Transfer");
        addTransferButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                addTransfer();
            }
        });

        add(new JLabel("Transfer Title:"));
        add(titleField);
        add(new JLabel("Amount:"));
        add(amountField);
        add(new JLabel("Source:"));
        add(sourceCombo);
        add(new JLabel("Destination:"));
        add(destinationCombo);
        add(addTransferButton);
    }

    private void addTransfer() {
        try {
            String title = titleField.getText();
            double amount = Double.parseDouble(amountField.getText());
            String source = (String) sourceCombo.getSelectedItem();
            String destination = (String) destinationCombo.getSelectedItem();

            Transfer newTransfer = new Transfer(title, amount, source, destination);
            mainMenu.addTransfer(newTransfer);
            dispose();
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Please enter a valid amount.");
        }
    }
}
