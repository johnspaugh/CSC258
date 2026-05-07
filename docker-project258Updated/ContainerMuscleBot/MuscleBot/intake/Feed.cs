using System.Text.Json;

namespace MuscleBot.intake
{
    public class FeedReader ()
    {
        public static FeedData? DeserializeFeed(string jsonString)
        {
            var options = new JsonSerializerOptions{PropertyNameCaseInsensitive = true};
            FeedData? feed = JsonSerializer.Deserialize<FeedData>(jsonString, options);

            return feed;
        }
    }


    public class FeedData
    {
        public string message { get; set; } = ""; 
        public List<string> path { get; set; } = new List<string>();
        public int iterations { get; set; } = 0;
        public string status { get; set; } = "";
        public List<Post> posts { get; set; } = new List<Post>();

        public int requestID { get; set; } = -1;
    }
    public class Post
    {
        public string text { get; set; } = "";
        public string display_name { get; set; } = "";
        public string handle { get; set; } = "";
        public string created_at { get; set; } = "";
        public List<string>? tags { get; set; } = null;
    }

}
