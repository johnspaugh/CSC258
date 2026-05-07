using DSharpPlus.CommandsNext;
using System.Text.Json;
using System.Net.Sockets;
using System.Text;

namespace MuscleBot
{
    internal class Utility
    {
        public static string SendCommandMessage(object messageObject, string receivingHost, int port, CommandContext? ctx = null)
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

        public static void SendToLogs(string service, string username, string poster, string createdAt, string message)
        {
            LogMessage logMessage = new LogMessage
            {
                service = service,
                username = username,
                poster = poster,
                createdAt = createdAt,
                message = message
            };


            SendCommandMessage(logMessage, "logdatabase", 5000);
        }

        public class LogMessage
        {
            public string service { get; set; } = "";
            public string username { get; set; } = "";
            public string poster { get; set; } = "";
            public string createdAt { get; set; } = "";
            public string message { get; set; } = "";

        }

    }
}
