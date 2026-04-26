using DSharpPlus.CommandsNext;
using DSharpPlus.CommandsNext.Attributes;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;

namespace MuscleBot.commands
{
    public class CommandMessage
    {
        public string message { get; set; } = "request";
        public string[] path { get; set; } = new string[] { "dataRequest" };
        public int iterations { get; set; } = 1;
        public string status { get; set; } = "requested";

    }

}
