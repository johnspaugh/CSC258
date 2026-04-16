using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MuscleBot.intake
{
    public class FeedJsonReader
    {

    }


    internal sealed class FeedJson
    {
        public string Handle { get; set; } = "";
        public string displayName { get; set; } = "";
        public string Text { get; set; } = "";
        public string Created { get; set; } = "";
      
        public List<FeedJson> replies { get; set; } = new List<FeedJson>();
        public List<string> tags { get; set; } = new List<string>();
    }
}
