public class code {
    
    public static int add(int a, int b) {
        int c = a + b;
        return c;
    }

    public static int test(int a, int b, float c) {
        return a + b;
    }

    public static void hello(String name) {
        System.out.println("Hello " + name);
    }

    public static void main(String[] args) {
        add(2022, 1);
        hello("world");
        test(6,7,8.6);
    }

}
