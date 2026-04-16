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

namespace MuscleBotTest
{
    internal class Program
    {
        static string HOST = "0.0.0.0";
        static int PORT = 5000;

        private static DiscordClient? Client { get; set; }
        private static CommandsNextExtension? Commands { get; set; }

        static async Task Main(string[] args)
        {
            JSONReader reader = new JSONReader();

            // Starting Listener
            _ = RunListener();


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

            // Run the bot
            await Client.ConnectAsync();
            await Task.Delay(-1);
        }

        static Task Client_Ready(DiscordClient sender, ReadyEventArgs args)
        {
            return Task.CompletedTask;
        }

        static bool listenerRunning = true;
        static async Task RunListener()
        {
            TcpListener listener = new TcpListener(IPAddress.Parse(HOST), PORT);
            listener.Start();

            while (listenerRunning)
            {
                var client = await listener.AcceptTcpClientAsync();

                _ = Task.Run(async () =>
                {
                    using var stream = client.GetStream();
                    using var ms = new MemoryStream();
                    byte[] buffer = new byte[4096];
                    int bytesRead = await stream.ReadAsync(buffer, 0, buffer.Length);
                    string json = Encoding.UTF8.GetString(buffer, 0, bytesRead);

                    Console.WriteLine($"Received: {json}");

                    // testing
                    if (BlueSkyCommands.currentContext is not null)
                    {
                        var ctx = BlueSkyCommands.currentContext;
                        try
                        {
                            FeedData2? feed = FeedReader.DeserializeFeed2(json);
                            Console.WriteLine("Deserialized SUCCESS");

                            if (feed is not null && feed.posts.Count > 0)
                            {
                                Console.WriteLine($"Feed sending");

                                await ctx.Channel.SendMessageAsync(
                                    $"Display Name: {feed.posts[0].display_name}\n" +
                                    $"Handle: {feed.posts[0].handle}\n" +
                                    $"CreatedAt: {feed.posts[0].created_at}\n" +
                                    $"Text: {feed.posts[0].text}");
                            }
                            else
                                await ctx.Channel.SendMessageAsync($"Failed to deserialize test Feed");
                        }
                        catch (Exception ex)
                        {
                            Console.WriteLine($"Deserialize exception: {ex}");
                        }
                    }
                    else
                        Console.WriteLine("Context is empty.");

                    client.Close();
                });
            }
        }

    }
}
