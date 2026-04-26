using Microsoft.Data.Sqlite;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;

public class UserProfileService
{
    static string HOST = "0.0.0.0";
    static int PORT = 5000;

    static async Task Main(string[] args)
    {
        // Start Listening for tasks
        TcpListener listener = new TcpListener(IPAddress.Parse(HOST), PORT);
        listener.Start();
        Console.WriteLine($"UserProfileService is listening...");

        // Generate database if it doersnt exist
        SQL.CreateUserProfileDatabase();
        Console.WriteLine($"Generated User Profile Database...");

        while (true)
        {
            TcpClient client = await listener.AcceptTcpClientAsync();

            _ = Task.Run(async () =>
            {
                // Setting up message stream
                using var stream = client.GetStream();
                using var ms = new MemoryStream();

                byte[] buffer = new byte[4096];
                int bytesRead;

                // Receiving chunks until message has been completed
                while ((bytesRead = await stream.ReadAsync(buffer, 0, buffer.Length)) > 0)
                {
                    ms.Write(buffer, 0, bytesRead);
                }

                string jsonMessage = Encoding.UTF8.GetString(ms.ToArray());
               
                Console.WriteLine($"UserProfileService Received: {jsonMessage}");

                // Attempt to Deserialize the message and execute command
                try
                {
                    var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                    UserProfileCommandMessage? commandMessage = JsonSerializer.Deserialize<UserProfileCommandMessage>(jsonMessage, options);

                    if(commandMessage is not null)
                    {
                        if(commandMessage.command == "register")
                        {
                            Commands.Register(commandMessage);
                        }
                    }

                }
                // Case Message Deserialization fails
                catch(Exception ex)
                {
                    Console.WriteLine($"Deserialize exception: {ex}");
                }
                    

                client.Close();
            });
        }
    }
}

public class UserProfileCommandMessage()
{
    public string? command { get; set; } = null;
    public string? username { get; set; } = null;
    public string? message { get; set; } = null;

    public int requestID { get; set; } = -1;
}


public class UserProfile
{
    public string UserId { get; set; } = "";

    public ProfileType ProfileType { get; set; } = ProfileType.Discord;

    public HashSet<string> PreferredKeywords { get; set; } = new();
    public HashSet<string> BlockedKeywords { get; set; } = new();
}

public enum ProfileType
{
    Discord,
}
