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
        // Functional 
        public string message { get; set; } = "request";
        public int requestID { get; set; } = -1;

        // Data Logging 
        public string[] path { get; set; } = new string[] { "dataRequest" };
        public int iterations { get; set; } = 1;
        public string status { get; set; } = "requested";
    }

}
