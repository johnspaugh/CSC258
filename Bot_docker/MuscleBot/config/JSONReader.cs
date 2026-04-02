using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MuscleBot.config
{
    public class JSONReader
    {
        public string token { get; set; } = "";
        public string prefix { get; set; } = "";

        public async Task ReadJSON()
        {
            var path = Path.Combine(AppContext.BaseDirectory, "config", "config.json");

            using (StreamReader sr = new StreamReader(path))
            {
                string json = await sr.ReadToEndAsync();
                JSONStructure data = JsonConvert.DeserializeObject<JSONStructure>(json);

                if (data != null)
                {
                    this.token = data.token;
                    this.prefix = data.prefix;
                }
                
            }
        }

    }


    internal sealed class JSONStructure
    {
        public string token { get; set; } = "";
        public string prefix { get; set; } = "";
    }
}
