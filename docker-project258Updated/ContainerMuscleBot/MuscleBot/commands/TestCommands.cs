using DSharpPlus.CommandsNext;
using DSharpPlus.CommandsNext.Attributes;
using MuscleBot.intake;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MuscleBot.commands
{
    public class TestCommands : BaseCommandModule
    {
        [Command("test")]
        public async Task TestCommand(CommandContext ctx)
        {
            await ctx.Channel.SendMessageAsync($"Hello {ctx.User.Username}");
        }


        [Command("add")]
        public async Task ADD(CommandContext ctx, int number1, int number2)
        {
            int result = number1 + number2;
            await ctx.Channel.SendMessageAsync($"The answer is {result}");
        }

        [Command("testJsonReader")]
        public async Task TestJsonReader(CommandContext ctx)
        {
            FeedData? feed = FeedReader.DeserializeFeed(jsonTestString);

            if(feed is not null)
            {
                await ctx.Channel.SendMessageAsync(
                    $"Display Name: {feed.display_name}\n" +
                    $"Handle: {feed.handle}\n" +
                    $"CreatedAt: {feed.created_at}\n" +
                    $"Text: {feed.text}");
            }
            else
                await ctx.Channel.SendMessageAsync($"Failed to deserialize test Feed");
        }


        string jsonTestString = @"
        {
          ""display_name"": ""John Doe"",
          ""text"": ""Hello World!"",
          ""created_at"": ""2026-04-15T12:34:56Z"",
          ""handle"": ""@johndoe.bsky.social"",
          ""parent"": {
            ""parent"": {
              ""cid"": ""bafyreparent123"",
              ""uri"": ""at://user/post/123"",
              ""py_type"": ""com.atproto.repo.strongRef""
            },
            ""root"": {
              ""cid"": ""bafyroot456"",
              ""uri"": ""at://user/post/456"",
              ""py_type"": ""com.atproto.repo.strongRef""
            }
          },
          ""tags"": ""test"",
          ""indexed_at"": ""2026-04-15T12:35:00Z"",
          ""python_map"": """"
        }";
    }
}
