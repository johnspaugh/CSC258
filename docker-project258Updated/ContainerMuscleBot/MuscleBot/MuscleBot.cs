using DSharpPlus;
using DSharpPlus.CommandsNext;
using DSharpPlus.EventArgs;
using MuscleBot.commands;
using MuscleBot.config;
using MuscleBot.intake;
using System;
using System.Collections.Generic;
using System.Formats.Asn1;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Channels;
using System.Threading.Tasks;

namespace MuscleBot
{
    internal class MuscleBot
    {
        static string HOST = "0.0.0.0";
        static int PORT = 5000;

        private static Dictionary<int, CommandContext> PendingRequests = new Dictionary<int, CommandContext>();
        private static int RequestID = 0;

        private static DiscordClient? Client { get; set; }
        private static CommandsNextExtension? Commands { get; set; }

        public static CommandContext TEMP { get; set; }

        static async Task Main(string[] args)
        {
            JSONReader reader = new JSONReader();

            // Starting Listener
            _ = Listener.Run(HOST, PORT);

            // Bot Setup
            await reader.ReadJSON();

            DiscordConfiguration discordConfig = new DiscordConfiguration()
            {
                Intents = DiscordIntents.All,
                Token = reader.token,
                TokenType = TokenType.Bot,
                AutoReconnect = true,
            };

            Client = new DiscordClient(discordConfig);
            Client.Ready += Client_Ready;

            var commandsConfig = new CommandsNextConfiguration()
            {
                StringPrefixes = new string[] { reader.prefix },
                EnableMentionPrefix = true,
                EnableDms = true,
                EnableDefaultHelp = false,
            };

            Commands = Client.UseCommandsNext(commandsConfig);

            Commands.RegisterCommands<TestCommands>();
            Commands.RegisterCommands<BlueSkyCommands>();
            Commands.RegisterCommands<MastodonCommands>();
            Commands.RegisterCommands<UserProfileCommands>();

            // Run the bot
            await Client.ConnectAsync();
            await Task.Delay(-1);
        }

        static Task Client_Ready(DiscordClient sender, ReadyEventArgs args)
        {
            return Task.CompletedTask;
        }

        public static int GenerateRequestID(CommandContext commandContext)
        {
            int newRequestID = RequestID++;
            PendingRequests[newRequestID] = commandContext;

            return newRequestID;
        }
        public static CommandContext? LookupRequest(int RequestID)
        {
            if (PendingRequests.ContainsKey(RequestID) == false)
            {
                Console.WriteLine("ERROR: RequestID not found.");
                return null;
            }

            return PendingRequests[RequestID];
        }

        public static CommandContext? CompleteRequest(int RequestID)
        {
            if(PendingRequests.ContainsKey (RequestID) == false)
            {
                Console.WriteLine("ERROR: RequestID not found.");
                return null;
            }    

            CommandContext context = PendingRequests[RequestID];
            PendingRequests.Remove(RequestID);

            return context;
        }
    }
}
