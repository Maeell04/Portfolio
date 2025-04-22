public class App {
    public static void main(String[] args) {
        // Start the application
        MainMenu menu = ManagerLoader.loadManager(); // Load a expense manager
        if (menu != null) {
            menu.setVisible(true);
        } else {
            ManagerCreation creation = new ManagerCreation();
            creation.setVisible(true);
        }
    }
}
