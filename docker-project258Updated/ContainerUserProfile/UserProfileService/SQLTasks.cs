using Microsoft.Data.Sqlite;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;

public static class SQL
{
    public static bool UserExists(string username)
    {
        // Connect to the database
        using var connection = new SqliteConnection("Data Source=/app/data/userprofiles.db");
        connection.Open();

        // Find the user with the given username
        var command = connection.CreateCommand();
        command.CommandText =
        @"
        SELECT 1
        FROM UserProfiles
        WHERE Username = $username
        LIMIT 1;
        ";

        command.Parameters.AddWithValue("$username", username);

        // booleanize whether username was found
        var result = command.ExecuteScalar();

        return result != null;
    }

    public static void CreateUserProfileDatabase()
    {
        // Connect to the userprofile database 
        Directory.CreateDirectory("/app/data");
        using var sql = new SqliteConnection("Data Source=/app/data/userprofiles.db");
        sql.Open();

        // Create the new user and add to the database
        var createTable = sql.CreateCommand();
        createTable.CommandText =
            @" CREATE TABLE IF NOT EXISTS UserProfiles (Username TEXT PRIMARY KEY);";
        createTable.ExecuteNonQuery();
    }
}

