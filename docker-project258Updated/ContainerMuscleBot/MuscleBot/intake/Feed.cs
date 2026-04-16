using System.Text.Json;

namespace MuscleBot.intake
{
    public class FeedReader ()
    {
        public static FeedData? DeserializeFeed(string jsonString)
        {
            var options = new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            };

            FeedData? feed = JsonSerializer.Deserialize<FeedData>(jsonString);

            return feed;
        }

        public static FeedData2? DeserializeFeed2(string jsonString)
        {
            var options = new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            };

            FeedData2? feed = JsonSerializer.Deserialize<FeedData2>(jsonString);

            return feed;
        }
    }


    public class FeedData2
    {
        public string message { get; set; } = ""; 
        public List<string> path { get; set; } = new List<string>();
        public int iterations { get; set; } = 0;
        public string status { get; set; } = "";
        public List<Post2> posts { get; set; } = new List<Post2>();
    }

    public class Post2
    {
        public string text { get; set; } = "";
        public string display_name { get; set; } = "";
        public string handle { get; set; } = "";
        public string created_at { get; set; } = "";
        public string? tags { get; set; } = "";
    }

    public class FeedData
    {
        public string display_name { get; set; } = "";
        public string text { get; set; } = "";
        public string created_at { get; set; } = "";
        public string handle { get; set; } = "";
        public ReplyContext? parent { get; set; } = null;
        public string tags { get; set; } = "";
        public string indexed_at { get; set; } = "";
        public string python_map { get; set; } = "";
    }
    public class ReplyContext
    {
        public PostRef? parent { get; set; } = null;
        public PostRef? root { get; set; } = null;
    }

    public class PostRef
    {
        public string cid { get; set; } = "";
        public string uri { get; set; } = "";
        public string py_type { get; set; } = "";
    }
}
