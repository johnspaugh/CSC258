using DSharpPlus.CommandsNext;
using System.Text.Json;
using System.Net.Sockets;
using System.Text;

namespace MuscleBot.commands
{
    internal class Utility
    {
        public static string SendCommandMessage(CommandContext ctx, object messageObject, string receivingHost, int port)
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
}
