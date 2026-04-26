using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;

public static class Commands
{
    static string RECEIVING_HOST = "musclebot";
    static int PORT = 5000;

    public static void Register(UserProfileCommandMessage receivedMessage)
    {
        UserProfileCommandMessage commandMessage = new UserProfileCommandMessage();
        commandMessage.username = receivedMessage.username;
        commandMessage.message = receivedMessage.username + " has been Registered";
        commandMessage.requestID = receivedMessage.requestID;

        SendCommandMessage(commandMessage, RECEIVING_HOST, PORT);
    }



    public static string SendCommandMessage(object messageObject, string receivingHost, int port)
    {
        try
        {
            using (TcpClient client = new TcpClient(receivingHost, port))
            {
                // Convert message to bytes
                string json = JsonSerializer.Serialize(messageObject);
                byte[] bytes = Encoding.UTF8.GetBytes(json);

                // Send out command to target host
                NetworkStream stream = client.GetStream();
                stream.Write(bytes, 0, bytes.Length);

                return $"Sent -> {json}";
            }
        }
        catch (Exception e)
        {
            return $"Error sending: {e.Message}";
        }
    }
}

