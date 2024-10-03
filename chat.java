import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class OpenAIExample {

    public static void main(String[] args) {
        try {
            // OpenAI API URL for ChatGPT
            String apiUrl = "https://api.openai.com/v1/chat/completions";

            // API key for authorization
            String apiKey = "your-api-key-here";

            // Define the JSON body for the request
            String requestBody = "{\"model\": \"gpt-4\", \"messages\": [{\"role\": \"user\", \"content\": \"Hello!\"}], \"max_tokens\": 150}";

            // Create the URL and connection
            URL url = new URL(apiUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            // Set the request method and headers
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setRequestProperty("Authorization", "Bearer " + apiKey);

            // Enable sending the request body
            connection.setDoOutput(true);

            // Write the JSON body to the output stream
            try (OutputStream outputStream = connection.getOutputStream()) {
                byte[] input = requestBody.getBytes(StandardCharsets.UTF_8);
                outputStream.write(input, 0, input.length);
            }

            // Read the response
            int responseCode = connection.getResponseCode();
            System.out.println("Response Code: " + responseCode);

            // Handle the response (you can read the response input stream here)

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
