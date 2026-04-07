using DSharpPlus.CommandsNext;
using DSharpPlus.CommandsNext.Attributes;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;

namespace MuscleBot.commands
{
    public class BlueSkyCommands
    {
        [Command("BlueSky")]
        public async Task IngestBlueSky(CommandContext ctx)
        {
            using var client = new TcpClient("muscleBot", 9000);
            using var stream = client.GetStream();

            var msg = Encoding.UTF8.GetBytes("INGEST:");
            await stream.WriteAsync(msg, 0, msg.Length);

            using var ms = new MemoryStream();
            byte[] buffer = new byte[1024];
            int bytesRead;

            // Read in segments of the message each loop until complete
            while ((bytesRead = await stream.ReadAsync(buffer, 0, buffer.Length)) > 0)
            {
                ms.Write(buffer, 0, bytesRead);

                if (bytesRead <= 0)
                    break;
            }

            // Decode the incoming BlueSky feed json
            string response = Encoding.UTF8.GetString(buffer, 0, bytesRead);

            await ctx.RespondAsync(response);
        }
    }

    
}
