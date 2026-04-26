using Microsoft.Data.Sqlite;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;

public static class Commands
{
    static string RECEIVING_HOST = "musclebot";
    static int PORT = 5000;

    public static void Register(UserProfileCommandMessage receivedMessage)
    {
        // Build respond message to discord
        UserProfileCommandMessage commandMessage = new UserProfileCommandMessage();
        commandMessage.username = receivedMessage.username;
        commandMessage.requestID = receivedMessage.requestID;

        // If the username already exist no need to add to the database
        if (receivedMessage.username is not null && SQL.UserExists(receivedMessage.username))
            commandMessage.message = receivedMessage.username + " already exists.";
        else
        {
            // Register the discord username as a profile for our API
            using var sql = new SqliteConnection("Data Source=/app/data/userprofiles.db");
            sql.Open();

            var sqlCommand = sql.CreateCommand();
            sqlCommand.CommandText =
            @"
            INSERT OR IGNORE INTO UserProfiles (Username)
            VALUES ($username);
            ";

            sqlCommand.Parameters.AddWithValue("$username", receivedMessage.username);
            sqlCommand.ExecuteNonQuery();
        }

        // Send Response back to discord
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

