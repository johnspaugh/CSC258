using DSharpPlus.CommandsNext;
using MuscleBot.intake;
using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;

namespace MuscleBot.commands
{
    internal class Listener
    {
        static bool listenerRunning = true;

        static public async Task Run(string HOST, int PORT)
        {
            TcpListener listener = new TcpListener(IPAddress.Parse(HOST), PORT);
            listener.Start();

            while (listenerRunning)
            {
                var client = await listener.AcceptTcpClientAsync();

                _ = HandleClient(client);
            }
        }
        static async Task HandleClient(TcpClient client)
        {
            try
            {
                using var stream = client.GetStream();
                using var ms = new MemoryStream();

                byte[] buffer = new byte[4096];
                int bytesRead;

                // Read in message until its done
                while ((bytesRead = await stream.ReadAsync(buffer, 0, buffer.Length)) > 0)
                    ms.Write(buffer, 0, bytesRead);

                string json = Encoding.UTF8.GetString(ms.ToArray());

                // Parse and handle json message accordingly
                await HandleMessage(json);

                Console.WriteLine($"Received: {json}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Listener error: {ex}");
            }
            finally
            {
                client.Close();
            }
        }

        static async Task HandleMessage(string json)
        {
            using JsonDocument doc = JsonDocument.Parse(json);
            var root = doc.RootElement;

            // Check if the Json is a BluSky Messagea
            if (root.TryGetProperty("posts", out _))
            {
                var feed = FeedReader.DeserializeFeed2(json);

                if (feed is not null && feed.posts.Count > 0)
                {
                    Console.WriteLine($"Sending Feed to Discord Client.");
                    var bluSkyContext = BluSkyCommands.currentContext;

                    if (bluSkyContext is not null)
                    {
                        await bluSkyContext.Channel.SendMessageAsync(
                            $"Display Name: {feed.posts[0].display_name}\n" +
                            $"Handle: {feed.posts[0].handle}\n" +
                            $"CreatedAt: {feed.posts[0].created_at}\n" +
                            $"Text: {feed.posts[0].text}");
                    }
                }
            }

            // Check if the Json is a UserProfile message
            else if (root.TryGetProperty("requestID", out _))
            {
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                UserProfileCommandMessage? userProfileCommandMessage = JsonSerializer.Deserialize<UserProfileCommandMessage>(json, options);

                if (userProfileCommandMessage is not null)
                {
                    CommandContext? ctx = MuscleBot.LookupRequest(userProfileCommandMessage.requestID);
                    Console.WriteLine("test.");
                    if (ctx is not null)
                        await ctx.Channel.SendMessageAsync(userProfileCommandMessage.message);
                }
            }
            else
            {
                Console.WriteLine("INVALID JSON");
            }
        }
        
    }
}
