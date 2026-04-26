using MuscleBot.intake;
using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;

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

                _ = Task.Run(async () =>
                {
                    using var stream = client.GetStream();
                    using var ms = new MemoryStream();
                    byte[] buffer = new byte[4096];
                    int bytesRead;

                    while ((bytesRead = await stream.ReadAsync(buffer, 0, buffer.Length)) > 0)
                    {
                        ms.Write(buffer, 0, bytesRead);
                    }

                    string json = Encoding.UTF8.GetString(ms.ToArray());

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
