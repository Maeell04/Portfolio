import java.io.Serializable;

public class Transfer implements Serializable {
    private static final long serialVersionUID = 1L;
    private String title;
    private double amount;
    private String source;
    private String destination;

    public Transfer(String title, double amount, String source, String destination) {
        this.title = title;
        this.amount = amount;
        this.source = source;
        this.destination = destination;
    }

    public String getTitle() {
        return title;
    }

    public double getAmount() {
        return amount;
    }

    public String getSource() {
        return source;
    }

    public String getDestination() {
        return destination;
    }

    @Override
    public String toString() {
        return title + " - " + amount + "€ from " + source + " to " + destination;
    }
}
