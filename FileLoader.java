import java.io.*;

public class FileLoader {
    public String loadFile(String fileName) throws IOException {
        File file = new File("/var/data/" + fileName);
        BufferedReader reader = new BufferedReader(new FileReader(file));
        StringBuilder content = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            content.append(line);
        }
        reader.close();
        return content.toString();
    }
}
