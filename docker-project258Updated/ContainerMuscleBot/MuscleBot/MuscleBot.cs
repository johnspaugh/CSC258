using DSharpPlus;
using DSharpPlus.CommandsNext;
using DSharpPlus.EventArgs;
using MuscleBot.commands;
using MuscleBot.config;
using MuscleBot.intake;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
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
        static readonly string HOST = "0.0.0.0";
        static readonly int PORT = 5000;

        private static Dictionary<int, CommandContext> PendingRequests = new Dictionary<int, CommandContext>();
        private static int RequestID = 0;

        private static DiscordClient? Client { get; set; }
        private static CommandsNextExtension? Commands { get; set; }

        static async Task Main(string[] args)
        {
            ConfigHandler reader = new ConfigHandler();

            // Starting Listener
            _ = Listener.Run(HOST, PORT);

            // Bot Setup
            await reader.LoadConfig();

            DiscordConfiguration discordConfig = new DiscordConfiguration()
            {
                Intents = DiscordIntents.All,
                Token = reader.token,
                TokenType = TokenType.Bot,
                AutoReconnect = true,
            };

            // Prepping discord bot to run
            Client = new DiscordClient(discordConfig);
            Client.Ready += Client_Ready;

            // Configurations for the discord bot
            var commandsConfig = new CommandsNextConfiguration()
            {
                StringPrefixes = new string[] { reader.prefix },
                EnableMentionPrefix = true,
                EnableDms = true,
                EnableDefaultHelp = false,
            };

            Commands = Client.UseCommandsNext(commandsConfig);
            
            // Registering all discord command groups
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
            // Incrementing request ID to make every ID unique
            int newRequestID = RequestID++;

            // Storing the request ID to finish request later
            PendingRequests[newRequestID] = commandContext;

            return newRequestID;
        }
        public static CommandContext? LookupRequest(int RequestID)
        {
            // Check for valid request ID
            if (PendingRequests.ContainsKey(RequestID) == false)
            {
                Console.WriteLine("ERROR: RequestID not found.");
                return null;
            }

            return PendingRequests[RequestID];
        }

        public static CommandContext? PopRequest(int RequestID)
        {
            // Check for valid request ID
            if(PendingRequests.ContainsKey (RequestID) == false)
            {
                Console.WriteLine($"ERROR: RequestID ({RequestID}) not found.");
                return null;
            }

            // Obtain discord context matching with the request ID
            CommandContext context = PendingRequests[RequestID];

            // Request complete and no longer pending
            PendingRequests.Remove(RequestID);

            return context;
        }
    }
}
