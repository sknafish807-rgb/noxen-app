public class NoxenCore {

    public static String process(String input) {
        return "NOXEN Java Core: " + input;
    }

    public static void main(String[] args) {
        String input = args.length > 0 ? args[0] : "System Ready";
        System.out.println(process(input));
    }
}
