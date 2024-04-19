package Database;
import java.sql.*;
import java.util.Properties;
public class DbConnect {
	public static Connection connection;
	public static String dbname = "";//graphbipartite
	public DbConnect() {
		 try {
			//Establishing connection
		 	Properties properties = new Properties();
		    properties.setProperty("user", "root");
		    properties.setProperty("password", "hsn123");
		    properties.setProperty("connectTimeout", Integer.toString(1728000));
		    //String year = "2022";
			 connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/"+dbname, properties);
			 System.out.println("Connected With the database successfully");
			 } catch (SQLException e) {
			 System.out.println("Error while connecting to the database");
			 }
	}
	
}
