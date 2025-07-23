import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class MainMenu extends JFrame implements Serializable {
    private static final long serialVersionUID = 1L;
    private String title;
    private ArrayList<String> participants;
    private ArrayList<Expense> expenses;
    private ArrayList<Transfer> transfers;

    public MainMenu(String title, ArrayList<String> participants) {
        this.title = title;
        this.participants = participants;
        this.expenses = new ArrayList<>();
        this.transfers = new ArrayList<>();
        initializeUI();
    }

    private void initializeUI() {
        setTitle("Expense Manager - " + title);
        setSize(400, 400);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        JButton groupExpensesButton = new JButton("Group Expenses");
        JButton balanceButton = new JButton("Balance");
        JButton addButton = new JButton("+ Add Expense");
        JButton addTransferButton = new JButton("Add Transfer");
        JButton saveButton = new JButton("Save Manager");
        JButton closeButton = new JButton("Close");

        JPanel topPanel = new JPanel(new BorderLayout());
        topPanel.add(closeButton, BorderLayout.WEST);
        topPanel.add(saveButton, BorderLayout.CENTER);

        add(topPanel, BorderLayout.NORTH);
        add(groupExpensesButton, BorderLayout.WEST);
        add(balanceButton, BorderLayout.EAST);
        add(addButton, BorderLayout.SOUTH);
        add(addTransferButton, BorderLayout.CENTER);

        groupExpensesButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                showGroupExpenses();
            }
        });

        balanceButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                showBalance();
            }
        });

        addButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                showAddExpense();
            }
        });

        addTransferButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                showAddTransfer();
            }
        });

        saveButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                saveManager();
            }
        });

        closeButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                closeApplication();
            }
        });
    }

    public void restoreState() {
        initializeUI();
        setVisible(true);
    }

    private void closeApplication() {
        int response = JOptionPane.showConfirmDialog(this, "Do you want to quit?", "Confirmation", JOptionPane.YES_NO_OPTION);
        if (response == JOptionPane.YES_OPTION) {
            System.exit(0);
        }
    }

    private void showGroupExpenses() {
        StringBuilder sb = new StringBuilder();
        for (Expense expense : expenses) {
            sb.append(expense).append("\n");
        }
        JOptionPane.showMessageDialog(this, sb.length() > 0 ? sb.toString() : "No expenses added.");
    }

    /**
     * Calculer et afficher la balance avec des arrondis au centième.
     */
    private void showBalance() {
        Map<String, Double> balanceMap = new HashMap<>();

        // Initialiser la balance pour chaque participant
        for (String participant : participants) {
            balanceMap.put(participant, 0.0);
        }

        // Calculer les dettes à partir des dépenses
        for (Expense expense : expenses) {
            double amountPerParticipant = expense.getAmount() / expense.getParticipants().size();
            for (String participant : expense.getParticipants()) {
                if (!participant.equals(expense.getPayer())) {
                    balanceMap.put(participant, balanceMap.get(participant) - amountPerParticipant);
                    balanceMap.put(expense.getPayer(), balanceMap.get(expense.getPayer()) + amountPerParticipant);
                }
            }
        }

        // Calculer les transferts
        for (Transfer transfer : transfers) {
            balanceMap.put(transfer.getSource(), balanceMap.get(transfer.getSource()) - transfer.getAmount());
            balanceMap.put(transfer.getDestination(), balanceMap.get(transfer.getDestination()) + transfer.getAmount());
        }

        // Réduire les dettes et arrondir au centième
        StringBuilder sb = new StringBuilder();
        for (String participant : balanceMap.keySet()) {
            double balance = balanceMap.get(participant);
            if (balance < 0) {
                for (String other : balanceMap.keySet()) {
                    if (balanceMap.get(other) > 0 && balance != 0) {
                        double minTransfer = Math.min(balanceMap.get(other), -balance);
                        balanceMap.put(participant, balanceMap.get(participant) + minTransfer);
                        balanceMap.put(other, balanceMap.get(other) - minTransfer);

                        // Arrondir au centième
                        minTransfer = Math.round(minTransfer * 100.0) / 100.0;
                        sb.append(participant).append(" owes ").append(String.format("%.2f", minTransfer))
                          .append("€ to ").append(other).append("\n");
                    }
                }
            }
        }

        JOptionPane.showMessageDialog(this, sb.length() > 0 ? sb.toString() : "No balance available.");
    }

    private void showAddExpense() {
        AddExpense addExpense = new AddExpense(participants, this);
        addExpense.setVisible(true);
    }

    private void showAddTransfer() {
        AddTransfer addTransfer = new AddTransfer(participants, this);
        addTransfer.setVisible(true);
    }

    public void addExpense(Expense expense) {
        expenses.add(expense);
        JOptionPane.showMessageDialog(this, "Expense added successfully!");
    }

    public void addTransfer(Transfer transfer) {
        transfers.add(transfer);
        JOptionPane.showMessageDialog(this, "Transfer added successfully!");
    }

    private void saveManager() {
        try {
            File saveDir = new File("save");
            if (!saveDir.exists()) {
                saveDir.mkdir();
            }

            String fileName = "save/" + title + "_manager.ser";
            try (FileOutputStream fileOut = new FileOutputStream(fileName);
                 ObjectOutputStream out = new ObjectOutputStream(fileOut)) {
                out.writeObject(this);
                JOptionPane.showMessageDialog(this, "Manager saved successfully to " + fileName);
            }
        } catch (Exception e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(this, "Error during save: " + e.getMessage());
        }
    }
}
