using DSharpPlus.CommandsNext;
using DSharpPlus.CommandsNext.Attributes;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;

namespace MuscleBot.commands
{
    [Group("user")]
    public class UserProfileCommands : BaseCommandModule
    {
        static string USERPROFILE_HOST = "userprofileservice"; // change if outside docker
        static int USERPROFILE_PORT = 5000;

        public static CommandContext? currentContext;

        [Command("register")]
        public async Task Register(CommandContext ctx)
        {
            UserProfileCommandMessage message = new UserProfileCommandMessage();
            message.command = "register";
            message.username = ctx.User.Username;
            message.requestID = MuscleBot.GenerateRequestID(ctx); 

            string discordMessage = Utility.SendCommandMessage(ctx, message, USERPROFILE_HOST, USERPROFILE_PORT);

            await ctx.Channel.SendMessageAsync(discordMessage);
        }
    }
    public class UserProfileCommandMessage()
    {
        public string? command { get; set; } = null;
        public string? username { get; set; } = null;
        public string? message { get; set; } = null;

        public int requestID { get; set; } = -1;
    }

}
