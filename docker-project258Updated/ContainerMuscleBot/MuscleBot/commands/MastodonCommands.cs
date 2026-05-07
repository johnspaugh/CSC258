using DSharpPlus.CommandsNext;
using DSharpPlus.CommandsNext.Attributes;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;

namespace MuscleBot.commands
{ 
    [Group("mastodon")]
    public class MastodonCommands : BaseCommandModule
    {
        static string MASTODON_HOST = "dataingestionmastodon"; // change if outside docker
        static int MASTODON_PORT = 5000;

        public static CommandContext? currentContext;

        [Command("ingest")]
        public async Task IngestMastodon(CommandContext ctx, string keyword)
        {
            // Create a default test command for now
            CommandMessage commandMessage = new CommandMessage();
            commandMessage.message = keyword;
            commandMessage.requestID = MuscleBot.GenerateRequestID(ctx);

            Console.WriteLine($"Sending with RequestID ({commandMessage.requestID})");

            // Convert message to bytes
            string discordMessage = Utility.SendCommandMessage(commandMessage, MASTODON_HOST, MASTODON_PORT, ctx);

            await ctx.Channel.SendMessageAsync(discordMessage);
        }
    }

    
}
