using DSharpPlus.CommandsNext;
using DSharpPlus.CommandsNext.Attributes;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;

namespace MuscleBot.commands
{ 
    public class BlueSkyCommands : BaseCommandModule
    {
        static string BLUESKY_HOST = "dataingestion"; // change if outside docker
        static int BLUESKY_PORT = 5000;

        [Command("Ingest")]
        public async Task IngestBlueSky(CommandContext ctx)
        {
            try
            {
                using (TcpClient client = new TcpClient(BLUESKY_HOST, BLUESKY_PORT))
                {
                    // Create a default test command for now
                    Command command = new Command();

                    // Convert message to bytes
                    string json = JsonSerializer.Serialize(command);
                    byte[] bytes = Encoding.UTF8.GetBytes(json);

                    // Send out command to BluSky ingestion
                    NetworkStream stream = client.GetStream();
                    stream.Write(bytes, 0, bytes.Length);

                    await ctx.Channel.SendMessageAsync($"Sent -> {json}");
                }
            }
            catch (Exception e)
            {
                await ctx.Channel.SendMessageAsync($"Error sending: {e.Message}");
            }
        }

        public class Command
        {
            public string message { get; set; } = "request";
            public string[] path { get; set; }  = new string[] { "dataRequest" };
            public int iterations { get; set; }  = 1;
            public string status { get; set; }  = "requested";
        
        }
    }

    
}
