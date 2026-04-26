using DSharpPlus.CommandsNext;
using DSharpPlus.CommandsNext.Attributes;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;

namespace MuscleBot.commands
{ 
    public class BluSkyCommands : BaseCommandModule
    {
        static string BLUESKY_HOST = "dataingestion"; // change if outside docker
        static int BLUESKY_PORT = 5000;

        public static CommandContext? currentContext;

        [Command("ingest")]
        public async Task IngestBlueSky(CommandContext ctx)
        {
            try
            {
                using (TcpClient client = new TcpClient(BLUESKY_HOST, BLUESKY_PORT))
                {
                    // Create a default test command for now
                    CommandMessage commandMessage = new CommandMessage();

                    // Convert message to bytes
                    string json = JsonSerializer.Serialize(commandMessage);
                    byte[] bytes = Encoding.UTF8.GetBytes(json);

                    // Send out command to BluSky ingestion
                    NetworkStream stream = client.GetStream();
                    stream.Write(bytes, 0, bytes.Length);

                    // Saved context
                    currentContext = ctx;

                    Console.WriteLine($"Stored channel: {ctx.Channel.Id}");

                    await ctx.Channel.SendMessageAsync($"Sent -> {json}");
                }
            }
            catch (Exception e)
            {
                await ctx.Channel.SendMessageAsync($"Error sending: {e.Message}");
            }
        }
    }

    
}
